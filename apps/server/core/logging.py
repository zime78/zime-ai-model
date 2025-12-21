"""
구조화된 로깅 설정
JSON 또는 텍스트 포맷으로 로깅을 구성합니다.
"""

import logging
import json
import sys
from datetime import datetime
from typing import Optional

from apps.server.core.config import settings


class JSONFormatter(logging.Formatter):
    """JSON 형식의 로그 포맷터"""

    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # 예외 정보 추가
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)

        # 추가 필드
        if hasattr(record, "extra"):
            log_obj["extra"] = record.extra

        return json.dumps(log_obj, ensure_ascii=False)


class TextFormatter(logging.Formatter):
    """텍스트 형식의 로그 포맷터"""

    def __init__(self):
        super().__init__(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )


def setup_logging(
    level: Optional[str] = None,
    log_format: Optional[str] = None,
) -> None:
    """
    애플리케이션 로깅 설정

    Args:
        level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR)
        log_format: 로그 포맷 (json, text)
    """
    log_level = level or settings.LOG_LEVEL
    fmt = log_format or settings.LOG_FORMAT

    # 루트 로거 설정
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # 기존 핸들러 제거
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # 새 핸들러 설정
    handler = logging.StreamHandler(sys.stdout)

    if fmt == "json":
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(TextFormatter())

    root_logger.addHandler(handler)

    # 에러 로그 파일 설정 (error.txt)
    try:
        file_handler = logging.FileHandler("error.txt", encoding="utf-8")
        file_handler.setLevel(logging.ERROR)
        if fmt == "json":
            file_handler.setFormatter(JSONFormatter())
        else:
            file_handler.setFormatter(TextFormatter())
        root_logger.addHandler(file_handler)
    except Exception:
        pass  # 파일 권한 등으로 실패시 무시

    # 외부 라이브러리 로그 레벨 조정
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("chromadb").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    로거 인스턴스 반환

    Args:
        name: 로거 이름 (보통 __name__ 사용)

    Returns:
        설정된 로거 인스턴스
    """
    return logging.getLogger(name)
