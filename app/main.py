from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from orchestrator import Orchestrator
from memory.vector_store import VectorStore
from tools.mock_search import MockSearchClient
from tools.calendar_client import MockCalendarClient
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Symphony Launch Concierge - MVP")

# Global orchestrator & stores (in-memory for MVP)
vector_store = VectorStore()
search_client = MockSearchClient()
calendar_client = MockCalendarClient()
orchestrator = Orchestrator(llm_api_key=os.getenv("OPENAI_API_KEY"), tools={
    "search": search_client,
    "calendar": calendar_client
}, memory=vector_store)

# Task registry
TASKS = {}  # task_id -> task info {status, progress, result, background_task}

class LaunchSpec(BaseModel):
    product_name: str
    persona: str
    launch_date: str  # ISO date string preferred
    team: list = []

@app.post("/launch")
async def launch(spec: LaunchSpec, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    TASKS[task_id] = {"status": "queued", "progress": 0, "logs": [], "result": None}
    # run orchestrator in background
    background_tasks.add_task(run_orchestrator_task, task_id, spec.dict())
    return {"task_id": task_id}

async def run_orchestrator_task(task_id: str, spec: dict):
    TASKS[task_id]["status"] = "running"
    try:
        result = await orchestrator.run_launch(spec, task_id, status_callback=make_status_cb(task_id))
        TASKS[task_id]["status"] = "completed"
        TASKS[task_id]["result"] = result
        TASKS[task_id]["progress"] = 100
    except Exception as e:
        TASKS[task_id]["status"] = "failed"
        TASKS[task_id]["logs"].append(f"error: {e}")
        raise

def make_status_cb(task_id):
    def cb(percent: int, message: str):
        TASKS[task_id]["progress"] = percent
        TASKS[task_id]["logs"].append(message)
    return cb

@app.get("/status/{task_id}")
def status(task_id: str):
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="task_id not found")
    return {
        "task_id": task_id,
        "status": TASKS[task_id]["status"],
        "progress": TASKS[task_id]["progress"],
        "logs": TASKS[task_id]["logs"][-20:]
    }

@app.get("/result/{task_id}")
def result(task_id: str):
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="task_id not found")
    if TASKS[task_id]["status"] != "completed":
        raise HTTPException(status_code=400, detail="Result not ready")
    return TASKS[task_id]["result"]

# Monitor control endpoints
@app.post("/monitor/{task_id}/start")
async def start_monitor(task_id: str):
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="task_id not found")
    ok = orchestrator.monitor.start_monitoring(task_id)
    return {"started": ok}

@app.post("/monitor/{task_id}/pause")
async def pause_monitor(task_id: str):
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="task_id not found")
    ok = orchestrator.monitor.pause_monitoring(task_id)
    return {"paused": ok}
