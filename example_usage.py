#!/usr/bin/env python
"""
Example usage of the knowledge-base-builder package.

This script demonstrates how to use the knowledge-base-builder
package to create a knowledge base from various sources.
"""

import os
from dotenv import load_dotenv
from knowledge_base_builder import KBBuilder

# Load environment variables from .env file
load_dotenv()

def main():
    """Run the knowledge base builder with example sources."""
    # API and model configuration
    config = {
        'GOOGLE_API_KEY': os.getenv("GOOGLE_API_KEY"),
        'GITHUB_USERNAME': os.getenv("GITHUB_USERNAME", ""),
        'GITHUB_API_KEY': os.getenv("GITHUB_API_KEY"),
    }
    
    # Ensure the Google API key is available
    if not config['GOOGLE_API_KEY']:
        print("Error: GOOGLE_API_KEY environment variable is required.")
        print("Please set it in your .env file or environment.")
        return
    
    # Example source documents using the new unified 'files' approach
    sources = {
        # Unified files list - automatically detects and processes each file type
        'files': [
            # PDF documents
            "https://kostadindev.github.io/static/documents/cv.pdf",
            "https://kostadindev.github.io/static/documents/sbu_transcript.pdf",
            "file:///C:/Users/kosta/OneDrive/Desktop/MS%20Application%20Materials/emf-ellipse-publication.pdf",
            
            # Web pages
            "https://kostadindev.github.io/index.html",
            "https://kostadindev.github.io/projects.html",
            
            # Add other file types as needed
            # "https://example.com/data.csv",
            # "file:///path/to/document.docx",
            # "https://example.com/api-docs.json",
        ],
        
        # Process all pages from a sitemap
        'sitemap_url': "https://kostadindev.github.io/sitemap.xml"
    }
    
    # Output file path
    output_file = "knowledge_base.md"
    
    print("Starting knowledge base creation with the following sources:")
    print(f"- {len(sources['files'])} files/URLs")
    print(f"- Sitemap: {sources['sitemap_url']}")
    print(f"Output will be saved to: {output_file}")
    
    # Create knowledge base builder instance
    kbb = KBBuilder(config)
    
    # Build the knowledge base
    kbb.build_kb(sources=sources, output_file=output_file)
    
    print(f"\nKnowledge base creation complete!")
    print(f"The knowledge base has been saved to: {output_file}")
    print("You can now use this file in your RAG pipelines or LLM applications.")

if __name__ == "__main__":
    main() 