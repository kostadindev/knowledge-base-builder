from typing import List
from knowledge_base_builder.gemini_client import GeminiClient

class LLM:
    """Build and process knowledge bases using Gemini."""
    def __init__(self, gemini_client: GeminiClient):
        self.gemini = gemini_client

    def build_kb(self, text: str) -> str:
        """Build a knowledge base from raw text."""
        prompt = f"""You're a helpful assistant.

Turn the following document into a structured **Markdown knowledge base** with summaries, bullet points, and clearly formatted sections.

---DOCUMENT START---
{text}
---DOCUMENT END---

Return only the Markdown."""
        return self.gemini.run(prompt)

    def merge_kbs(self, kb1: str, kb2: str) -> str:
        """Merge two knowledge bases into one."""
        prompt = f"""Merge the following two Markdown knowledge bases into one logically organized document.

---KB1---
{kb1}
---KB2---

{kb2}
Return only the final Markdown."""
        return self.gemini.run(prompt)

    def recursively_merge_kbs(self, kbs: List[str]) -> str:
        """Recursively merge multiple knowledge bases."""
        while len(kbs) > 1:
            merged = []
            for i in range(0, len(kbs), 2):
                if i + 1 < len(kbs):
                    merged_kb = self.merge_kbs(kbs[i], kbs[i+1])
                    merged.append(merged_kb)
                else:
                    merged.append(kbs[i])
            kbs = merged
        return kbs[0] if kbs else "" 