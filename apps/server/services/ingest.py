import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from apps.server.services.rag import rag_engine
from apps.server.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IngestHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

    def process_file(self, filepath: str):
        try:
            _, ext = os.path.splitext(filepath)
            ext = ext.lower()
            
            # 텍스트 기반 파일 처리
            if ext in ['.md', '.txt']:
                logger.info(f"Processing text file: {filepath}")
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 메타데이터 생성
                meta = {
                    "source": filepath,
                    "filename": os.path.basename(filepath),
                    "type": "text"
                }
                
                # RAG 엔진에 추가
                rag_engine.add_text(content, meta)
                logger.info(f"Successfully indexed: {filepath}")
            
            # 이미지 처리 (Vision/OCR)
            elif ext in ['.png', '.jpg', '.jpeg']:
                logger.info(f"Processing image file: {filepath}")
                from apps.server.services.llm import llm_service
                
                description = llm_service.describe_image(filepath)
                
                meta = {
                    "source": filepath,
                    "filename": os.path.basename(filepath),
                    "type": "image"
                } 
                
                # 이미지 설명 텍스트를 인덱싱
                rag_engine.add_text(f"[Image Description]\n{description}", meta)
                logger.info(f"Successfully indexed image: {filepath}")

            # URL 파일 처리 (.url)
            elif ext in ['.url']:
                logger.info(f"Processing URL file: {filepath}")
                with open(filepath, 'r') as f:
                    lines = f.readlines()
                
                target_url = None
                for line in lines:
                    if line.strip().startswith('URL='):
                        target_url = line.strip().split('=', 1)[1]
                        break
                
                if target_url:
                    import requests
                    from bs4 import BeautifulSoup
                    
                    try:
                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                        resp = requests.get(target_url, headers=headers, timeout=10)
                        resp.raise_for_status()
                        soup = BeautifulSoup(resp.text, 'html.parser')
                        
                        # script/style 제거
                        for script in soup(["script", "style"]):
                            script.decompose()
                            
                        text_content = soup.get_text(separator=' ', strip=True)
                        
                        meta = {
                            "source": filepath,
                            "filename": os.path.basename(filepath),
                            "type": "url_content",
                            "url": target_url
                        }
                        
                        rag_engine.add_text(f"[URL Content: {target_url}]\n{text_content}", meta)
                        logger.info(f"Successfully indexed URL content: {target_url}")
                    except Exception as e:
                        logger.error(f"Failed to fetch URL {target_url}: {e}")

        except Exception as e:
            logger.error(f"Error processing file {filepath}: {e}")

class IngestionService:
    def __init__(self):
        self.observer = Observer()
        self.handler = IngestHandler()

    def start_watching(self):
        """데이터 폴더 감시 시작"""
        # data 폴더가 없으면 생성
        data_dirs = [
            os.path.join(os.getcwd(), 'data', 'company'),
            os.path.join(os.getcwd(), 'data', 'personal'),
            os.path.join(os.getcwd(), 'data', 'project')
        ]
        
        for d in data_dirs:
            if not os.path.exists(d):
                os.makedirs(d, exist_ok=True)
            self.observer.schedule(self.handler, d, recursive=True)
        
        self.observer.start()
        logger.info("Ingestion Service started watching data directories.")

    def stop_watching(self):
        self.observer.stop()
        self.observer.join()

ingestion_service = IngestionService()
