import re
from typing import Optional


class GitHubAgent:
    def __init__(self, client):
        self.client = client

    def process(self, query: str, repository: Optional[str] = None) -> dict:
        normalized = (query or "").strip()
        lowered = normalized.lower()

        if any(keyword in lowered for keyword in ["how many repositories", "repositories do i have", "list my repositories", "repository count"]):
            repos = self.client.list_repositories()
            return {
                "intent": "repositories",
                "response": f"I checked your accessible repositories and found {len(repos)} repositories. This is read-only access, so I can inspect them but not change them.",
                "read_only": True,
            }

        if "readme" in lowered:
            repo_name = self._extract_repository_name(normalized, repository)
            if repo_name:
                readme = self.client.get_readme(repo_name)
                content = readme.get("content", "") or ""
                summary = content[:400].strip()
                if not summary:
                    summary = "I could not find a README for that repository."
                return {
                    "intent": "readme",
                    "response": f"Here is the README for {repo_name}:\n\n{summary}\n\nThis response is generated in read-only mode.",
                    "read_only": True,
                }
            return {
                "intent": "readme",
                "response": "I need a repository name to fetch the README. Please provide one.",
                "read_only": True,
            }

        if any(keyword in lowered for keyword in ["branch", "branches"]):
            repo_name = self._extract_repository_name(normalized, repository)
            branches = self.client.list_branches(repo_name or "") if repo_name else []
            branch_names = ", ".join(branches[:5]) if branches else "none found"
            return {
                "intent": "branches",
                "response": f"I found these branches for {repo_name or 'the requested repository'}: {branch_names}. This is read-only access.",
                "read_only": True,
            }

        if any(keyword in lowered for keyword in ["commit", "commits", "latest commit"]):
            repo_name = self._extract_repository_name(normalized, repository)
            commits = self.client.list_commits(repo_name or "") if repo_name else []
            commit_summary = commits[0].get("message", "no commits found") if commits else "no commits found"
            return {
                "intent": "commits",
                "response": f"The latest commit for {repo_name or 'the requested repository'} is: {commit_summary}. I can inspect commit history in read-only mode.",
                "read_only": True,
            }

        return {
            "intent": "general",
            "response": f"I can help inspect GitHub repositories in read-only mode. Your request was: {normalized}",
            "read_only": True,
        }

    def _extract_repository_name(self, query: str, repository: Optional[str] = None) -> Optional[str]:
        if repository:
            return repository

        matches = re.findall(r"(?:for|in|of)\s+([A-Za-z0-9_.-]+)", query, flags=re.IGNORECASE)
        if matches:
            return matches[-1]

        if re.search(r"\b([A-Za-z0-9_.-]+)\b", query):
            candidate = re.search(r"\b([A-Za-z0-9_.-]+)\b", query).group(1)
            return candidate
        return None
