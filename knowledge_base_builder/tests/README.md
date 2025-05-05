# Knowledge Base Builder Tests

This directory contains tests for the Knowledge Base Builder application.

## Setup

Install the test dependencies:

```bash
pip install -r ../test-requirements.txt
```

## Running Tests

To run all tests:

```bash
pytest
```

To run tests with coverage report:

```bash
pytest --cov=. --cov-report=term-missing
```

## Test Structure

- `test_kb_builder.py` - Tests for the main KB Builder class
- `test_pdf_processor.py` - Tests for PDF processing functionality
- `test_website_processor.py` - Tests for website processing
- `test_github_processor.py` - Tests for GitHub integration
- `test_gemini_client.py` - Tests for the Gemini API client
- `test_llm.py` - Tests for LLM class functionality
- `test_construct_kb.py` - Tests for the main script

## Current Coverage Report

```
Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
__init__.py                           7      0   100%
construct_kb.py                      13      1    92%   49
gemini_client.py                      7      0   100%
github_processor.py                  48      1    98%   41
kb_builder.py                       101     49    51%   87-96, 100-107, 111-123, 128-129, 133-140, 146-156
llm.py                               21      1    95%   43
pdf_processor.py                     37      2    95%   28-29
tests\__init__.py                     0      0   100%
tests\conftest.py                    23     11    52%   9-11, 16-24, 29, 40
tests\test_construct_kb.py           39      2    95%   60, 71
tests\test_gemini_client.py          29      1    97%   64
tests\test_github_processor.py       60      1    98%   108
tests\test_kb_builder.py             48      1    98%   80
tests\test_llm.py                    39      1    97%   85
tests\test_pdf_processor.py          59      1    98%   94
tests\test_website_processor.py      47      1    98%   91
website_processor.py                 20      0   100%
---------------------------------------------------------------
TOTAL                               598     73    88%
```

### Coverage Summary

- Overall coverage: 88%
- Modules with 100% coverage: `gemini_client.py`, `website_processor.py`, `__init__.py`
- Modules with 90%+ coverage: `construct_kb.py` (92%), `github_processor.py` (98%), `llm.py` (95%), `pdf_processor.py` (95%)
- Modules needing improvement: `kb_builder.py` (51%)

## Areas for Improvement

The main area that could use more tests is the `kb_builder.py` module, which has the lowest coverage at 51%. Specifically, these methods need additional test coverage:

- `process_pdfs()` (lines 87-96)
- `process_web_urls()` (lines 100-107)
- `process_websites()` (lines 111-123)
- `process_github()` (lines 128-140)
- `build_final_kb()` (lines 146-156)

## Adding New Tests

When adding new tests, follow these conventions:
1. Create test files with the naming pattern `test_*.py`
2. Test classes should be named `Test*`
3. Test methods should be named `test_*`
4. Use fixtures from `conftest.py` when appropriate 