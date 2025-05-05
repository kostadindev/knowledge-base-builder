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
        description="Build a knowledge base from multiple sources using various LLM providers."
    )
    
    # Basic configuration
    parser.add_argument("--output", "-o", default="final_knowledge_base.md",
                      help="Output file path for the knowledge base (default: final_knowledge_base.md)")
    
    # LLM Provider selection
    parser.add_argument("--llm-provider", default=os.environ.get('LLM_PROVIDER', 'gemini'),
                      choices=['gemini', 'openai', 'anthropic'],
                      help="LLM provider to use (default: gemini)")
    
    # Gemini configuration
    parser.add_argument("--google-api-key", 
                      help="Google API Key (default: from GOOGLE_API_KEY env var)")
    parser.add_argument("--gemini-model", default="gemini-2.0-flash",
                      help="Gemini model name (default: gemini-2.0-flash)")
    parser.add_argument("--gemini-temperature", type=float, default=0.7,
                      help="Temperature for Gemini model (default: 0.7)")
    
    # OpenAI configuration
    parser.add_argument("--openai-api-key", 
                      help="OpenAI API Key (default: from OPENAI_API_KEY env var)")
    parser.add_argument("--openai-model", default="gpt-4o",
                      help="OpenAI model name (default: gpt-4o)")
    parser.add_argument("--openai-temperature", type=float, default=0.7,
                      help="Temperature for OpenAI model (default: 0.7)")
    
    # Anthropic configuration
    parser.add_argument("--anthropic-api-key", 
                      help="Anthropic API Key (default: from ANTHROPIC_API_KEY env var)")
    parser.add_argument("--anthropic-model", default="claude-3-7-sonnet",
                      help="Anthropic model name (default: claude-3-7-sonnet)")
    parser.add_argument("--anthropic-temperature", type=float, default=0.7,
                      help="Temperature for Anthropic model (default: 0.7)")
    
    # GitHub configuration
    parser.add_argument("--github-username", 
                      help="GitHub username (default: from GITHUB_USERNAME env var)")
    parser.add_argument("--github-api-key", 
                      help="GitHub API Key (default: from GITHUB_API_KEY env var)")
    
    # Sources - New unified approach
    parser.add_argument("--file", "-f", action="append", default=[],
                      help="File URL or local file path (any supported format) (can be used multiple times)")
    
    # Sources - Legacy support
    parser.add_argument("--pdf", "-p", action="append", default=[],
                      help="[Legacy] PDF URLs or local file paths")
    parser.add_argument("--document", "-d", action="append", default=[],
                      help="[Legacy] Document URLs or local file paths (.docx, .txt, .md, .rtf)")
    parser.add_argument("--spreadsheet", "-s", action="append", default=[],
                      help="[Legacy] Spreadsheet URLs or local file paths (.csv, .tsv, .xlsx, .ods)")
    parser.add_argument("--web-content", "-w", action="append", default=[],
                      help="[Legacy] Web content URLs or local file paths (.html, .xml, .json, .yaml/.yml)")
    parser.add_argument("--web-url", "-u", action="append", default=[],
                      help="[Legacy] Individual web page URLs")
    
    # Website / Sitemap
    parser.add_argument("--sitemap", "-m", 
                      help="Process an entire website using its sitemap URL")
    
    # GitHub repositories
    parser.add_argument("--github-repo", "-g", action="append", default=[],
                      help="GitHub repositories to process (format: username/repo or https://github.com/username/repo)")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Build config dictionary
    config = {
        # LLM provider selection
        'LLM_PROVIDER': args.llm_provider,
        
        # Gemini configuration
        'GOOGLE_API_KEY': args.google_api_key or os.environ.get('GOOGLE_API_KEY', ''),
        'GEMINI_MODEL': args.gemini_model,
        'GEMINI_TEMPERATURE': args.gemini_temperature,
        
        # OpenAI configuration
        'OPENAI_API_KEY': args.openai_api_key or os.environ.get('OPENAI_API_KEY', ''),
        'OPENAI_MODEL': args.openai_model,
        'OPENAI_TEMPERATURE': args.openai_temperature,
        
        # Anthropic configuration
        'ANTHROPIC_API_KEY': args.anthropic_api_key or os.environ.get('ANTHROPIC_API_KEY', ''),
        'ANTHROPIC_MODEL': args.anthropic_model,
        'ANTHROPIC_TEMPERATURE': args.anthropic_temperature,
        
        # GitHub configuration
        'GITHUB_USERNAME': args.github_username or os.environ.get('GITHUB_USERNAME', ''),
        'GITHUB_API_KEY': args.github_api_key or os.environ.get('GITHUB_API_KEY', ''),
    }
    
    # Validate required API keys based on selected provider
    if args.llm_provider == 'gemini' and not config['GOOGLE_API_KEY']:
        parser.error("Google API Key is required when using Gemini. Provide via --google-api-key or GOOGLE_API_KEY environment variable.")
    elif args.llm_provider == 'openai' and not config['OPENAI_API_KEY']:
        parser.error("OpenAI API Key is required when using OpenAI. Provide via --openai-api-key or OPENAI_API_KEY environment variable.")
    elif args.llm_provider == 'anthropic' and not config['ANTHROPIC_API_KEY']:
        parser.error("Anthropic API Key is required when using Claude. Provide via --anthropic-api-key or ANTHROPIC_API_KEY environment variable.")
    
    # Build sources dictionary for the knowledge base
    sources = {
        # Unified approach
        'files': args.file,
        
        # Legacy support
        'pdf_urls': args.pdf,
        'document_urls': args.document,
        'spreadsheet_urls': args.spreadsheet,
        'web_content_urls': args.web_content,
        'web_urls': args.web_url,
        
        # Sitemap
        'sitemap_url': args.sitemap,
        
        # GitHub repositories
        'github_repositories': args.github_repo,
    }
    
    # Initialize KB Builder
    kb_builder = KBBuilder(config)
    
    # Build and save knowledge base
    output_path = kb_builder.build_kb(sources, args.output)
    print(f"Knowledge base built successfully: {output_path}")

if __name__ == "__main__":
    main() 