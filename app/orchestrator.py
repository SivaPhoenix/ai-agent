import asyncio
from agents.research_agent import ResearchAgent
from agents.creative_agent import CreativeAgent
from agents.planner_agent import PlannerAgent
from agents.monitor_agent import MonitorAgent
import time
from utils.helpers import generate_query_variants

class Orchestrator:
    def __init__(self, llm_api_key: str, tools: dict, memory):
        self.llm_api_key = llm_api_key
        self.tools = tools
        self.memory = memory
        self.monitor = MonitorAgent(tools=tools, checkpoint_store="data/checkpoints.json")

    async def run_launch(self, launch_spec: dict, task_id: str, status_callback=None):
        cb = status_callback or (lambda p,m: None)
        cb(0, "Starting launch workflow")

        # 1) Research phase - run parallel search agents with query variants
        cb(5, "Generating search queries")
        variants = generate_query_variants(launch_spec["product_name"], n=3)
        cb(10, f"Executing {len(variants)} parallel research agents")
        research_tasks = [ResearchAgent(self.tools["search"]).run(q) for q in variants]
        research_results = await asyncio.gather(*research_tasks)
        combined_sources = [item for sub in research_results for item in sub]
        cb(30, f"Found {len(combined_sources)} sources")

        # 2) Creative phase - generate variants
        cb(35, "Generating creative content (headlines, posts, press release)")
        creative = CreativeAgent(llm_api_key=self.llm_api_key)
        variants_content = await creative.create_variants(launch_spec, combined_sources)
        cb(60, "Creative content generated")

        # 3) Planner - timeline + tasks
        cb(65, "Planning timeline and tasks")
        planner = PlannerAgent(llm_api_key=self.llm_api_key)
        plan = planner.plan(launch_spec, variants_content)
        cb(80, "Plan created")

        # 4) Optional: schedule (mock)
        cb(85, "Scheduling events (mock calendar)")
        self.tools["calendar"].create_events(plan.get("calendar_events", []))
        cb(90, "Events scheduled")

        # 5) Persist to memory (brief + variants)
        cb(92, "Storing artifacts to memory")
        self.memory.upsert(launch_spec.get("product_name"), {
            "brief": plan.get("brief"),
            "variants": variants_content
        })
        cb(95, "Stored to memory")

        # Final synthesis
        cb(98, "Synthesizing final result")
        result = {
            "task_id": task_id,
            "brief": plan.get("brief"),
            "variants": variants_content,
            "plan": plan,
            "sources": combined_sources
        }
        cb(100, "Completed")
        return result
