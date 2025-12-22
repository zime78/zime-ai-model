import os
from langchain_core.documents import Document
from apps.server.core.config import settings

class SimpleRAGEngine:
    """
    ChromaDB 설치 실패 대비용 경량 인메모리 검색 엔진.
    단순 키워드 매칭 기반으로 동작합니다.
    """
    def __init__(self):
        self.documents = []

    def add_text(self, text: str, meta: dict):
        """텍스트를 메모리에 저장"""
        # 단순화를 위해 전체 텍스트를 하나의 문서로 저장
        doc = Document(page_content=text, metadata=meta)
        self.documents.append(doc)
        print(f"[RAG] Indexed document: {meta.get('filename')}")

    def search(self, query: str, k: int = 3):
        """단순 키워드 검색"""
        results = []
        query_terms = query.lower().split()
        
        for doc in self.documents:
            content_lower = doc.page_content.lower()
            score = 0
            for term in query_terms:
                if term in content_lower:
                    score += 1
            
            if score > 0:
                results.append((doc, score))
        
        # 점수순 정렬
        results.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in results[:k]]

    def get_all_documents(self) -> list[str]:
        """현재 인덱싱된 모든 문서의 파일명 목록 반환"""
        filenames = set()
        for doc in self.documents:
            name = doc.metadata.get('filename', 'Unknown')
            filenames.add(name)
        return sorted(list(filenames))

    def get_tree_structure(self) -> str:
        """현재 인덱싱된 파일들의 폴더 구조를 트리 형태 문자열로 반환"""
        import os
        
        # 1. 파일 경로 수집
        file_paths = []
        for doc in self.documents:
            source = doc.metadata.get('source')
            if source:
                file_paths.append(source)
        
        if not file_paths:
            return "No files indexed."

        # 2. 트리 구조 생성
        tree = {}
        for path in file_paths:
            # 'data' 폴더 이후의 경로만 추출 시도
            if 'data/' in path:
                rel_path = path.split('data/', 1)[1]
                parts = rel_path.split(os.sep)
            else:
                # data 폴더가 없으면 파일명만 사용
                parts = [os.path.basename(path)]
            
            current = tree
            for part in parts:
                current = current.setdefault(part, {})

        # 3. 트리 문자열 변환 (재귀)
        def build_tree_str(current_node, prefix=""):
            lines = []
            keys = sorted(current_node.keys())
            for i, key in enumerate(keys):
                is_last = (i == len(keys) - 1)
                connector = "└── " if is_last else "├── "
                lines.append(f"{prefix}{connector}{key}")
                
                next_prefix = prefix + ("    " if is_last else "│   ")
                if current_node[key]: # 하위 노드가 있으면 재귀 호출
                    lines.extend(build_tree_str(current_node[key], next_prefix))
            return lines

        lines = ["data/"] + build_tree_str(tree)
        return "\n".join(lines)

    def get_tree_image(self) -> str:
        """현재 인덱싱된 파일 구조를 이미지(Base64)로 반환"""
        from PIL import Image, ImageDraw, ImageFont
        import base64
        from io import BytesIO

        tree_str = self.get_tree_structure()
        
        # 폰트 설정 (시스템 기본 폰트 시도, 없으면 기본값)
        try:
            # macOS 기본 멘로 폰트 등 시도
            font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
        except:
            font = ImageFont.load_default()

        # 이미지 크기 계산
        lines = tree_str.split('\n')
        max_width = 0
        total_height = 0
        line_height = 20 # 대략적인 줄 높이
        
        # 더 정확한 크기 계산을 위해 임시 이미지 생성
        dummy_img = Image.new('RGB', (1, 1))
        dummy_draw = ImageDraw.Draw(dummy_img)
        
        left, top, right, bottom = dummy_draw.textbbox((0, 0), lines[0], font=font)
        line_height = bottom - top + 4 # 여백 추가
        
        for line in lines:
            left, top, right, bottom = dummy_draw.textbbox((0, 0), line, font=font)
            width = right - left
            max_width = max(max_width, width)
        
        total_height = len(lines) * line_height + 20 # 상하 여백
        max_width += 40 # 좌우 여백

        # 이미지 생성 (검은 배경, 흰 글씨)
        image = Image.new('RGB', (max_width, total_height), color=(30, 30, 30))
        draw = ImageDraw.Draw(image)
        
        y = 10
        for line in lines:
            draw.text((10, y), line, font=font, fill=(200, 200, 200))
            y += line_height
        
        # Base64 변환
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return img_str

# ChromaDB 대신 SimpleRAGEngine 사용
rag_engine = SimpleRAGEngine()
