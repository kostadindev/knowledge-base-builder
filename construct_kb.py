import os
import requests
import tempfile
import urllib.parse
import hashlib
from typing import List
from bs4 import BeautifulSoup
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
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "kostadindev")
GITHUB_TOKEN = os.getenv("GITHUB_API_KEY")

# === Gemini Client ===
class GeminiClient:
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash", temperature: float = 0.7):
        self.model = ChatGoogleGenerativeAI(model=model, temperature=temperature, api_key=api_key)

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
    splitter = RecursiveCharacterTextSplitter(chunk_size=20000, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    return "\n".join(chunk.page_content for chunk in chunks)

# === Website Utilities ===
def get_urls_from_sitemap(sitemap_url: str) -> List[str]:
    response = requests.get(sitemap_url)
    if response.status_code != 200:
        raise Exception(f"Failed to load sitemap: {response.status_code}")
    soup = BeautifulSoup(response.text, "xml")
    return [loc.text for loc in soup.find_all("loc")]

def download_and_clean_html(url: str) -> str:
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download HTML: {response.status_code}")
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)

# === GitHub Utilities ===
def get_github_markdown_urls(username: str, token: str = None) -> List[str]:
    headers = {"Authorization": f"token {token}"} if token else {}

    def get_user_repos():
        repos = []
        page = 1
        while True:
            url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
            res = requests.get(url, headers=headers)
            if res.status_code != 200:
                raise Exception(f"GitHub API error: {res.status_code}")
            data = res.json()
            if not data:
                break
            repos.extend(repo['name'] for repo in data)
            page += 1
        return repos

    def get_repo_md_files(repo):
        def recurse(path=""):
            url = f"https://api.github.com/repos/{username}/{repo}/contents/{path}"
            res = requests.get(url, headers=headers)
            if res.status_code != 200:
                return []
            contents = res.json()
            files = []
            for item in contents:
                if item['type'] == 'file' and item['name'].endswith('.md'):
                    files.append(item['download_url'])
                elif item['type'] == 'dir':
                    files.extend(recurse(item['path']))
            return files
        return recurse()

    urls = []
    for repo in get_user_repos():
        print(f"🔍 Scanning repo: {repo}")
        urls.extend(get_repo_md_files(repo))
    return urls

def download_markdown(url: str) -> str:
    res = requests.get(url)
    if res.status_code != 200:
        raise Exception(f"Failed to fetch markdown from: {url}")
    return res.text

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
    # === Inputs ===
    pdf_urls = [
        "https://kostadindev.github.io/static/documents/cv.pdf",
        "https://kostadindev.github.io/static/documents/sbu_transcript.pdf",
        "file:///C:/Users/kosta/OneDrive/Desktop/MS%20Application%20Materials/emf-ellipse-publication.pdf"
    ]
    sitemap_url = "https://kostadindev.github.io/sitemap.xml"

    gemini = GeminiClient(api_key=GOOGLE_API_KEY, model=GEMINI_MODEL, temperature=GEMINI_TEMPERATURE)
    kbs = []

    # PDFs
    for url in pdf_urls:
        try:
            print(f"📄 PDF: {url}")
            path = download_pdf(url)
            text = extract_text(path)
            if not text.strip():
                continue
            kbs.append(build_kb(text, gemini))
        except Exception as e:
            print(f"❌ PDF error: {e}")

    # Websites
    try:
        print(f"🌐 Sitemap: {sitemap_url}")
        urls = get_urls_from_sitemap(sitemap_url)
        for url in urls:
            try:
                print(f"🔗 Website: {url}")
                text = download_and_clean_html(url)
                if text.strip():
                    kbs.append(build_kb(text, gemini))
            except Exception as e:
                print(f"❌ Site error: {e}")
    except Exception as e:
        print(f"❌ Sitemap load error: {e}")

    # # GitHub
    # try:
    #     md_urls = get_github_markdown_urls(GITHUB_USERNAME, GITHUB_TOKEN)
    #     for url in md_urls:
    #         try:
    #             print(f"📘 GitHub MD: {url}")
    #             text = download_markdown(url)
    #             if text.strip():
    #                 kbs.append(build_kb(text, gemini))
    #         except Exception as e:
    #             print(f"❌ GitHub MD error: {e}")
    # except Exception as e:
    #     print(f"❌ GitHub fetch error: {e}")

    if not kbs:
        print("⚠️ No knowledge bases created.")
        return

    print("🔀 Merging all knowledge bases...")
    final_kb = recursively_merge_kbs(kbs, gemini)

    output_path = "final_knowledge_base.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_kb)

    print(f"✅ Final KB written to: {output_path}")

if __name__ == "__main__":
    main()
