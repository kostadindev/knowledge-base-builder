#!/bin/bash
# Example usage of knowledge-base-builder CLI with unified 'files' parameter

# Basic usage with multiple files
python -m knowledge_base_builder.cli \
  --file "https://arxiv.org/pdf/2201.08239.pdf" \
  --file "https://www.gutenberg.org/files/1342/1342-0.txt" \
  --file "https://www.example.com/" \
  --output "cli_knowledge_base.md"

# Using a JSON sources file
python -m knowledge_base_builder.cli \
  --sources-file "example_sources.json" \
  --output "json_sources_knowledge_base.md"

# Advanced usage with all parameter types
python -m knowledge_base_builder.cli \
  --file "https://arxiv.org/pdf/2201.08239.pdf" \
  --file "https://www.example.com/" \
  --sitemap "https://www.example.com/sitemap.xml" \
  --google-api-key "$GOOGLE_API_KEY" \
  --gemini-model "gemini-2.0-flash" \
  --gemini-temperature 0.5 \
  --github-username "yourusername" \
  --output "advanced_knowledge_base.md" 