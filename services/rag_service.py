import hashlib
import os
from typing import Dict, List, Optional

import chromadb
import markdown
from docx import Document
from tqdm import tqdm


class RagService:
    def __init__(self, collection_name: str = "rag_collection", persist_directory: str = "chroma_db", docs_dir: str = "./tests/assets/rag_docs"):
        self.docs_dir = docs_dir
        if not os.path.exists(self.docs_dir):
            os.makedirs(self.docs_dir)
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})

    def calculate_md5(self, text: str) -> str:
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    def load_documents(self, chunk_size: int = 512, chunk_overlap: int = 20, batch_size: int = 10):
        documents = []
        ids = []
        metadatas = []

        for file_name in tqdm(os.listdir(self.docs_dir), desc="Loading documents"):
            file_path = os.path.join(self.docs_dir, file_name)
            if os.path.isfile(file_path):
                if file_name.endswith(".txt"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        text = f.read()
                elif file_name.endswith(".md"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        text = markdown.markdown(f.read())
                elif file_name.endswith(".docx"):
                    doc = Document(file_path)
                    text = "\n".join([para.text for para in doc.paragraphs])
                else:
                    continue

                current_md5 = self.calculate_md5(text)
                existing_docs = self.collection.get(where={"source": file_name})
                if existing_docs and len(existing_docs["ids"]) > 0:
                    existing_md5 = existing_docs["metadatas"][0].get("md5")
                    if existing_md5 == current_md5:
                        print("existing_md5 and skip: %s" % file_name)
                        continue
                    else:
                        print("existing_md5 but change, will delete: %s" % file_name)
                        self.collection.delete(where={"source": file_name})
                chunks = self._split_text_into_chunks(text, chunk_size, chunk_overlap)
                documents.extend(chunks)
                ids.extend([f"{file_name}_chunk_{i}" for i in range(len(chunks))])
                metadatas.extend([{"source": file_name, "md5": current_md5}] * len(chunks))
        if documents:
            for i in tqdm(range(0, len(documents), batch_size), desc="Adding documents to ChromaDB"):
                batch_documents = documents[i : i + batch_size]
                batch_ids = ids[i : i + batch_size]
                batch_metadatas = metadatas[i : i + batch_size]
                self.collection.add(documents=batch_documents, ids=batch_ids, metadatas=batch_metadatas)

    def _split_text_into_chunks(self, text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end - chunk_overlap
        return chunks

    def query(self, query_text: str, n_results: int = 5) -> Dict:
        results = self.collection.query(query_texts=[query_text], n_results=n_results)
        return results


def get_rag_service() -> RagService:
    return RagService()


if __name__ == "__main__":
    rag_service = RagService()
    rag_service.load_documents()
    query_text = "What year was Tesla born?"
    results = rag_service.query(query_text)
    print("Query Results:", results)
