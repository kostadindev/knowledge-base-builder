# 🧠 Multi-Source Knowledge Base Builder for LLMs

Python package to transform diverse content into a powerful, structured knowledge base. This tool seamlessly ingests **files** (PDFs, DOCXs, spreadsheets, Markdown, plaintext), **websites** (HTML pages, sitemaps, XML content), and **GitHub repositories**, processes them with state-of-the-art **large language models** (Gemini, GPT-4o, Claude), and produces a comprehensive **Markdown knowledge base**. Perfect for creating web-crawlable `/llms.txt` files, powering **RAG applications**, preprocessing content for **vector databases**, or building specialized chatbots. The algorithm uses a logarithmic-depth parallel merge tree with a concurrency-limited semaphore to efficiently process and merge all documents.

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

## 🔍 Applications


### Web Crawlable LLM Context Enhancement
- **/llms.txt**: Generate a compact, web-crawlable context file (typically 10-20KB) that allows LLMs to access your personal or organizational information during web searches.
- **/llms-full.txt**: Create an expanded knowledge file (50-100KB) with comprehensive details about your work, expertise, and content that search-powered LLMs can index.
- **Web Context Sources**: Enable web search LLMs like Perplexity, ChatGPT, Claude, and Gemini to discover and reference your structured information during user queries.

### RAG Applications
- **Vector Database Preprocessing**: Generate clean, structured content before embedding into vector stores like Pinecone, Chroma, or Weaviate, improving retrieval quality.
- **Single-Context LLM Applications**: Provide a comprehensive knowledge base that fits within a single LLM context window (up to 128K tokens) for domain-specific assistants.
- **Hybrid RAG Systems**: Combine the full knowledge base with selective vector retrieval for specialized question answering systems with reduced hallucination.

### Personal Knowledge Management
- **Professional Portfolio**: Create a comprehensive knowledge base integrating your resume, publications, projects, and online presence into a single searchable document.
- **Academic Research**: Compile research papers, conference proceedings, and citations into a structured knowledge base for literature reviews or thesis preparation.
- **Technical Documentation**: Consolidate documentation across multiple GitHub repositories, technical blogs, and API references into a unified technical manual.

### Enterprise Use Cases
- **Company Knowledge Base**: Consolidate internal documentation, product specifications, and team information into an easily updatable central resource.
- **Customer Support**: Transform support tickets, FAQs, and product manuals into a comprehensive knowledge base for support agents or automated systems.
- **Competitive Intelligence**: Build a structured repository of competitor information from various public sources, updated periodically with the latest data.
- **Candidate Evaluation**: Generate comprehensive profiles of job candidates by compiling their GitHub contributions, research papers, portfolio, and online presence.
- **Onboarding Acceleration**: Create personalized knowledge bases for new employees containing company policies, codebase documentation, and team information.

---

## 🧪 Upcoming Enhancements

### Data Sources Expansion
- [ ] **Cloud Integration**: Add support for Google Drive, Dropbox, and OneDrive documents
- [ ] **Social & Professional**: Add LinkedIn profiles, Twitter feeds, and Medium articles integration
- [ ] **Academic Sources**: Connect to arXiv, Google Scholar, and research databases

### Performance Optimizations
- [ ] **Parallel Processing**: Improve multi-document processing with adaptive concurrency control
- [ ] **Merge Algorithm**: Enhance the logarithmic-depth merge tree for better memory efficiency
- [ ] **Streaming Processing**: Implement document streaming for reduced memory footprint

### Output & Integration
- [ ] **Vector DB Export**: Direct export to Pinecone, Chroma, Weaviate, and other vector databases
- [ ] **LangChain Integration**: Simplified integration with LangChain for RAG applications
- [ ] **Custom Schemas**: User-definable output schemas for specialized knowledge base formats

### Advanced Features
- [ ] **Incremental Updates**: Support for updating existing knowledge bases with new content
- [ ] **Multi-language Support**: Process and merge content across different languages
- [ ] **Custom Taxonomies**: Allow users to define custom categorization schemas for content organization

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

MIT © [Kostadin Devedzhiev](https://github.com/kostadindev)
