"""Command line interface for Knowledge Base Builder."""

import os
import argparse
import json
from dotenv import load_dotenv
from knowledge_base_builder import KBBuilder

def main():
    """Main entry point for CLI."""
    # Load environment variables
    load_dotenv()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Build a knowledge base from multiple sources using Google Gemini models."
    )
    
    # Basic configuration
    parser.add_argument("--output", "-o", default="final_knowledge_base.md",
                      help="Output file path for the knowledge base (default: final_knowledge_base.md)")
    
    # API Keys and configuration
    parser.add_argument("--google-api-key", 
                      help="Google API Key (default: from GOOGLE_API_KEY env var)")
    parser.add_argument("--gemini-model", default="gemini-2.0-flash",
                      help="Gemini model name (default: gemini-2.0-flash)")
    parser.add_argument("--gemini-temperature", type=float, default=0.7,
                      help="Temperature for Gemini model (default: 0.7)")
    parser.add_argument("--github-username", 
                      help="GitHub username (default: from GITHUB_USERNAME env var)")
    parser.add_argument("--github-api-key", 
                      help="GitHub API Key (default: from GITHUB_API_KEY env var)")
    
    # Sources
    parser.add_argument("--pdf", "-p", action="append", default=[],
                      help="PDF URLs or local file paths (can be used multiple times)")
    parser.add_argument("--web", "-w", action="append", default=[],
                      help="Web URLs to process (can be used multiple times)")
    parser.add_argument("--sitemap", "-s", 
                      help="Sitemap URL to process all contained URLs")
    parser.add_argument("--sources-file", 
                      help="JSON file containing sources configuration")
    
    args = parser.parse_args()
    
    # Load API keys from args or environment
    config = {
        'GOOGLE_API_KEY': args.google_api_key or os.getenv("GOOGLE_API_KEY"),
        'GEMINI_MODEL': args.gemini_model or os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        'GEMINI_TEMPERATURE': float(args.gemini_temperature or os.getenv("GEMINI_TEMPERATURE", "0.7")),
        'GITHUB_USERNAME': args.github_username or os.getenv("GITHUB_USERNAME", ""),
        'GITHUB_API_KEY': args.github_api_key or os.getenv("GITHUB_API_KEY"),
    }
    
    # Validate required API key
    if not config['GOOGLE_API_KEY']:
        parser.error("Google API Key is required. Set --google-api-key or GOOGLE_API_KEY environment variable.")
        return
    
    # Build sources configuration
    sources = {
        'pdf_urls': args.pdf,
        'web_urls': args.web,
        'sitemap_url': args.sitemap,
    }
    
    # If sources file is provided, load and merge with command line sources
    if args.sources_file:
        try:
            with open(args.sources_file, 'r') as file:
                file_sources = json.load(file)
                
                # Merge sources from file with command line sources
                if 'pdf_urls' in file_sources and file_sources['pdf_urls']:
                    sources['pdf_urls'].extend(file_sources['pdf_urls'])
                
                if 'web_urls' in file_sources and file_sources['web_urls']:
                    sources['web_urls'].extend(file_sources['web_urls'])
                
                if 'sitemap_url' in file_sources and file_sources['sitemap_url'] and not sources['sitemap_url']:
                    sources['sitemap_url'] = file_sources['sitemap_url']
        except Exception as e:
            print(f"Error loading sources file: {e}")
    
    # Validate that we have at least one source
    if not sources['pdf_urls'] and not sources['web_urls'] and not sources['sitemap_url']:
        parser.error("No sources provided. Use --pdf, --web, --sitemap, or --sources-file.")
        return
    
    # Create KB builder
    kbb = KBBuilder(config)
    
    # Build knowledge base
    output_file = kbb.build_kb(sources=sources, output_file=args.output)
    
    print(f"Knowledge base successfully created at: {output_file}")

if __name__ == "__main__":
    main() 