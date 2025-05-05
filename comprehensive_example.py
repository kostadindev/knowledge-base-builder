#!/usr/bin/env python
"""
Comprehensive example of the knowledge-base-builder package.

This script demonstrates how to use the knowledge-base-builder
with all supported file types using the unified 'files' approach.
"""

import os
from dotenv import load_dotenv
from knowledge_base_builder import KBBuilder

# Load environment variables from .env file
load_dotenv()

def main():
    """Run the knowledge base builder with various source types."""
    # API and model configuration
    config = {
        'GOOGLE_API_KEY': os.getenv("GOOGLE_API_KEY"),
        'GEMINI_MODEL': os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        'GEMINI_TEMPERATURE': float(os.getenv("GEMINI_TEMPERATURE", "0.7")),
        'GITHUB_USERNAME': os.getenv("GITHUB_USERNAME", ""),
        'GITHUB_API_KEY': os.getenv("GITHUB_API_KEY"),
    }
    
    # Ensure the Google API key is available
    if not config['GOOGLE_API_KEY']:
        print("Error: GOOGLE_API_KEY environment variable is required.")
        print("Please set it in your .env file or environment.")
        return
    
    # Comprehensive example of source documents with all supported file types
    sources = {
        'files': [
            # Document formats
            # PDF documents
            "https://arxiv.org/pdf/2201.08239.pdf",  # Example: LLM research paper
            "file:///path/to/local/document.pdf",    # Local PDF file
            
            # Microsoft Word documents (.docx)
            "https://filesamples.com/samples/document/docx/sample3.docx",
            "file:///path/to/local/document.docx",
            
            # Text files (.txt)
            "https://www.gutenberg.org/files/1342/1342-0.txt",  # Pride and Prejudice
            "file:///path/to/local/document.txt",
            
            # Markdown files (.md)
            "https://raw.githubusercontent.com/microsoft/ML-For-Beginners/main/README.md",
            "file:///path/to/local/document.md",
            
            # Rich Text Format files (.rtf)
            "https://filesamples.com/samples/document/rtf/sample1.rtf",
            "file:///path/to/local/document.rtf",
            
            # Spreadsheet formats
            # CSV files
            "https://people.sc.fsu.edu/~jburkardt/data/csv/addresses.csv",
            "file:///path/to/local/data.csv",
            
            # TSV files
            "https://raw.githubusercontent.com/biolists/covid19/master/curated_data.tsv",
            "file:///path/to/local/data.tsv",
            
            # Excel spreadsheets (.xlsx)
            "https://filesamples.com/samples/document/xlsx/sample1.xlsx",
            "file:///path/to/local/data.xlsx",
            
            # OpenDocument spreadsheets (.ods)
            "https://filesamples.com/samples/document/ods/sample1.ods",
            "file:///path/to/local/data.ods",
            
            # Web and markup content
            # HTML files
            "https://www.example.com/",
            "file:///path/to/local/page.html",
            
            # XML files
            "https://www.w3schools.com/xml/note.xml",
            "file:///path/to/local/data.xml",
            
            # JSON files
            "https://jsonplaceholder.typicode.com/posts",
            "file:///path/to/local/data.json",
            
            # YAML files
            "https://raw.githubusercontent.com/openai/gym/master/gym/envs/classic_control/cartpole.py",
            "file:///path/to/local/config.yaml",
        ],
        
        # Process all pages from a sitemap
        'sitemap_url': "https://www.example.com/sitemap.xml",
    }
    
    # Output file path
    output_file = "comprehensive_knowledge_base.md"
    
    print("Starting knowledge base creation with all supported file types:")
    print(f"- {len(sources['files'])} files/URLs")
    if sources['sitemap_url']:
        print(f"- Sitemap: {sources['sitemap_url']}")
    if config['GITHUB_USERNAME']:
        print(f"- GitHub content from: {config['GITHUB_USERNAME']}")
    print(f"Output will be saved to: {output_file}")
    
    # Create knowledge base builder instance
    kbb = KBBuilder(config)
    
    # Build the knowledge base
    kbb.build(sources=sources, output_file=output_file)
    
    print(f"\nKnowledge base creation complete!")
    print(f"The knowledge base has been saved to: {output_file}")
    print("You can now use this file in your RAG pipelines or LLM applications.")

if __name__ == "__main__":
    main() 