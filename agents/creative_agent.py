# creative_agent.py
import asyncio
import openai
import os
from utils.helpers import short_summary

class CreativeAgent:
    def __init__(self, llm_api_key=None):
        self.api_key = llm_api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key

    async def create_variants(self, launch_spec: dict, sources: list):
        # Create 3 headline variants, social posts, and a press release using LLM (OpenAI ChatCompletion)
        product = launch_spec.get("product_name")
        persona = launch_spec.get("persona")
        # Create simple prompt
        prompt = f"""You are a creative marketing AI.
Product: {product}
Persona: {persona}
Sources: {', '.join([s.get('title','') for s in sources[:5]])}
Task: Produce 3 headline variants (short), 3 short tweet threads (3 tweets each), one LinkedIn post (~150 words), and a 150-200 word press release.
Return JSON with fields: headlines, tweets, linkedin, press_release.
"""
        # If OpenAI key not provided, return mocked content
        if not self.api_key:
            return {
                "headlines": [
                    f"{product}: Launching the next-gen solution",
                    f"{product}: Faster. Smarter. For {persona}",
                    f"Introducing {product} — Built for {persona}"
                ],
                "tweets": [
                    [f"Tweet 1 for variant 1 about {product}", "Tweet 2", "Tweet 3"],
                    [f"Tweet 1 for variant 2 about {product}", "Tweet 2", "Tweet 3"],
                    [f"Tweet 1 for variant 3 about {product}", "Tweet 2", "Tweet 3"]
                ],
                "linkedin": f"Introducing {product} — a short LinkedIn post for {persona}.",
                "press_release": f"{product} launches — press release placeholder."
            }

        # Call OpenAI ChatCompletion
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":"You are a marketing copywriter."},
                      {"role":"user","content":prompt}],
            max_tokens=700,
            temperature=0.7
        )
        text = resp["choices"][0]["message"]["content"]
        # We will keep parsing simple: use heuristics to extract content blocks
        # For robustness in production, return structured JSON from LLM
        return {
            "raw": text,
            "headlines": [f"{product} — headline A", f"{product} — headline B", f"{product} — headline C"]
        }
