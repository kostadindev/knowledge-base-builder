import requests
from typing import List, Optional

class GitHubProcessor:
    """Handle GitHub repository processing."""
    def __init__(self, username: str, token: Optional[str] = None):
        self.username = username
        self.headers = {"Authorization": f"token {token}"} if token else {}

    def get_markdown_urls(self) -> List[str]:
        """Get all markdown file URLs from user's repositories."""
        repos = self._get_user_repos()
        urls = []
        for repo in repos:
            print(f"🔍 Scanning repo: {repo}")
            urls.extend(self._get_repo_md_files(repo))
        return urls

    def _get_user_repos(self) -> List[str]:
        """Get all repositories for a user."""
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

    def _get_repo_md_files(self, repo: str) -> List[str]:
        """Get all markdown files from a repository."""
        def recurse(path=""):
            url = f"https://api.github.com/repos/{self.username}/{repo}/contents/{path}"
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

    @staticmethod
    def download_markdown(url: str) -> str:
        """Download markdown content from a URL."""
        res = requests.get(url)
        if res.status_code != 200:
            raise Exception(f"Failed to fetch markdown from: {url}")
        return res.text 