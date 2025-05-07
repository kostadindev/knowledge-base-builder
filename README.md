# 🧠 Multi-Source Knowledge Base Builder for LLMs

A robust Python package designed to transform diverse content sources into a structured and comprehensive Markdown knowledge base optimized for large language models (LLMs). Efficiently ingest web content (HTML pages, sitemaps, XML), documents (PDFs, DOCXs, spreadsheets, Markdown, plaintext), and GitHub repositories, then process and merge them seamlessly using LLMs.

Built to power:
- Web-crawlable context files (`/llms.txt`)
- Retrieval-Augmented Generation (**RAG**) systems
- Vector databases preprocessing
- Custom chatbots and knowledge applications

## ✨ Features

- 📥 **Unified Source Ingestion** – Seamlessly handle local and remote files, websites, and GitHub repositories.
- 🧹 **Structured Text Extraction** – Cleanly convert various document formats into Markdown.
- 🌐 **Website Crawling** – Extract and summarize content from HTML pages and sitemaps.
- 📚 **GitHub Integration** – Automatically retrieve and process Markdown content from repositories.
- 🤖 **Advanced LLM Summarization** – Employ leading-edge models (Gemini Flash 2.0, GPT-4o, Claude 3.7 Sonnet) for precise and readable summaries.
- 🔗 **Efficient Document Merging** – Merge multiple knowledge bases using a parallel preprocessing step followed by a single optimized merging step.
- ⚙️ **Concurrency Control** – Smart throttling with semaphore-based concurrency ensures optimal use of resources and stable API usage.
- 🚀 **Performance** – Optimized algorithm significantly reduces processing time, ensures predictable memory usage, and minimizes API calls.

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

# API and model configuration | You need only one of the below
config = {
    'GOOGLE_API_KEY': os.getenv("GOOGLE_API_KEY"),     # For Gemini | Get Free API Key at https://aistudio.google.com/app/apikey
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

---

## 🧠 LLM Providers

| Provider | Models | Features |
|----------|--------|----------|
| Google Gemini | gemini-2.0-flash (default) | Free to try, Fast, large context window cost-effective summaries |
| OpenAI | gpt-4o (default) | High-quality summaries, strong reasoning |
| Anthropic | claude-3-7-sonnet (default) | High-quality summaries, excellent formatting |

> **Recommended Provider: Google Gemini**
> 
> Google Gemini is the recommended provider as a free development API key can be obtained. Additionally, it is fast, has a large context window, and performs well on benchmarks. Get your free API key at [Google AI Studio](https://aistudio.google.com/app/apikey).

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
## 🌲 Algorithm

The knowledge base builder uses a two-step approach for efficient processing:

1. **Parallel Preprocessing**
   - All documents are preprocessed concurrently into structured KBs
   - Uses a semaphore to limit concurrent LLM requests
   - Each document is converted into a well-formatted Markdown knowledge base
   - Optimized for parallel processing with controlled concurrency

2. **Single Merge**
   - All preprocessed KBs are merged in a single operation
   - Maintains logical structure and organization
   - Reduces total LLM calls compared to recursive approaches
   - More predictable memory usage

This approach provides several advantages:
- Fewer total LLM calls (one per document + one final merge)
- Better parallelization of preprocessing
- More predictable memory usage
- Faster overall processing time

---

## ⚡ Concurrency Model

The knowledge base builder implements a multi-layer concurrency model to maximize performance while maintaining stability:

### 1. File Processing Concurrency
```python
# Multiple files processed simultaneously
tasks = [process_file_async(file) for file in files]
await asyncio.gather(*tasks)
```
- Enables parallel processing of multiple files
- Each file type (PDF, DOCX, web page, etc.) is processed independently
- Significantly reduces total processing time for multiple files

### 2. CPU-Bound Operations
```python
# CPU-intensive operations run in separate threads
path = await asyncio.to_thread(processor.download, url)
text = await asyncio.to_thread(processor.extract_text, path)
```
- Downloads and text extraction run in separate threads
- Prevents blocking the event loop during I/O operations
- Optimizes CPU utilization across cores

### 3. LLM Processing Concurrency
```python
# Controlled concurrent LLM API calls
async with self._sem:
    result = await self.llm_client.run_async(prompt)
```
- Uses a semaphore to limit concurrent LLM API calls
- Prevents overwhelming the LLM API
- Helps stay within API rate limits
- Default concurrency limit: 8 simultaneous requests

### 4. Final KB Merging
```python
# Concurrent preprocessing followed by single merge
tasks = [preprocess_text_async(text) for text in texts]
preprocessed_kbs = await asyncio.gather(*tasks)
final_kb = await merge_all_kbs(preprocessed_kbs)
```
- Preprocesses all documents concurrently
- Merges them into a final knowledge base

### Performance Considerations
- **Resource Management**: CPU-bound operations don't block the event loop
- **Rate Limiting**: LLM API calls are properly throttled
- **Scalability**: System can handle many files without performance degradation
- **Constraints**:
  - LLM concurrency limit (default: 8)
  - System resources (CPU, memory, network)
  - LLM API rate limits

---

## ⚠️ Limitations

### Memory Usage
- **Document Processing**: Each document is loaded into memory during processing
- **LLM Context Windows**: Different models have different context window limits:
  - Gemini: 1M tokens
- **Merge Operations**: Final merge operation requires all preprocessed KBs in memory
- **Recommendation**: Monitor memory usage when processing large documents or many files

### Processing Time
- **I/O Operations**: Each file requires multiple I/O operations:
  - Downloading/reading the file
  - Text extraction
- **LLM Latency**: Each document requires at least one LLM call:
  - One call per document for preprocessing
  - One final call for merging

### Rate Limits
- **LLM API Limits**: Each provider has different rate limits
- **GitHub API**: 60 requests per hour (unauthenticated)
- **Web Scraping**: Some websites may block rapid requests

---

## 🧪 Future Improvements

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

### Performance & Limitations Improvements
- **Memory Optimization**:
  - [ ] Implement streaming document processing to reduce memory footprint
  - [ ] Add chunking for documents exceeding context windows
  - [ ] Develop smart caching system for processed documents
  - [ ] Add memory usage monitoring and automatic batch sizing

- **Processing Speed**:
  - [ ] Implement progressive document loading
  - [ ] Develop smart retry mechanisms for failed operations

- **Rate Limit Management**:
  - [ ] Add automatic rate limit detection and adaptation
  - [ ] Implement smart queuing system for API calls
  - [ ] Add support for multiple API keys rotation


---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to get started.

## 🐛 Bug Reports

Found a bug? Please check our [Contributing Guidelines](CONTRIBUTING.md#bug-reports) for instructions on how to report it.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

MIT © [Kostadin Devedzhiev](https://github.com/kostadindev)
