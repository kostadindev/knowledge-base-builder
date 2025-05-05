import asyncio
from typing import List, Tuple
import time

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

from knowledge_base_builder.gemini_client import GeminiClient

class LLM:
    """Build and merge KBs via Gemini, with async I/O for merges."""
    def __init__(self, gemini_client: GeminiClient):
        self.gemini = gemini_client

    def build_kb(self, text: str) -> str:
        """Build a single KB chunk synchronously."""
        start_time = time.time()
        prompt = (
            "You're a helpful assistant.\n\n"
            "Turn the following document into a structured **Markdown knowledge base** "
            "with summaries, bullet points, and clearly formatted sections.\n\n"
            f"---DOCUMENT START---\n{text}\n---DOCUMENT END---\n\n"
            "Return only the Markdown."
        )
        result = self.gemini.run(prompt)
        end_time = time.time()
        print(f"  ⏱️ KB building with Gemini: {end_time - start_time:.2f} seconds")
        return result

    async def merge_pair_async(self, kb1: str, kb2: str) -> str:
        """Async merge of two Markdown KBs."""
        start_time = time.time()
        prompt = (
            "Merge the following two Markdown knowledge bases into one logically organized document.\n\n"
            f"---KB1---\n{kb1}\n\n---KB2---\n{kb2}\n\n"
            "Return only the final Markdown."
        )
        result = await self.gemini.run_async(prompt)
        end_time = time.time()
        print(f"  ⏱️ KB pair merging: {end_time - start_time:.2f} seconds")
        return result

    async def recursively_merge_kbs(self, kbs: List[str]) -> str:
        """
        Recursively merge a list of KBs using async gather.
        Runs in O(log N) rounds, merging all pairs each round.
        """
        if not kbs:
            return ""
        
        round_num = 0
        while len(kbs) > 1:
            round_num += 1
            print(f"  📑 Merge round {round_num}: {len(kbs)} knowledge bases remaining")
            round_start = time.time()
            
            # pair them up
            pairs = [(kbs[i], kbs[i+1]) for i in range(0, len(kbs)//2*2, 2)]
            leftover = kbs[len(pairs)*2:]  # odd one out
            
            # fire all merges concurrently
            tasks = [asyncio.create_task(self.merge_pair_async(a, b)) for a, b in pairs]
            merged = await asyncio.gather(*tasks)
            kbs = merged + leftover
            
            round_end = time.time()
            print(f"  ⏱️ Merge round {round_num} completed in {round_end - round_start:.2f} seconds")
        
        return kbs[0]
    """
    Build and merge Markdown KBs asynchronously.
    """

    def __init__(self, gemini_client: GeminiClient, max_concurrency: int = 8):
        self.gemini = gemini_client
        # A simple semaphore to cap concurrent in-flight requests
        self._sem = asyncio.Semaphore(max_concurrency)

    async def merge_pair_async(self, kb1: str, kb2: str) -> str:
        """Merge two Markdown KBs into one via Gemini."""
        start_time = time.time()
        prompt = (
            "Merge the following two Markdown knowledge bases into one logically organized document.\n\n"
            f"---KB1---\n{kb1}\n\n---KB2---\n{kb2}\n\n"
            "Return only the final Markdown."
        )
        # bound concurrency
        async with self._sem:
            result = await self.gemini.run_async(prompt)
        end_time = time.time()
        print(f"  ⏱️ KB pair merging: {end_time - start_time:.2f} seconds")
        return result

    async def recursively_merge_kbs_async(self, kbs: List[str]) -> str:
        """
        Recursively merge a list of KBs using async gather.
        Runs in O(log N) rounds, merging all pairs each round.
        """
        if not kbs:
            return ""

        round_num = 0
        # Keep merging until one remains
        while len(kbs) > 1:
            round_num += 1
            print(f"  📑 Merge round {round_num}: {len(kbs)} knowledge bases remaining")
            round_start = time.time()
            
            # Pair up for merging
            pairs: List[Tuple[str, str]] = [
                (kbs[i], kbs[i+1]) for i in range(0, len(kbs) // 2 * 2, 2)
            ]
            leftover = kbs[len(pairs) * 2 :]  # odd one out, if any

            # Launch all merge tasks concurrently
            tasks = [
                asyncio.create_task(self.merge_pair_async(a, b))
                for a, b in pairs
            ]

            # Wait for all to complete (exceptions will propagate)
            merged_results = await asyncio.gather(*tasks)

            # Build new round list, preserving original left-to-right
            kbs = [*merged_results, *leftover]
            
            round_end = time.time()
            print(f"  ⏱️ Merge round {round_num} completed in {round_end - round_start:.2f} seconds")

        return kbs[0]