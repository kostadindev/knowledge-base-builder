# Test Plan for Improving Coverage

This document outlines a test plan to improve the coverage of the `kb_builder.py` module, which currently has 51% test coverage.

## Target Methods

These methods in `kb_builder.py` need additional test coverage:

1. `process_pdfs()` (lines 87-96)
2. `process_web_urls()` (lines 100-107)
3. `process_websites()` (lines 111-123)
4. `process_github()` (lines 128-140)
5. `build_final_kb()` (lines 146-156)

## Test Plan

### Testing `process_pdfs()`

Add the following test cases to `test_kb_builder.py`:

- `test_process_pdfs_success`: Test processing PDFs successfully
  - Mock PDF processor to return valid text
  - Mock LLM to return a knowledge base
  - Verify KBs are added to the instance

- `test_process_pdfs_error`: Test handling errors in PDF processing
  - Mock PDF processor to raise exceptions
  - Verify error handling works correctly

### Testing `process_web_urls()`

Add the following test cases:

- `test_process_web_urls_success`: Test processing web URLs successfully
  - Mock website processor to return valid text
  - Mock LLM to return a knowledge base
  - Verify KBs are added to the instance

- `test_process_web_urls_error`: Test handling errors
  - Mock website processor to raise exceptions
  - Verify error handling works correctly

### Testing `process_websites()`

Add the following test cases:

- `test_process_websites_success`: Test processing websites from a sitemap
  - Mock website processor to return list of URLs
  - Mock website processor to return valid text for each URL
  - Verify multiple URLs are processed correctly

- `test_process_websites_error`: Test error handling
  - Test sitemap fetch error
  - Test individual URL processing errors

### Testing `process_github()`

Add the following test cases:

- `test_process_github_with_credentials`: Test with valid GitHub credentials
  - Mock GitHub processor to return list of markdown URLs
  - Mock download responses with valid markdown content
  - Verify markdown files are processed

- `test_process_github_without_credentials`: Test behavior when no GitHub username is provided
  - Verify no processing occurs

- `test_process_github_error`: Test error handling
  - Mock GitHub API errors
  - Verify processing continues despite errors

### Testing `build_final_kb()`

Add the following test cases:

- `test_build_final_kb_with_kbs`: Test with knowledge bases
  - Create multiple mock knowledge bases
  - Mock LLM's recursive merge
  - Verify final KB is written to file

- `test_build_final_kb_empty`: Test with no knowledge bases
  - Verify appropriate handling when no KBs have been created

## Implementation Plan

1. Add fixtures in `conftest.py` for common test data
2. Implement the test cases in priority order
3. Run with coverage to validate improved percentage
4. Document improvements in the README.md 