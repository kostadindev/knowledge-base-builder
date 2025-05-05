# 🧠 Multi-Source Knowledge Base Builder for LLMs

This project builds a **textual knowledge base** from various data sources such as PDFs, websites, and GitHub markdown files, using **Google Gemini models** to structure and summarize the content. The final output is a **Markdown-formatted knowledge base**, ready for use in **RAG pipelines**, chatbots, or any LLM application.

---

## ✨ Features

- 📄 **PDF ingestion** – Downloads local or remote PDFs and extracts structured text.
- 🌐 **Website ingestion** – Crawls pages from a sitemap and extracts clean HTML content.
- 📘 **GitHub integration** *(optional)* – Fetches Markdown files from public repositories.
- 🧠 **LLM-powered summarization** – Uses Gemini to convert raw data into readable, structured Markdown.
- 🔁 **Recursive merging** – Combines multiple knowledge base sections into a single cohesive document.
- 🏗️ **Modular design** – Well-organized class-based architecture for better maintainability.

---

## 🚀 Quickstart

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/llm-kb-builder.git
cd llm-kb-builder
```

### 2. Set up your `.env` file

Create a `.env` file in the root directory with the following variables:

```env
GOOGLE_API_KEY=your_google_api_key
GEMINI_MODEL=gemini-2.0-flash
GEMINI_TEMPERATURE=0.7

GITHUB_USERNAME=your_github_username
GITHUB_API_KEY=your_github_token  # Optional
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Script

```bash
python construct_kb.py
```

The script will:

1. Download PDFs and extract text.
2. Crawl your sitemap and parse web page content.
3. *(Optional)* Fetch Markdown files from your GitHub repos.
4. Use Gemini to convert all content into structured Markdown.
5. Merge everything into `final_knowledge_base.md`.

---

## 🏗️ Architecture

The codebase follows an object-oriented design with the following components:

```
KnowledgeBaseApp (Main application class)
├── GeminiClient (LLM client)
├── KnowledgeBaseBuilder (KB generation & merging)
├── PDFProcessor (PDF handling)
├── WebsiteProcessor (Website parsing)
└── GitHubProcessor (GitHub integration)
```

### Class Responsibilities:

- **KnowledgeBaseApp**: Orchestrates the entire knowledge base building process
- **GeminiClient**: Handles interactions with Google's Gemini AI model
- **KnowledgeBaseBuilder**: Builds and merges knowledge base content
- **PDFProcessor**: Downloads and extracts text from PDF files
- **WebsiteProcessor**: Parses sitemaps and extracts content from websites
- **GitHubProcessor**: Fetches Markdown files from GitHub repositories

### File Structure:

```
.
├── construct_kb.py         # Main script
├── gemini_client.py        # Gemini API client
├── kb_app.py               # Main application class
├── kb_builder.py           # Knowledge base building utility
├── pdf_processor.py        # PDF processing utility
├── website_processor.py    # Website processing utility
├── github_processor.py     # GitHub processing utility
├── __init__.py             # Package initialization
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
└── test_kb_builder.py      # Test script
```

---

## 🔧 Supported Sources

| Source     | Description                                       | Toggle |
|------------|---------------------------------------------------|--------|
| PDFs       | Local or HTTP/HTTPS links                         | ✅     |
| Websites   | All URLs found via XML sitemap                    | ✅     |
| GitHub     | Markdown files from your public repositories      | 🔲 (Optional, commented out) |

To enable GitHub ingestion, uncomment the corresponding code in `main()`.

---

## 🧠 Gemini Prompt Strategy

- Summarizes content into Markdown using **sections**, **bullet points**, and **clear formatting**.
- Merges summaries recursively in pairs to ensure **contextual cohesion**.

---

## 📌 Example Usage

### Basic Usage
Run the main script to process all configured sources:
```bash
python construct_kb.py
```

### Using Individual Components

```python
from kb_app import KnowledgeBaseApp
import os

# Configuration
config = {
    'GOOGLE_API_KEY': os.getenv("GOOGLE_API_KEY"),
    'GEMINI_MODEL': "gemini-2.0-flash",
    'GEMINI_TEMPERATURE': 0.7,
}

# Create app instance
app = KnowledgeBaseApp(config)

# Process specific sources
app.process_pdfs(["path/to/document.pdf"])
app.process_websites("https://example.com/sitemap.xml")

# Generate final knowledge base
app.build_final_kb("output.md")
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

- [ ] Add support for other document types (.docx, .txt)
- [ ] Handle rate limits for large GitHub accounts
- [ ] Add CLI flags to enable/disable each source
- [ ] Integrate with vector databases (e.g., Pinecone, Chroma)
- [ ] Add unit tests for each class
- [ ] Create configuration file for easier customization
- [ ] Implement async processing for better performance

---

## 📄 License

MIT © [Kostadin Devedzhiev](https://github.com/kostadindev)
