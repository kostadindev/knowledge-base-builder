# 🧠 Multi-Source Knowledge Base Builder for LLMs

This project builds a **textual knowledge base** from various data sources such as PDFs, websites, and GitHub markdown files, using **Google Gemini models** to structure and summarize the content. The final output is a **Markdown-formatted knowledge base**, ready for use in **RAG pipelines**, chatbots, or any LLM application.

---

## ✨ Features

- 📄 **PDF ingestion** – Downloads local or remote PDFs and extracts structured text.
- 🌐 **Website ingestion** – Crawls pages from a sitemap or list of pages and extracts clean HTML content.
- 📘 **GitHub integration**  – Fetches Markdown files from public repositories.
- 🧠 **LLM-powered summarization** – Uses Gemini to convert raw data into readable, structured Markdown.
- 🔁 **Recursive merging** – Combines multiple knowledge base sections into a single cohesive document.

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

Create a `.env` file in your project directory with the following variables:

```env
GOOGLE_API_KEY=your_google_api_key # Required

GITHUB_USERNAME=your_github_username # Optional if you want to include Github repositories as file sources.
GITHUB_API_KEY=your_github_token  # Optional (only required for accounts with a large number of repositories 50+)
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
    'GOOGLE_API_KEY': os.getenv("GOOGLE_API_KEY"),
}

# Source documents - NEW unified approach
sources = {
    'files': [
        # All file types are now supported through a single list
        "https://example.com/document.pdf",
        "file:///path/to/local/document.pdf",
        "https://example.com/data.csv",
        "file:///path/to/local/document.docx",
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

Example `sources.json` file:
```json
{
  "files": [
    "https://example.com/document.pdf",
    "file:///path/to/local/document.docx",
    "https://example.com/data.xlsx", 
    "https://example.com/api-docs.json",
    "https://example.com/page1.html"
  ],
  "sitemap_url": "https://example.com/sitemap.xml"
}
```

> **Note**: The legacy format with separate lists (`pdf_urls`, `web_urls`, etc.) is still supported for backward compatibility, but the new unified `files` approach is recommended.

---


### File Structure:

```
.
├── construct_kb.py         # Main script
├── gemini_client.py        # Gemini API client
├── kb_app.py               # Main application class
├── llm.py           # Knowledge base building utility
├── pdf_processor.py        # PDF processing utility
├── website_processor.py    # Website processing utility
├── github_processor.py     # GitHub processing utility
├── __init__.py             # Package initialization
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
└── test_llm.py      # Test script
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

## 🧠 Gemini Prompt Strategy

- Summarizes content into Markdown using **sections**, **bullet points**, and **clear formatting**.
- Merges summaries recursively in pairs to ensure **contextual cohesion**.

---

## 📌 Example Usage

### Basic Usage
Run the main script to process all configured sources:
```bash
python -m knowledge_base_builder.cli --file "https://example.com/document.pdf" --file "file:///path/to/document.docx" --output kb.md
```

Or use a sources file:
```bash
python -m knowledge_base_builder.cli --sources-file sources.json --output kb.md
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

## 🧪 TODOs & Enhancements

- [x] Add support for other document types (.docx, .txt, .md, .rtf)
- [x] Add support for spreadsheet data (.csv, .tsv, .xlsx, .ods) 
- [x] Add support for web content formats (.html, .xml, .json, .yaml)
- [ ] Add support for other data sources (Google Drive, LinkedIn)
- [ ] Add support for other large language models (GPT4o, Claude 3.7)
- [ ] Support knowledge base to vector DB (e.g., Pinecone, Chroma)
- [ ] Create configuration file for easier customization
- [ ] Implement async processing for better performance

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

MIT © [Kostadin Devedzhiev](https://github.com/kostadindev)
