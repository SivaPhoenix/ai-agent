# monitor_agent.py
import asyncio
import json
import os
from threading import Thread, Event
import time

class MonitorAgent:
    def __init__(self, tools: dict, checkpoint_store: str = "data/checkpoints.json"):
        self.tools = tools
        self.checkpoint_file = checkpoint_store
        os.makedirs(os.path.dirname(self.checkpoint_file), exist_ok=True)
        # load checkpoints
        try:
            with open(self.checkpoint_file, "r") as f:
                self.checkpoints = json.load(f)
        except Exception:
            self.checkpoints = {}
        self._tasks = {}  # task_id -> control events & thread

    def _save(self):
        with open(self.checkpoint_file, "w") as f:
            json.dump(self.checkpoints, f, indent=2)

    def start_monitoring(self, task_id: str):
        if task_id in self._tasks and not self._tasks[task_id]["stop"].is_set():
            return False
        stop_evt = Event()
        pause_evt = Event()
        t = Thread(target=self._monitor_loop, args=(task_id, stop_evt, pause_evt), daemon=True)
        self._tasks[task_id] = {"thread": t, "stop": stop_evt, "pause": pause_evt}
        t.start()
        return True

    def pause_monitoring(self, task_id: str):
        if task_id not in self._tasks:
            return False
        self._tasks[task_id]["pause"].set()
        # save checkpoint
        self.checkpoints[task_id] = {"paused_at": time.time()}
        self._save()
        return True

    def resume_monitoring(self, task_id: str):
        if task_id not in self._tasks:
            return False
        self._tasks[task_id]["pause"].clear()
        return True

    def stop_monitoring(self, task_id: str):
        if task_id in self._tasks:
            self._tasks[task_id]["stop"].set()
            return True
        return False

    def _monitor_loop(self, task_id: str, stop_evt: Event, pause_evt: Event):
        # demo monitor: poll "health" every 5s
        while not stop_evt.is_set():
            if pause_evt.is_set():
                time.sleep(1)
                continue
            # check endpoint(s) - here we call tools.check_endpoints() if exists
            alerts = []
            try:
                if hasattr(self.tools["search"], "health_check"):
                    alerts = self.tools["search"].health_check()
            except Exception:
                alerts = [{"level":"error","msg":"health check failed"}]
            # persist checkpoint about last check
            self.checkpoints[task_id] = {"last_checked": time.time(), "alerts": alerts}
            self._save()
            time.sleep(5)
