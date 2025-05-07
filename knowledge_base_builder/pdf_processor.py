import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from knowledge_base_builder.base_processor import BaseProcessor

class PDFProcessor(BaseProcessor):
    """Handle PDF document processing."""
    
    SUPPORTED_EXTENSIONS = ['.pdf']
    
    @staticmethod
    def download(url: str) -> str:
        """Download a PDF from a URL or load from local file."""
        return BaseProcessor.download(url, PDFProcessor.SUPPORTED_EXTENSIONS)

    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """Extract text from a PDF file."""
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=20000, chunk_overlap=100)
        chunks = splitter.split_documents(documents)
        return "\n".join(chunk.page_content for chunk in chunks) 