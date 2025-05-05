# 🧠 Multi-Source Knowledge Base Builder for LLMs

This project builds a web crawlable **textual knowledge base** from various data sources such as PDFs, websites, and GitHub markdown files, using **large language models** to structure and summarize the content. The final output is a **Markdown-formatted knowledge base**, ready for use as an llms.txt or llms-full.txt format. It can also be used in **RAG pipelines** and chatbots. Supports **Google Gemini**, **OpenAI GPT-4o**, and **Anthropic Claude**. The algorithm uses a logarithmic-depth parallel merge tree with a concurrency-limited semaphore to efficiently process and merge all documents.

---

## ✨ Features

- 📄 **Document ingestion** – Downloads local or remote documents and extracts structured text.
- 🌐 **Website ingestion** – Crawls pages from a sitemap or list of pages and extracts clean HTML content.
- 📘 **GitHub integration**  – Fetches Markdown files from public repositories.
- 🧠 **LLM-powered summarization** – Uses state-of-the-art models to convert raw data into readable, structured Markdown.
- 🔁 **Recursive merging** – Combines multiple knowledge base sections into a single cohesive document.
- 🔄 **Multiple model providers** – Choose between Google Gemini, OpenAI GPT-4o, or Anthropic Claude 3.7 Sonnet.
- ⚡ **Performance** – Load files in parallel and make multiple asynchronous calls to LLMs to summarize documents.

---

## 🚀 Installation

### Install from PyPI

```bash
pip install knowledge-base-builder
```

### Install from Source

```bash
git clone https://github.com/kostadindev/knowledge-base-builder.git
cd knowledge-base-builder
pip install -e .
```

---

## 🚀 Quickstart

### 1. Set up your `.env` file

Create a `.env` file in your project directory with the following variables (add the API keys for the models you intend to use):

```env

# You need only one of the following
GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional if you want to include Github repositories with a high rate limit
GITHUB_API_KEY=your_github_api_key_here 
```

### 2. Use as a Python Package

```python
import os
from dotenv import load_dotenv
from knowledge_base_builder import KBBuilder

# Load environment variables
load_dotenv()

# API and model configuration
config = {
    'LLM_PROVIDER': 'gemini',  # Choose: 'gemini', 'openai', or 'anthropic'
    'GOOGLE_API_KEY': os.getenv("GOOGLE_API_KEY"),     # For Gemini
    'OPENAI_API_KEY': os.getenv("OPENAI_API_KEY"),     # For GPT-4o
    'ANTHROPIC_API_KEY': os.getenv("ANTHROPIC_API_KEY"), # For Claude
}

# Source documents - unified approach
    sources = {
        # Unified files list - automatically detects and processes each file type
        'files': [
            # PDF documents - remote
            "https://kostadindev.github.io/static/documents/cv.pdf",
            "https://kostadindev.github.io/static/documents/sbu_transcript.pdf",
            # Local file path (no need for file:/// prefix)
            "C:/Users/kosta/OneDrive/Desktop/MS Application Materials/emf-ellipse-publication.pdf",
            
            # Web pages
            "https://kostadindev.github.io/index.html",
            "https://kostadindev.github.io/projects.html",
            
            # Add other file types as needed
            # "https://example.com/data.csv",
            # "path/to/local/document.docx",  # Relative local path example
            # "https://example.com/api-docs.json",
        ],
        
        # Process all pages from a sitemap
        'sitemap_url': "https://kostadindev.github.io/sitemap.xml",
        
        # GitHub repositories to process (format: username/repo or full URL)
        'github_repositories': [
            "https://github.com/kostadindev/Knowledge-Base-Builder",
            "https://github.com/kostadindev/GONEXT",
            "https://github.com/kostadindev/GONEXT-ML",
            "https://github.com/kostadindev/meta-me",
            "https://github.com/kostadindev/Recursive-QA",
            "https://github.com/kostadindev/deep-gestures",
            "https://github.com/kostadindev/emf-ellipse"
        ]
    }
# Create KB builder
kbb = KBBuilder(config)

# Build knowledge base
kbb.build(sources=sources, output_file="final_knowledge_base.md")
```

---

## 🔧 Supported Sources

| Source Type | Description | Formats |
|-------------|-------------|---------|
| Documents | Text documents | PDF, DOCX, TXT, MD, RTF |
| Spreadsheets | Tabular data | CSV, TSV, XLSX, ODS |
| Web Content | Structured web data | HTML, XML, JSON, YAML/YML |
| Websites | Live web pages | Any URL or sitemap |
| GitHub | Repository content | Markdown files from public repos |

> All sources can now be added through the unified `files` parameter, with automatic format detection.

---

## 🧠 LLM Providers

| Provider | Models | Features |
|----------|--------|----------|
| Google Gemini | gemini-2.0-flash (default) | Fast, cost-effective summaries |
| OpenAI | gpt-4o (default) | High-quality summaries, strong reasoning |
| Anthropic | claude-3-7-sonnet (default) | High-quality summaries, excellent formatting |

---

## 📥 Output Example

```markdown
# Resume Summary

## Education
- B.S. in Computer Science from XYZ University

## Experience
- Software Engineer at ABC Corp
- Developed NLP-based document parsers...

---

# Website Summary

## Project Pages
- **Project Alpha**: A machine learning system for ...
- **Blog Post**: How to use Gemini with LangChain ...
```

---

## 🧪 Upcoming Enhancements
- [ ] Add support for other data sources (Google Drive, LinkedIn)
- [ ] Support conversion from knowledge base to vector DB (e.g., Pinecone, Chroma)
- [ ] Implement additional async processing for better performance
- [ ] Improve performance of the logarithmic-depth parallel merge tree with a concurrency-limited semaphore

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

MIT © [Kostadin Devedzhiev](https://github.com/kostadindev)
