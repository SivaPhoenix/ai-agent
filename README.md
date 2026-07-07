### Symphony – AI Product Launch Concierge
### Problem Statement

Launching a product involves many fragmented tasks: researching competitors, generating content, planning timelines, scheduling activities, and monitoring performance. These steps are time-consuming, repetitive, and often require switching between multiple tools.

This results in:

- Slower launch cycles
- Inconsistent messaging
- Missed deadlines
- Poor visibility into launch readiness

Symphony addresses this by automating the end-to-end launch workflow using a coordinated multi-agent AI system.

### Why Agents?

Product launches naturally map to a multi-stage workflow. Each stage requires different skills:

Research → information retrieval
Copywriting → creativity + synthesis
Planning → reasoning + task generation
Monitoring → long-running system checks
A single model cannot perform all of these optimally.

Agents are the ideal solution because they provide:
- Specialization: each agent handles a distinct responsibility
- Parallel execution: multiple research agents run at once
- Sequential reasoning: research → creative → planning → scheduling
- Long-running behavior: monitoring agent continuously checks system health
- Tool integration: agents can call search APIs, calendar APIs, or custom tools
- Memory: storing previous launches improves future outputs

Using agents allows Symphony to automate an entire process—not just one task.

### What I Created (Architecture Overview)

The system consists of a structured multi-agent workflow orchestrated by a FastAPI backend.

1. ResearchAgent (Parallel)

- Executes multiple search queries concurrently
- Collects competitor signals and market insights
- Uses asyncio.gather() for parallel execution

2. CreativeAgent (LLM-Powered)

Generates:

- Headlines
- Tweet threads
- LinkedIn posts
- Press releases

Uses OpenAI (when API key provided), or a fallback mock generator

3. PlannerAgent

- Creates a structured 7-day launch plan
- Assigns tasks and owners
- Prepares calendar events

4. MonitorAgent (Long-Running)

- Runs as a background thread
- Performs periodic health checks
- Supports pause and resume
- Saves state in a checkpoint file

### Memory Layer

A TF-IDF-based VectorStore stores:

- Launch briefs
- Generated content  
- Metadata for future reuse

### Backend Orchestrator

- Coordinates the full pipeline
- Tracks task progress and logs
- Stores final results
- Exposes public API endpoints
- Handles long-running agent lifecycle

### Tools

- MockSearchClient — replaceable with real search APIs
- MockCalendarClient — replaceable with Google Calendar API

### Demo
1. Start a Launch
POST /launch
```
{
	"product_name": "NovaApp",
	"persona": "Growth PM",
	"launch_date": "2025-12-10",
	"team": ["alice", "bob"]
}
```

Response:
```
{
	"task_id": "d8f1a0b3-..."
}
```
2. Check Status
```
GET /status/{task_id}
```
You receive:
Status (queued, running, completed, failed)
Progress %

Latest logs (last 20 entries)

3. Retrieve Final Result
```
GET /result/{task_id}
```

The result includes:
- Launch brief
- Headlines
- Tweet threads
- LinkedIn post
- Press release
- Calendar events
- Competitor insights
- Memory references

4. Start Monitoring
```
POST /monitor/{task_id}/start
```
5. Pause Monitoring
```
POST /monitor/{task_id}/pause
```

### The Build
### Technologies Used

- Python 3.11
- FastAPI for backend orchestration
- AsyncIO for parallel research execution
- Threads for long-running monitoring
- OpenAI API (optional)
- TF-IDF VectorStore for memory
- Docker & docker-compose for deployment
- Environment variables (.env) for configuration

### Key Components

`
/agents → ResearchAgent, CreativeAgent, PlannerAgent, MonitorAgent
/tools → Search + Calendar tool clients
/memory → VectorStore
/orchestrator.py → Agent coordinator
/main.py → API interface
/data/checkpoints.json → Persisted monitor state
`

### What This Demonstrates

- Multi-agent collaboration
- Parallel + sequential agents
- Long-running agent loops
- Custom tool usage
- Memory with stateful recall
- Observability (progress logs + checkpoints)
- Deployment-ready architecture

### If I Had More Time, This Is What I’d Do
1. Real API Integrations

- Google Search API
- Google Calendar API
- Slack or Discord notifications
- Social media posting automation

2. Frontend Dashboard

- Real-time logs via WebSockets
- Calendar timeline visualization
- Editable content workspace

3. Agent-to-Agent Protocol

- Redis pub/sub
- Event-driven communication
- Distributed agent execution
4. Improved Memory

- FAISS or Pinecone vectors
- Embedding-based recall
- Multi-launch knowledge base

5. Rich Evaluation Metrics

- ROUGE/BERTScore auto-evaluation
- Engagement prediction
- Automated draft improvement loops

6. Production Monitoring

- OpenTelemetry traces
- Grafana dashboards
- Prometheus metrics

