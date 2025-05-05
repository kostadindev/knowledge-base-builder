from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

class GeminiClient:
    """Client for interacting with Google's Gemini AI model."""
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash", temperature: float = 0.7):
        self.model = ChatGoogleGenerativeAI(model=model, temperature=temperature, api_key=api_key)

    def run(self, prompt: str) -> str:
        """Run a prompt through the Gemini model."""
        return self.model.invoke([HumanMessage(content=prompt)]).content 