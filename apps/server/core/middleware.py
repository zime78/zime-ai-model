"""
FastAPI 미들웨어 모듈
요청 타이밍, 로깅 등의 미들웨어를 제공합니다.
"""

import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class RequestTimingMiddleware(BaseHTTPMiddleware):
    """
    요청 처리 시간을 측정하고 로깅하는 미들웨어
    응답 헤더에 X-Process-Time 추가
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.3f}"

        # 요청 로깅 (헬스체크 제외)
        if not request.url.path.startswith("/health"):
            logger.info(
                f"{request.method} {request.url.path} "
                f"status={response.status_code} duration={process_time:.3f}s"
            )

        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    요청/응답 상세 로깅 미들웨어 (디버그용)
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        # 요청 정보 로깅
        logger.debug(
            f"Request: {request.method} {request.url} "
            f"client={request.client.host if request.client else 'unknown'}"
        )

        response = await call_next(request)

        # 응답 정보 로깅
        logger.debug(
            f"Response: status={response.status_code} "
            f"content-type={response.headers.get('content-type', 'unknown')}"
        )

        return response
