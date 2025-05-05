import asyncio
from typing import List, Tuple
import time

from knowledge_base_builder.llm_client import LLMClient

class LLM:
    """Build and merge KBs via LLM, with async I/O for merges."""
    def __init__(self, llm_client: LLMClient, max_concurrency: int = 8):
        self.llm_client = llm_client
        # A simple semaphore to cap concurrent in-flight requests
        self._sem = asyncio.Semaphore(max_concurrency)

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
        result = self.llm_client.run(prompt)
        end_time = time.time()
        client_name = self.llm_client.__class__.__name__
        print(f"  ⏱️ KB building with {client_name}: {end_time - start_time:.2f} seconds")
        return result

    async def merge_pair_async(self, kb1: str, kb2: str) -> str:
        """Async merge of two Markdown KBs."""
        start_time = time.time()
        prompt = (
            "Merge the following two Markdown knowledge bases into one logically organized document.\n\n"
            f"---KB1---\n{kb1}\n\n---KB2---\n{kb2}\n\n"
            "Return only the final Markdown."
        )
        # bound concurrency
        async with self._sem:
            result = await self.llm_client.run_async(prompt)
        end_time = time.time()
        print(f"  ⏱️ KB pair merging: {end_time - start_time:.2f} seconds")
        return result
    
    async def merge_group_async(self, group: List[str]) -> str:
        """Merge a group of Markdown KBs into one via LLM."""
        start_time = time.time()
        prompt = (
            "Merge the following knowledge bases into one logically structured Markdown document.\n\n" +
            "\n\n".join(f"---KB{i+1}---\n{kb}" for i, kb in enumerate(group)) +
            "\n\nReturn only the final Markdown."
        )
        async with self._sem:
            result = await self.llm_client.run_async(prompt)
        end_time = time.time()
        print(f"  ⏱️ KB group merge ({len(group)} KBs): {end_time - start_time:.2f} seconds")
        return result

    async def recursively_merge_kbs(self, kbs: List[str], group_size: int = 2) -> str:
        """
        Recursively merge a list of KBs using async gather.
        Merges groups of `group_size` at each level to reduce total rounds.
        """
        if not kbs:
            return ""

        round_num = 0
        while len(kbs) > 1:
            round_num += 1
            print(f"  📑 Merge round {round_num}: {len(kbs)} KBs to merge with group size {group_size}")
            round_start = time.time()

            # Form groups of group_size
            groups = [kbs[i:i + group_size] for i in range(0, len(kbs), group_size)]

            # Launch all merge tasks concurrently
            tasks = [asyncio.create_task(self.merge_group_async(group)) for group in groups]
            kbs = await asyncio.gather(*tasks)

            round_end = time.time()
            print(f"  ⏱️ Round {round_num} finished in {round_end - round_start:.2f} seconds")

        return kbs[0]