#!/usr/bin/env python
"""
Script to create a properly formatted .pypirc file with UTF-8 encoding without BOM.
"""
import os

pypirc_content = """[testpypi]
username = __token__
password = pypi-your-token-here
repository = https://test.pypi.org/legacy/

[pypi]
username = __token__
password = pypi-your-token-here
"""

user_home = os.path.expanduser("~")
pypirc_path = os.path.join(user_home, ".pypirc")

with open(pypirc_path, "w", encoding="utf-8") as f:
    f.write(pypirc_content)

print(f"Created {pypirc_path} with UTF-8 encoding without BOM") 