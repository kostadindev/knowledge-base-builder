#!/usr/bin/env python
"""
Script to update the TestPyPI token in .pypirc file.
"""
import os

def update_pypirc():
    # Get token from user
    token = input("Enter your TestPyPI token: ")
    
    pypirc_content = f"""[testpypi]
username = __token__
password = {token}
repository = https://test.pypi.org/legacy/

[pypi]
username = __token__
password = pypi-your-token-here
"""

    user_home = os.path.expanduser("~")
    pypirc_path = os.path.join(user_home, ".pypirc")

    with open(pypirc_path, "w", encoding="utf-8") as f:
        f.write(pypirc_content)

    print(f"Updated {pypirc_path} with your TestPyPI token")

if __name__ == "__main__":
    update_pypirc() 