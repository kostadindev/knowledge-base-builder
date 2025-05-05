from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="knowledge-base-builder",
    version="0.1.0",
    author="Kostadin Devedzhiev",
    author_email="kostadin.devedzhiev@gmail.com",  # Replace with actual email
    description="Build knowledge bases from multiple sources using large language models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kostadindev/knowledge-base-builder",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain>=0.1.0",
        "langchain-google-genai>=0.0.5",
        "langchain-community>=0.0.13",
        "beautifulsoup4>=4.12.2",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "lxml>=4.9.3",
        "pypdf>=3.17.0",
        # New dependencies for document processors
        "python-docx>=0.8.11",  # For .docx files
        "markdown>=3.4.3",      # For .md files
        "mistune>=2.0.5",       # Alternative Markdown parser
        "striprtf>=0.0.22",     # For .rtf files
        # New dependencies for spreadsheet processors
        "pandas>=2.0.0",        # For tabular data processing
        "openpyxl>=3.1.2",      # For .xlsx files
        "ezodf>=0.3.2",         # For .ods files
        # New dependencies for web content processors
        "pyyaml>=6.0",          # For .yaml/.yml files
    ],
    entry_points={
        "console_scripts": [
            "knowledge-base-builder=knowledge_base_builder.cli:main",
        ],
    },
) 