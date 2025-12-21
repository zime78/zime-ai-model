#!/bin/bash

# 에러 발생 시 중단
set -e

echo "Stopping running instances..."
# 기존 프로세스 종료 (오류 무시)
killall MyBrainAI 2>/dev/null || true

echo "Cleaning previous builds..."
rm -rf build dist

echo "Running PyInstaller..."
# 가상환경 활성화 (필요시)
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

pyinstaller build_mac.spec --noconfirm --clean

echo "Fixing LaunchServices logic (PkgInfo)..."
if [ ! -f "dist/MyBrainAI.app/Contents/PkgInfo" ]; then
    echo -n "APPL????" > dist/MyBrainAI.app/Contents/PkgInfo
    echo "Created PkgInfo."
fi

echo "Clearing quarantine attributes..."
xattr -rc dist/MyBrainAI.app

# LaunchServices 등록을 위해 앱 실행 권한 및 메타데이터 갱신
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f dist/MyBrainAI.app

echo "Copying data folder to dist..."
# 원본 데이터 폴더가 존재하면 dist/data로 복사
if [ -d "data" ]; then
    cp -r data dist/data
    echo "Data folder copied."
else
    echo "Warning: 'data' folder not found in project root."
fi

echo "Build Complete!"
echo "Run using: open dist/MyBrainAI.app"
