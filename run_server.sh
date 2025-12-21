#!/bin/bash

# 가상환경 활성화
source .venv/bin/activate

# 서버 실행
# apps.server 패키지로 인식되도록 PYTHONPATH 설정
export PYTHONPATH=$PYTHONPATH:$(pwd)

python apps/server/main.py
