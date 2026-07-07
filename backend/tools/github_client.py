class GitHubReadOnlyClient:
    def __init__(self, mock_data=None):
        self.mock_data = mock_data or {}

    def list_repositories(self):
        return self.mock_data.get("repositories", [])

    def get_readme(self, repo_name):
        return self.mock_data.get("readme", {"content": ""})

    def list_branches(self, repo_name):
        return self.mock_data.get("branches", ["main", "development"])

    def list_commits(self, repo_name):
        return self.mock_data.get("commits", [{"message": "Initial commit"}])
