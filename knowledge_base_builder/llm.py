import asyncio
from typing import List, Tuple
import time

from knowledge_base_builder.llm_client import LLMClient

class LLM:
    """Build and merge KBs via LLM, with async I/O for preprocessing."""
    def __init__(self, llm_client: LLMClient, max_concurrency: int = 8):
        self.llm_client = llm_client
        # A simple semaphore to cap concurrent in-flight requests
        self._sem = asyncio.Semaphore(max_concurrency)

    def build(self, text: str) -> str:
        """Build a single KB chunk synchronously."""
        start_time = time.time()
        prompt = (
            "You're a knowledge base builder.\n\n"
            "Turn the following document into a structured **Markdown knowledge base** "
            "with summaries, bullet points, and clearly formatted sections.\n\n"
            f"---DOCUMENT START---\n{text}\n---DOCUMENT END---\n\n"
            "Return only the Markdown."
        )
        result = self.llm_client.run(prompt)
        end_time = time.time()
        client_name = self.llm_client.__class__.__name__
        print(f"  ⏱️ KB building with {client_name}: {end_time - start_time:.2f} seconds")
        return result

    async def preprocess_text_async(self, text: str) -> str:
        """Preprocess a single text document into a structured KB asynchronously."""
        start_time = time.time()
        prompt = (
            "You're a knowledge base builder.\n\n"
            "Turn the following document into a structured **Markdown knowledge base** "
            "with summaries, bullet points, and clearly formatted sections.\n\n"
            f"---DOCUMENT START---\n{text}\n---DOCUMENT END---\n\n"
            "Return only the Markdown."
        )
        async with self._sem:
            result = await self.llm_client.run_async(prompt)
        end_time = time.time()
        print(f"  ⏱️ Document preprocessing: {end_time - start_time:.2f} seconds")
        return result

    async def merge_all_kbs(self, kbs: List[str]) -> str:
        """Merge all preprocessed KBs into one final document."""
        if not kbs:
            return ""
            
        start_time = time.time()
        prompt = (
            "Merge the following knowledge bases into one logically structured Markdown document.\n\n" +
            "\n\n".join(f"---KB{i+1}---\n{kb}" for i, kb in enumerate(kbs)) +
            "\n\nReturn only the final Markdown."
        )
        async with self._sem:
            result = await self.llm_client.run_async(prompt)
        end_time = time.time()
        print(f"  ⏱️ Final KB merge ({len(kbs)} KBs): {end_time - start_time:.2f} seconds")
        return result

    async def process_documents(self, texts: List[str]) -> str:
        """
        Process multiple documents in two steps:
        1. Preprocess each document into a KB concurrently
        2. Merge all KBs into one final document
        """
        if not texts:
            return ""

        # Step 1: Preprocess all documents concurrently
        print(f"  📑 Preprocessing {len(texts)} documents")
        preprocess_start = time.time()
        tasks = [asyncio.create_task(self.preprocess_text_async(text)) for text in texts]
        preprocessed_kbs = await asyncio.gather(*tasks)
        preprocess_end = time.time()
        print(f"  ⏱️ Preprocessing completed in {preprocess_end - preprocess_start:.2f} seconds")

        # Step 2: Merge all preprocessed KBs into one final document
        print(f"  📑 Merging {len(preprocessed_kbs)} KBs into final document")
        final_kb = await self.merge_all_kbs(preprocessed_kbs)
        
        return final_kb