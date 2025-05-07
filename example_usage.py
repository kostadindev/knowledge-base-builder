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
        'GITHUB_API_KEY': os.getenv("GITHUB_API_KEY"), # Optional
    }
    
    
    # Example source documents using the new unified 'files' approach
    sources = {
        # # Unified files list - automatically detects and processes each file type
        'files': [
            "https://kostadindev.github.io/projects.html",
        #     "C:/Users/kosta/Untitled Folder/Knowledge-Base-Builder/test_files/csms-checklist-revised-March-2024 (2).xlsx",
        #     "C:/Users/kosta/Untitled Folder/Knowledge-Base-Builder/test_files/random_data.csv",
        #     "C:/Users/kosta/Untitled Folder/Knowledge-Base-Builder/test_files/CV_2024.docx",
        #     "C:/Users/kosta/Untitled Folder/Knowledge-Base-Builder/test_files/emf-ellipse-publication.pdf"
        ],
        
        # Process all pages from a sitemap
        'sitemap_url': "https://kostadindev.github.io/sitemap.xml",
        
        # # # GitHub repositories to process (format: username/repo or full URL)
        'github_repositories': [
            "https://github.com/kostadindev/Knowledge-Base-Builder",
            "https://github.com/kostadindev/GONEXT",
            "https://github.com/kostadindev/Recursive-QA",
            "https://github.com/kostadindev/deep-gestures",
            "https://github.com/kostadindev/emf-ellipse",
            "https://github.com/kostadindev"
        ],
        # 'github_username': "kostadindev" # Process all repositories for a specific username
    }
    
    print("Starting knowledge base creation with the following sources:")
    print(f"- {len(sources['files'] if 'files' in sources else [])} files/URLs")
    print(f"- Sitemap: {sources.get('sitemap_url', 'None')}")
    print(f"- GitHub Repositories: {len(sources.get('github_repositories', []))}")
    print(f"Output will be saved to: knowledge_base.md")
    
    # Create knowledge base builder instance
    kbb = KBBuilder(config)
    
    # Build the knowledge base
    kbb.build(sources=sources, output_file="knowledge_base.md")
    
    print(f"\nKnowledge base creation complete!")
    print(f"The knowledge base has been saved to: knowledge_base.md")
    print("You can now use this file in your RAG pipelines or LLM applications.")

if __name__ == "__main__":
    main() 