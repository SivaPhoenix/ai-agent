# mock_search.py
class MockSearchClient:
    def __init__(self):
        pass

    def search(self, query):
        # Return 3 mocked results per query
        return [
            {"title": f"{query} - Market analysis", "snippet": "A short summary of market trends.", "url": "https://example.com/article1"},
            {"title": f"{query} - Competitor signal", "snippet": "Competitor launched feature X.", "url": "https://example.com/article2"},
            {"title": f"{query} - User sentiment", "snippet": "Users are asking for integration Y.", "url": "https://example.com/article3"}
        ]

    def health_check(self):
        # Return empty (healthy) list; you can simulate alerts here
        return []
