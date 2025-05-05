# 🧠 Multi-Source Knowledge Base Builder for LLMs

This project builds a **textual knowledge base** from various data sources such as PDFs, websites, and GitHub markdown files, using **Google Gemini models** to structure and summarize the content. The final output is a **Markdown-formatted knowledge base**, ready for use in **RAG pipelines**, chatbots, or any LLM application.

---

## ✨ Features

- 📄 **PDF ingestion** – Downloads local or remote PDFs and extracts structured text.
- 🌐 **Website ingestion** – Crawls pages from a sitemap and extracts clean HTML content.
- 📘 **GitHub integration** *(optional)* – Fetches Markdown files from public repositories.
- 🧠 **LLM-powered summarization** – Uses Gemini to convert raw data into readable, structured Markdown.
- 🔁 **Recursive merging** – Combines multiple knowledge base sections into a single cohesive document.

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

> Make sure `langchain`, `bs4`, `requests`, and `python-dotenv` are included.

### 4. Run the Script

```bash
python main.py
```

The script will:

1. Download PDFs and extract text.
2. Crawl your sitemap and parse web page content.
3. *(Optional)* Fetch Markdown files from your GitHub repos.
4. Use Gemini to convert all content into structured Markdown.
5. Merge everything into `final_knowledge_base.md`.

---

## 🛠️ Project Structure

```bash
.
├── main.py                # Main pipeline logic
├── requirements.txt       # Python dependencies
├── .env                   # Your secret tokens and config
└── final_knowledge_base.md # Output KB (auto-generated)
```

---

## 🔧 Supported Sources

| Source     | Description                                       | Toggle |
|------------|---------------------------------------------------|--------|
| PDFs       | Local or HTTP/HTTPS links                         | ✅     |
| Websites   | All URLs found via XML sitemap                    | ✅     |
| GitHub     | Markdown files from your public repositories      | 🔲 (Optional, commented out) |

To enable GitHub ingestion, uncomment the corresponding code in `main.py`.

---

## 🧠 Gemini Prompt Strategy

- Summarizes content into Markdown using **sections**, **bullet points**, and **clear formatting**.
- Merges summaries recursively in pairs to ensure **contextual cohesion**.

---

## 📌 Example Usage

Here’s what you’ll see in the terminal:

```
📄 PDF: https://example.com/doc.pdf
🌐 Sitemap: https://example.com/sitemap.xml
🔗 Website: https://example.com/page1
🔀 Merging all knowledge bases...
✅ Final KB written to: final_knowledge_base.md
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

---

## 📄 License

MIT © [Kostadin Devedzhiev](https://github.com/kostadindev)
