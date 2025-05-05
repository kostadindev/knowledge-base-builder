import requests
from typing import List, Optional

class GitHubProcessor:
    """Handle GitHub repository processing."""
    def __init__(self, username: Optional[str] = None, token: Optional[str] = None):
        self.username = username
        self.headers = {"Authorization": f"token {token}"} if token else {}

    def get_markdown_urls(self) -> List[str]:
        """Get all markdown file URLs from user's repositories."""
        if not self.username:
            raise ValueError("Username is required for this method")
        
        repos = self.get_user_repos()
        urls = []
        for repo in repos:
            print(f"🔍 Scanning repo: {repo}")
            urls.extend(self.get_markdown_urls_for_repo(self.username, repo))
        return urls

    def get_user_repos(self) -> List[str]:
        """Get all repositories for a user."""
        if not self.username:
            raise ValueError("Username is required for this method")
            
        repos = []
        page = 1
        while True:
            url = f"https://api.github.com/users/{self.username}/repos?per_page=100&page={page}"
            res = requests.get(url, headers=self.headers)
            if res.status_code != 200:
                raise Exception(f"GitHub API error: {res.status_code}")
            data = res.json()
            if not data:
                break
            repos.extend(repo['name'] for repo in data)
            page += 1
        return repos

    def get_markdown_urls_for_repo(self, owner: str, repo: str) -> List[str]:
        """Get all markdown files from a specific repository."""
        def recurse(path=""):
            url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
            res = requests.get(url, headers=self.headers)
            if res.status_code != 200:
                return []
            contents = res.json()
            files = []
            for item in contents:
                if item['type'] == 'file' and item['name'].endswith('.md'):
                    files.append(item['download_url'])
                elif item['type'] == 'dir':
                    files.extend(recurse(item['path']))
            return files
        return recurse()

    # Legacy method, maintained for backward compatibility
    def _get_user_repos(self) -> List[str]:
        """Get all repositories for a user (legacy method)."""
        return self.get_user_repos()

    # Legacy method, maintained for backward compatibility
    def _get_repo_md_files(self, repo: str) -> List[str]:
        """Get all markdown files from a repository (legacy method)."""
        if not self.username:
            raise ValueError("Username is required for this method")
        return self.get_markdown_urls_for_repo(self.username, repo)

    @staticmethod
    def download_markdown(url: str) -> str:
        """Download markdown content from a URL."""
        res = requests.get(url)
        if res.status_code != 200:
            raise Exception(f"Failed to fetch markdown from: {url}")
        return res.text 