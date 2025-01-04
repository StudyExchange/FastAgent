import asyncio
import hashlib
import os
from typing import Dict, List, Optional

import markdown
import numpy as np
from docx import Document
from lightrag import LightRAG, QueryParam
from lightrag.llm import (
    gpt_4o_complete,
    gpt_4o_mini_complete,
    openai_complete_if_cache,
    openai_embedding,
)
from lightrag.utils import EmbeddingFunc
from tqdm import tqdm

from config import settings


async def llm_model_func(prompt, system_prompt=None, history_messages=[], keyword_extraction=False, **kwargs) -> str:
    return await openai_complete_if_cache(
        settings.openai_model_name,
        prompt,
        system_prompt=system_prompt,
        history_messages=history_messages,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        **kwargs,
    )


async def embedding_func(texts: list[str]) -> np.ndarray:
    return await openai_embedding(
        texts,
        model=settings.openai_embedding_name,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
    )


class RagService:
    def __init__(self, working_dir: str = settings.lightrag_working_dir, docs_dir: str = settings.lightrag_docs_dir):
        self.working_dir = working_dir
        self.docs_dir = docs_dir
        if not os.path.exists(self.docs_dir):
            raise Exception("Can't find folder: %s" % self.docs_dir)
        
        self.client: LightRAG = self.get_client()

    def get_client(self):
        rag = LightRAG(
            working_dir=self.working_dir,
            addon_params={"insert_batch_size": 20},  # Process 20 documents per batch
            llm_model_func=llm_model_func,
            embedding_func=EmbeddingFunc(
                embedding_dim=1536,
                max_token_size=8192,
                func=embedding_func,
            ),
        )
        return rag

    async def load_documents(self):
        os.makedirs(self.docs_dir, exist_ok=True)
        documents = []
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
                documents.append(text)
        if documents:
            res = await self.client.ainsert(documents)

    async def query(self, query_text: str, mode: str = "hybrid") -> Dict:
        res = await self.client.aquery(query_text, param=QueryParam(mode="hybrid"))
        return res


def get_rag_service() -> RagService:
    return RagService()


async def main():
    rag_service = RagService()
    await rag_service.load_documents()
    query_text = "What year was Tesla born?"
    results = await rag_service.query(query_text)
    print("Query Results:", results)


if __name__ == "__main__":
    asyncio.run(main())
