# 🧠 Multi-Source Knowledge Base Builder for LLMs

This project builds a **textual knowledge base** from various data sources such as PDFs, websites, and GitHub markdown files, using **AI models** to structure and summarize the content. Supports **Google Gemini**, **OpenAI GPT-4o**, and **Anthropic Claude**. The final output is a **Markdown-formatted knowledge base**, ready for use in **RAG pipelines**, chatbots, or any LLM application.

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
# Choose your LLM provider (gemini, openai, or anthropic)
LLM_PROVIDER=gemini

# Google Gemini API Key
GOOGLE_API_KEY=your_google_api_key # Obtain at https://ai.google.dev/gemini-api/docs/api-key

# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key # Obtain at https://platform.openai.com/api-keys

# Anthropic API Key
ANTHROPIC_API_KEY=your_anthropic_api_key # Obtain at https://console.anthropic.com/keys

# GitHub API Key (optional)
GITHUB_API_KEY=your_github_token  # Only required for accounts with many repositories
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
    'files': [
        # All file types are supported through a single list
        "https://example.com/document.pdf",
        "/path/to/local/document.pdf",
        "https://example.com/data.csv",
        "/path/to/local/document.docx",
        "https://example.com/page1.html",
        "https://example.com/data.json",
        "https://example.com/"  # Regular web pages are also supported
    ],
    # 'sitemap_url': "https://example.com/sitemap.xml"
}

# Create KB builder
kbb = KBBuilder(config)

# Build knowledge base
kbb.build_kb(sources=sources, output_file="final_knowledge_base.md")
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

## 📌 Example Usage

### Basic Usage
Run the CLI tool to process sources with your preferred LLM:

```bash
# Using Google Gemini (default)
python -m knowledge_base_builder.cli --llm-provider gemini --file "https://example.com/document.pdf" --output kb.md

# Using OpenAI GPT-4o
python -m knowledge_base_builder.cli --llm-provider openai --file "/path/to/document.docx" --output kb.md

# Using Anthropic Claude
python -m knowledge_base_builder.cli --llm-provider anthropic --file "https://example.com/page.html" --output kb.md
```

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
- [x] Add support for other large language models (GPT-4o, Claude 3.7)
- [ ] Add support for other data sources (Google Drive, LinkedIn)
- [ ] Support knowledge base to vector DB (e.g., Pinecone, Chroma)
- [ ] Create configuration file for easier customization
- [ ] Implement additional async processing for better performance

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

MIT © [Kostadin Devedzhiev](https://github.com/kostadindev)
