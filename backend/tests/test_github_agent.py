import asyncio

from backend.agents.github_agent import GitHubAgent
from backend.tools.github_client import GitHubReadOnlyClient


def test_repository_count_query():
    client = GitHubReadOnlyClient(mock_data={
        "repositories": [
            {"name": "ai-agent", "private": False},
            {"name": "inventory-system", "private": True},
            {"name": "docs", "private": False},
        ]
    })
    agent = GitHubAgent(client)

    result = asyncio.run(agent.process("How many repositories do I have?"))

    assert result["intent"] == "repositories"
    assert "3 repositories" in result["response"]


def test_readme_query_uses_repository_context():
    client = GitHubReadOnlyClient(mock_data={
        "repositories": [{"name": "ai-agent", "private": False}],
        "readme": {"content": "# AI Agent\n\nThis project helps users explore GitHub."},
    })
    agent = GitHubAgent(client)

    result = asyncio.run(agent.process("Show the README for AI-Agent", repository="ai-agent"))

    assert result["intent"] == "readme"
    assert "AI Agent" in result["response"]
    assert "read-only" in result["response"].lower()
