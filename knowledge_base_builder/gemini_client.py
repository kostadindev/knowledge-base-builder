import asyncio
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

class GeminiClient:
    """Asynchronous client for Google's Gemini AI via LangChain."""
    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.0-flash",
        temperature: float = 0.7,
        max_retries: int = 3,
        max_concurrency: int = 8,
    ):
        self.model = ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            api_key=api_key,
        )
        self.max_retries = max_retries
        # Semaphore to cap concurrent requests
        self._sem = asyncio.Semaphore(max_concurrency)

    async def run_async(self, prompt: str) -> str:
        """
        Send prompt to Gemini and return the response.
        Uses retries + exponential backoff.
        """
        start_time = time.time()
        for attempt in range(1, self.max_retries + 1):
            try:
                async with self._sem:
                    result = await self.model.ainvoke([HumanMessage(content=prompt)])
                    end_time = time.time()
                    print(f"    ⏱️ Gemini API call: {end_time - start_time:.2f} seconds")
                    return result.content if hasattr(result, "content") else result
            except Exception as e:
                if attempt == self.max_retries:
                    end_time = time.time()
                    print(f"    ⏱️ Gemini API call failed after {end_time - start_time:.2f} seconds and {attempt} attempts")
                    raise
                # backoff: 2, 4, 8, ...
                backoff_time = 2 ** attempt
                print(f"    ⚠️ Gemini API call attempt {attempt} failed, retrying in {backoff_time} seconds...")
                await asyncio.sleep(backoff_time)

    # Keep a synchronous alias if you still need it elsewhere
    def run(self, prompt: str) -> str:
        start_time = time.time()
        result = asyncio.get_event_loop().run_until_complete(self.run_async(prompt))
        end_time = time.time()
        print(f"    ⏱️ Gemini API call (sync): {end_time - start_time:.2f} seconds")
        return result.content if hasattr(result, "content") else result