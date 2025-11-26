# planner_agent.py
import datetime

class PlannerAgent:
    def __init__(self, llm_api_key=None):
        self.llm_api_key = llm_api_key

    def plan(self, launch_spec: dict, variants_content: dict):
        # Simple deterministic planner: generate a 7-day countdown with tasks
        launch_date = launch_spec.get("launch_date")
        try:
            ld = datetime.datetime.fromisoformat(launch_date)
        except Exception:
            ld = datetime.datetime.utcnow() + datetime.timedelta(days=7)

        events = []
        # create a few calendar events
        for i, title in enumerate(["Finalize copy", "QA landing page", "Schedule social", "Press outreach"]):
            dt = ld - datetime.timedelta(days=(7 - i*2))
            events.append({
                "title": title,
                "datetime": dt.isoformat(),
                "owner": (launch_spec.get("team") or ["owner"])[0]
            })
        brief = {
            "headline_suggestion": variants_content.get("headlines", ["Use these headlines"])[0],
            "target_persona": launch_spec.get("persona"),
            "kpis": ["signup conversions", "demo requests", "engagement"]
        }
        return {"brief": brief, "calendar_events": events}
