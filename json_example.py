#!/usr/bin/env python
"""
JSON configuration example for knowledge-base-builder.

This script demonstrates how to load source configurations from a JSON file
using the unified 'files' approach.
"""

import os
import json
from dotenv import load_dotenv
from knowledge_base_builder import KBBuilder

# Load environment variables from .env file
load_dotenv()

def main():
    """Run the knowledge base builder with sources from a JSON file."""
    # API and model configuration
    config = {
        'GOOGLE_API_KEY': os.getenv("GOOGLE_API_KEY"),
        'GEMINI_MODEL': os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        'GITHUB_USERNAME': os.getenv("GITHUB_USERNAME", ""),
        'GITHUB_API_KEY': os.getenv("GITHUB_API_KEY"),
    }
    
    # Ensure the Google API key is available
    if not config['GOOGLE_API_KEY']:
        print("Error: GOOGLE_API_KEY environment variable is required.")
        print("Please set it in your .env file or environment.")
        return
    
    # Load sources from JSON file
    sources_file = "example_sources.json"
    try:
        with open(sources_file, 'r') as file:
            sources = json.load(file)
            print(f"Successfully loaded sources from {sources_file}")
    except Exception as e:
        print(f"Error loading sources file {sources_file}: {e}")
        return
    
    # Output file path
    output_file = "json_config_knowledge_base.md"
    
    print("\nSource configuration loaded from JSON:")
    print(f"- {len(sources.get('files', []))} files/URLs")
    if sources.get('sitemap_url'):
        print(f"- Sitemap: {sources['sitemap_url']}")
    print(f"Output will be saved to: {output_file}")
    
    # Create knowledge base builder instance
    kbb = KBBuilder(config)
    
    # Build the knowledge base
    kbb.build_kb(sources=sources, output_file=output_file)
    
    print(f"\nKnowledge base creation complete!")
    print(f"The knowledge base has been saved to: {output_file}")

if __name__ == "__main__":
    main() 