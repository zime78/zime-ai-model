import os
import sys

# 프로젝트 루트를 path에 추가 (앱 실행 환경 모사)
current_dir = os.getcwd()
sys.path.append(current_dir)

from apps.server.services.ingest import ingestion_service, rag_engine
from apps.server.services.ingest import logger
import logging

# 로깅 설정 (Console 출력 온전하게)
logging.basicConfig(level=logging.INFO)

def debug_rag():
    target_file = "dist/data/company/Q앱버전관리/3.0.19"
    abs_path = os.path.abspath(target_file)
    
    print(f"Checking file: {abs_path}")
    if not os.path.exists(abs_path):
        print("File not found!")
        return

    print("Running process_file...")
    # 강제로 파일 처리 호출
    ingestion_service.handler.process_file(abs_path)
    
    print("\nChecking RAG Engine state...")
    print(f"Total documents: {len(rag_engine.documents)}")
    
    # 검색 테스트
    query = "SADM-501"
    print(f"\nSearching for '{query}'...")
    results = rag_engine.search(query)
    
    if results:
        print("Found results:")
        for doc in results:
            print(f"- {doc.metadata['filename']}")
            print(f"Preview: {doc.page_content[:100]}...")
    else:
        print("No results found.")

if __name__ == "__main__":
    debug_rag()
