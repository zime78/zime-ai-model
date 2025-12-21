"""
Gunicorn 설정 파일
프로덕션 환경을 위한 워커 및 성능 설정
"""

import multiprocessing
import os

# === 바인딩 설정 ===
bind = f"{os.getenv('API_HOST', '0.0.0.0')}:{os.getenv('API_PORT', '8000')}"

# === 워커 설정 ===
# CPU 코어 수에 따른 자동 스케일링
workers = int(os.getenv('WORKERS_COUNT', multiprocessing.cpu_count() * 2 + 1))
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000

# 워커 재시작 설정 (메모리 누수 방지)
max_requests = 1000
max_requests_jitter = 50

# === 타임아웃 설정 ===
# LLM 응답 대기를 고려한 긴 타임아웃
timeout = int(os.getenv('REQUEST_TIMEOUT', 120))
graceful_timeout = 30
keepalive = 5

# === 로깅 설정 ===
accesslog = "-"  # stdout으로 출력
errorlog = "-"   # stdout으로 출력
loglevel = os.getenv("LOG_LEVEL", "info").lower()
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# === 프로세스 설정 ===
proc_name = "my-brain-api"

# 애플리케이션 프리로드 (메모리 공유)
preload_app = True

# 데몬 모드 비활성화 (Docker/Supervisor 사용 시)
daemon = False

# 현재 디렉토리 유지
chdir = os.getenv('APP_DIR', '/app')
