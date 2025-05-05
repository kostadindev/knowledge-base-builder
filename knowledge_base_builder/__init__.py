"""
Knowledge Base Builder Package
-----------------------------

This package provides tools to build structured knowledge bases from various sources
using Google Gemini models for summarization and processing.
"""

__version__ = "0.1.0"

from knowledge_base_builder.gemini_client import GeminiClient
from knowledge_base_builder.llm import LLM
from knowledge_base_builder.kb_builder import KBBuilder
from knowledge_base_builder.pdf_processor import PDFProcessor
from knowledge_base_builder.document_processor import DocumentProcessor
from knowledge_base_builder.spreadsheet_processor import SpreadsheetProcessor
from knowledge_base_builder.web_content_processor import WebContentProcessor
from knowledge_base_builder.website_processor import WebsiteProcessor
from knowledge_base_builder.github_processor import GitHubProcessor

__all__ = [
    'GeminiClient',
    'LLM',
    'KBBuilder',
    'PDFProcessor',
    'DocumentProcessor',
    'SpreadsheetProcessor',
    'WebContentProcessor',
    'WebsiteProcessor',
    'GitHubProcessor',
] 