import traceback
import sys
from datetime import datetime

def log_critical_error(e: Exception, context: str = "System"):
    """
    치명적인 에러를 error.txt 파일에 기록합니다.
    로깅 시스템이 초기화되기 전이나 붕괴되었을 때 사용합니다.
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("error.txt", "a", encoding="utf-8") as f:
            f.write(f"\n[{timestamp}] [CRITICAL] {context} Error:\n")
            f.write(f"{str(e)}\n")
            f.write(traceback.format_exc())
            f.write("="*60 + "\n")
    except Exception:
        # 이 함수 자체가 실패하면 할 수 있는 게 거의 없음 (stderr 출력 정도)
        print(f"Failed to write to error.txt: {e}", file=sys.stderr)
