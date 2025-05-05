"""
Test script to demonstrate usage of the Knowledge Base Builder.
This script shows basic functionality without requiring all the data sources.
"""

import os
from dotenv import load_dotenv
from gemini_client import GeminiClient
from kb_builder import KnowledgeBaseBuilder
from kb_app import KnowledgeBaseApp

# Load environment variables
load_dotenv()

def test_build_simple_kb():
    """Simple test to build a knowledge base from text and save it."""
    print("🧪 Testing simple knowledge base creation")
    
    # Configuration
    config = {
        'GOOGLE_API_KEY': os.getenv("GOOGLE_API_KEY"),
        'GEMINI_MODEL': os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        'GEMINI_TEMPERATURE': float(os.getenv("GEMINI_TEMPERATURE", "0.7")),
    }
    
    # Create a simple text knowledge base
    gemini_client = GeminiClient(
        api_key=config['GOOGLE_API_KEY'],
        model=config.get('GEMINI_MODEL', 'gemini-2.0-flash'),
        temperature=float(config.get('GEMINI_TEMPERATURE', 0.7))
    )
    
    kb_builder = KnowledgeBaseBuilder(gemini_client)
    
    # Sample text to build knowledge base from
    sample_text = """
    # Knowledge Base Builder
    
    ## Description
    This is a tool that builds knowledge bases from various sources including:
    - PDFs
    - Websites
    - GitHub repositories
    
    ## Technical Details
    The tool uses Gemini models from Google to process and structure the data.
    It extracts text from PDFs, cleans HTML from websites, and processes markdown from GitHub.
    
    ## Usage
    To use this tool, you need to:
    1. Set up environment variables
    2. Configure your data sources
    3. Run the application
    """
    
    # Build KB from sample text
    kb = kb_builder.build_kb(sample_text)
    
    # Save the output
    output_path = "test_knowledge_base.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(kb)
    
    print(f"✅ Test knowledge base written to: {output_path}")

def test_app_with_minimal_sources():
    """Test the KnowledgeBaseApp with minimal sources."""
    print("🧪 Testing KnowledgeBaseApp with minimal sources")
    
    # Configuration
    config = {
        'GOOGLE_API_KEY': os.getenv("GOOGLE_API_KEY"),
        'GEMINI_MODEL': os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        'GEMINI_TEMPERATURE': float(os.getenv("GEMINI_TEMPERATURE", "0.7")),
    }
    
    # Create app instance
    app = KnowledgeBaseApp(config)
    
    # Add a simple text KB directly
    sample_text = """
    # Sample Knowledge
    This is some sample knowledge content that would normally come from a PDF or website.
    
    ## Topics
    - Topic 1: Information about topic 1
    - Topic 2: Information about topic 2
    
    ## Conclusion
    This is a conclusion paragraph.
    """
    
    kb = app.kb_builder.build_kb(sample_text)
    app.kbs.append(kb)
    
    # Build final KB
    app.build_final_kb("test_app_kb.md")
    
    print(f"✅ Test app knowledge base written to: test_app_kb.md")

if __name__ == "__main__":
    print("Starting Knowledge Base Builder tests...")
    test_build_simple_kb()
    print("\n" + "-" * 40 + "\n")
    test_app_with_minimal_sources()
    print("\nTests completed!") 