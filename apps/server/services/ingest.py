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
            filename = os.path.basename(filepath)
            # 시스템 파일/숨김 파일 무시
            if filename.startswith('.') or filename == '.DS_Store':
                return

            _, ext = os.path.splitext(filepath)
            ext = ext.lower()
            
            # 이미지 처리 (Vision/OCR)
            if ext in ['.png', '.jpg', '.jpeg']:
                logger.info(f"Processing image file: {filepath}")
                from apps.server.services.llm import llm_service
                
                description = llm_service.describe_image(filepath)
                
                meta = {
                    "source": filepath,
                    "filename": filename,
                    "type": "image"
                } 
                
                # 이미지 설명 텍스트를 인덱싱
                rag_engine.add_text(f"[Image Description]\n{description}", meta)
                logger.info(f"Successfully indexed image: {filepath}")

            # URL 파일 처리 (.url)
            elif ext in ['.url']:
                logger.info(f"Processing URL file: {filepath}")
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    target_url = None
                    for line in lines:
                        if line.strip().startswith('URL='):
                            target_url = line.strip().split('=', 1)[1]
                            break
                    
                    if target_url:
                        import requests
                        from bs4 import BeautifulSoup
                        
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
                            "filename": filename,
                            "type": "url_content",
                            "url": target_url
                        }
                        
                        rag_engine.add_text(f"[URL Content: {target_url}]\n{text_content}", meta)
                        logger.info(f"Successfully indexed URL content: {target_url}")
                except Exception as e:
                    logger.error(f"Failed to process URL file {filepath}: {e}")

            # 그 외 모든 파일은 텍스트로 시도 (확장자 없음, .19, .md 등)
            else:
                # 바이너리 확장자 블랙리스트
                if ext in ['.pyc', '.bin', '.exe', '.dll', '.dylib', '.zip', '.tar', '.gz']:
                    return

                try:
                    # UTF-8로 읽기 시도
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    logger.info(f"Processing text file: {filepath}")
                    
                    meta = {
                        "source": filepath,
                        "filename": filename,
                        "type": "text"
                    }
                    
                    rag_engine.add_text(content, meta)
                    logger.info(f"Successfully indexed: {filepath}")
                except UnicodeDecodeError:
                    # 텍스트가 아니면 조용히 무시 (혹은 warning)
                    pass
                except Exception as e:
                    logger.error(f"Failed to read text file {filepath}: {e}")

        except Exception as e:
            logger.error(f"Error processing file {filepath}: {e}")

class IngestionService:
    def __init__(self):
        self.observer = Observer()
        self.handler = IngestHandler()
        self.data_dirs = [
            os.path.join(os.getcwd(), 'data', 'company'),
            os.path.join(os.getcwd(), 'data', 'personal'),
            os.path.join(os.getcwd(), 'data', 'project')
        ]

    def scan_existing_files(self):
        """기존 파일 스캔 및 인덱싱"""
        logger.info("Scanning existing files...")
        count = 0
        for d in self.data_dirs:
            if not os.path.exists(d):
                continue
            for root, _, files in os.walk(d):
                for file in files:
                    filepath = os.path.join(root, file)
                    self.handler.process_file(filepath)
                    count += 1
        logger.info(f"Scanned and processed {count} existing files.")

    def start_watching(self):
        """데이터 폴더 감시 시작"""
        # data 폴더가 없으면 생성
        for d in self.data_dirs:
            if not os.path.exists(d):
                os.makedirs(d, exist_ok=True)
            self.observer.schedule(self.handler, d, recursive=True)
        
        # 시작 시 기존 파일 스캔
        self.scan_existing_files()
        
        self.observer.start()
        logger.info("Ingestion Service started watching data directories.")

    def stop_watching(self):
        self.observer.stop()
        self.observer.join()

ingestion_service = IngestionService()
