from fastapi import FastAPI
from pydantic import BaseModel
from backend.agents.github_agent import GitHubAgent
from backend.tools.github_client import GitHubReadOnlyClient

app = FastAPI(title="GitHub Read-Only AI Agent")
client = GitHubReadOnlyClient(mock_data={
    "repositories": [
        {"name": "ai-agent", "private": False},
        {"name": "inventory-system", "private": True},
        {"name": "docs", "private": False},
    ],
    "readme": {"content": "# AI Agent\n\nThis project helps users explore GitHub in read-only mode."},
    "branches": ["main", "development", "feature/chat"],
    "commits": [{"message": "Add GitHub agent support"}],
})
agent = GitHubAgent(client)


class GitHubQuery(BaseModel):
    query: str
    repository: str | None = None


@app.post("/chat")
async def chat(payload: GitHubQuery):
    return agent.process(payload.query, repository=payload.repository)
