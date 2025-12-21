import os
import sys
import webbrowser
import threading
import time
import uvicorn
from fastapi.staticfiles import StaticFiles
import traceback
from datetime import datetime
import psutil

def cleanup_old_processes():
    """기존에 실행 중인 MyBrainAI 프로세스를 찾아 종료"""
    try:
        current_pid = os.getpid()
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # 프로세스 이름이 MyBrainAI이고 현재 프로세스가 아닌 경우
                # macOS에서 번들 실행 시 이름이 'MyBrainAI'로 뜸
                if proc.info['name'] == 'MyBrainAI' and proc.info['pid'] != current_pid:
                    print(f"Found existing instance (PID: {proc.info['pid']}). Terminating...")
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    except Exception as e:
        print(f"Error during cleanup: {e}")

# 시작 시 기존 프로세스 정리
cleanup_old_processes()
if getattr(sys, 'frozen', False):
    # PyInstaller Bundle (macOS .app)
    # sys.executable: .../dist/MyBrainAI.app/Contents/MacOS/MyBrainAI
    exe_path = sys.executable
    
    # 목표: .app 번들이 있는 폴더(dist)를 CWD로 설정하여
    # dist/data 및 dist/error.txt를 사용하도록 함.
    
    # 1. .../Contents/MacOS
    exe_dir = os.path.dirname(exe_path)
    # 2. .../Contents
    contents_dir = os.path.dirname(exe_dir)
    # 3. .../MyBrainAI.app
    bundle_dir = os.path.dirname(contents_dir)
    # 4. .../dist (Bundle Parent)
    dist_dir = os.path.dirname(bundle_dir)
    
    # 만약 .app 구조가 아니라면(단일 실행파일 등), 안전하게 exe 있는 곳 사용
    if not bundle_dir.endswith('.app'):
         base_dir = os.path.dirname(os.path.abspath(sys.executable))
    else:
         base_dir = dist_dir

    os.chdir(base_dir)
else:
    # 개발 환경
    base_dir = os.path.dirname(os.path.abspath(__file__))

try:
    from apps.server.core.error_handler import log_critical_error
except ImportError:
    # 만약 이 모듈조차 로드 못하면 최후의 수단으로 간단히 정의
    def log_critical_error(e, context="System"):
        print(f"[CRITICAL] {context} Error: {e}")


try:
    from apps.server.main import app
    from apps.server.core.config import settings
except ImportError as e:
    log_critical_error(e, "Import")
    print("\n" + "="*60)
    print(f"CRITICAL ERROR: Failed to import required packages.")
    print(f"Missing dependency: {e}")
    print("Please contact support or verify requirements.txt")
    print("="*60 + "\n")
    sys.exit(1)
except Exception as e:
    log_critical_error(e, "Bootstrap")
    print(f"Critical error during bootstrap: {e}")
    sys.exit(1)

def get_static_path():
    # If running as a pyinstaller bundle, check _MEIPASS
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'static')
        
    # Local dev mode (relative to this file)
    # apps/server/bundle_main.py -> ../../apps/web/out
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "../../"))
    return os.path.join(project_root, "apps/web/out")

static_path = get_static_path()

# Mount static files to root
if os.path.exists(static_path):
    print(f"Mounting static files from: {static_path}")
    # html=True allows serving index.html for directories
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")
else:
    print(f"WARNING: Static files not found at {static_path}")

def open_browser():
    # Wait a bit for server to start
    time.sleep(1.5)
    url = f"http://localhost:{settings.API_PORT}"
    print(f"Opening browser at {url}")
    webbrowser.open(url)

def start():
    # Start browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run server
    # Note: reload=False for binary
    uvicorn.run(app, host="0.0.0.0", port=settings.API_PORT, log_level="info")

if __name__ == "__main__":
    try:
        start()
    except Exception as e:
        log_critical_error(e, "Runtime")
        print(f"Runtime error: {e}")
        # 터미널이 바로 꺼지지 않게 잠시 대기
        time.sleep(5)
        sys.exit(1)
