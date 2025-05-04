import os
import requests
import tempfile
import urllib.parse
from typing import List

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import HumanMessage

# === Load .env variables ===
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
GEMINI_TEMPERATURE = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))

# === Minimal Gemini Client ===

class GeminiClient:
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash", temperature: float = 0.7):
        self.model = ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            api_key=api_key
        )

    def run(self, prompt: str) -> str:
        return self.model.invoke([HumanMessage(content=prompt)]).content

# === PDF Utilities ===
def download_pdf(url: str) -> str:
    if url.startswith("file://"):
        parsed = urllib.parse.urlparse(url)
        local_path = urllib.parse.unquote(parsed.path)
        if os.name == 'nt' and local_path.startswith('/'):
            local_path = local_path.lstrip('/')
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Local file not found: {local_path}")
        return local_path
    else:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to download PDF from {url}")
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_file.write(response.content)
        temp_file.close()
        return temp_file.name

def extract_text(pdf_path: str) -> str:
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    return "\n".join(chunk.page_content for chunk in chunks)

# === KB Generation & Merging ===
def build_kb(text: str, gemini: GeminiClient) -> str:
    prompt = f"""You're a helpful assistant.

Turn the following document into a structured **Markdown knowledge base** with summaries, bullet points, and clearly formatted sections.

---DOCUMENT START---
{text}
---DOCUMENT END---

Return only the Markdown."""
    return gemini.run(prompt)

def merge_kbs(kb1: str, kb2: str, gemini: GeminiClient) -> str:
    prompt = f"""Merge the following two Markdown knowledge bases into one logically organized document.

---KB1---
{kb1}
---KB2---
{kb2}

Return only the final Markdown."""
    return gemini.run(prompt)

def recursively_merge_kbs(kbs: List[str], gemini: GeminiClient) -> str:
    while len(kbs) > 1:
        merged = []
        for i in range(0, len(kbs), 2):
            if i + 1 < len(kbs):
                merged_kb = merge_kbs(kbs[i], kbs[i+1], gemini)
                merged.append(merged_kb)
            else:
                merged.append(kbs[i])
        kbs = merged
    return kbs[0]

# === Main ===
def main():
    pdf_urls = [
        "https://kostadindev.github.io/static/documents/cv.pdf",
        "https://kostadindev.github.io/static/documents/sbu_transcript.pdf",
        "file:///C:/Users/kosta/OneDrive/Desktop/MS%20Application%20Materials/emf-ellipse-publication.pdf"
    ]

    gemini = GeminiClient(api_key=GOOGLE_API_KEY, model=GEMINI_MODEL, temperature=GEMINI_TEMPERATURE)

    kbs = []
    for url in pdf_urls:
        try:
            print(f"Processing: {url}")
            path = download_pdf(url)
            text = extract_text(path)
            if not text.strip():
                print(f"Skipping empty document: {url}")
                continue
            kb = build_kb(text, gemini)
            kbs.append(kb)
        except Exception as e:
            print(f"Failed to process {url}: {e}")

    if not kbs:
        print("No knowledge bases created.")
        return

    print("Merging all knowledge bases...")
    final_kb = recursively_merge_kbs(kbs, gemini)

    output_path = "final_knowledge_base.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_kb)

    print(f"✅ Final KB written to: {output_path}")

if __name__ == "__main__":
    main()
