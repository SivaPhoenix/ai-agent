# research_agent.py
from typing import List
import asyncio

class ResearchAgent:
    def __init__(self, search_client):
        self.search = search_client

    async def run(self, query: str) -> List[dict]:
        # In real implementation, call search API or SerpAPI; here we use mock client
        # Simulate network latency
        await asyncio.sleep(0.5)
        results = self.search.search(query)
        # Return list of dicts: {title, snippet, url}
        return results

