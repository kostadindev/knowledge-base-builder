#!/usr/bin/env python
"""
Build script for the knowledge-base-builder package.
This script helps with building and publishing the package to PyPI.
"""

import os
import sys
import shutil
import subprocess

def run_command(command):
    """Run a shell command and print output."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=True)
    return result.returncode == 0

def clean():
    """Clean build directories."""
    print("Cleaning build directories...")
    directories = ['dist', 'build', 'knowledge_base_builder.egg-info']
    for directory in directories:
        if os.path.exists(directory):
            shutil.rmtree(directory)
    print("Clean complete!")

def build():
    """Build the package."""
    print("Building package...")
    if not run_command("pip install --upgrade build"):
        return False
    if not run_command("python -m build"):
        return False
    print("Build complete!")
    return True

def upload_test():
    """Upload the package to TestPyPI."""
    print("Uploading to TestPyPI...")
    if not run_command("pip install --upgrade twine"):
        return False
    if not run_command("twine upload --repository testpypi dist/*"):
        return False
    print("Upload to TestPyPI complete!")
    return True

def upload_prod():
    """Upload the package to PyPI."""
    print("Uploading to PyPI...")
    if not run_command("pip install --upgrade twine"):
        return False
    if not run_command("twine upload dist/*"):
        return False
    print("Upload to PyPI complete!")
    return True

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python build_package.py [clean|build|upload-test|upload|all]")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'clean' or command == 'all':
        clean()
    
    if command == 'build' or command == 'all':
        if not build():
            print("Build failed!")
            return
    
    if command == 'upload-test' or command == 'all':
        if not upload_test():
            print("Upload to TestPyPI failed!")
            return
    
    if command == 'upload' and len(sys.argv) > 2 and sys.argv[2].lower() == '--confirm':
        if not upload_prod():
            print("Upload to PyPI failed!")
            return
    elif command == 'upload':
        print("To upload to production PyPI, use: python build_package.py upload --confirm")
        return
    
    print("All operations completed successfully!")

if __name__ == "__main__":
    main() 