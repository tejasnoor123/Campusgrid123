# CampusGrid

A campus distributed computing platform. Students submit Python jobs packaged as Docker images that run on other students' idle laptops, sandboxed in Docker containers, across any network.

## Quick Start

```bash
# 1. Clone and configure
git clone https://github.com/your-org/campusgrid
cd campusgrid
cp .env.example .env

# 2. Start everything
docker compose up

# 3. Open the dashboard
open http://localhost:3000

# 4. In a separate terminal, run the node agent
cd agent
pip install -r requirements.txt
cp ../.env.example .env
# Edit .env: set SCHEDULER_URL=http://localhost:8000 and USER_TOKEN from the dashboard
python agent.py
```

## Architecture

```
Student browser → FastAPI scheduler → Redis queue → Node agent (any laptop)
                                                          ↓
                                              Docker container (sandboxed job)
                                                          ↓
                                              Results → Scheduler → Student
```

## Components

| Component | Location | Description |
|-----------|----------|-------------|
| Backend API | `backend/` | FastAPI + PostgreSQL + Redis |
| Scheduler | `backend/services/scheduler.py` | Celery beat task, best-fit matching |
| Node Agent | `agent/` | Python daemon, runs on worker laptops |
| Frontend | `frontend/` | React 18 + Vite + Tailwind |

## Environment Variables

See `.env.example` for all configuration options.

Key variables:
- `SCHEDULER_URL` — public URL of the scheduler (ngrok or Render.com)
- `JWT_SECRET` — secret for signing tokens (change this!)
- `DATABASE_URL` — PostgreSQL connection string
- `REDIS_URL` — Redis connection string

## Public Network Setup

Nodes can be on **any network** — home, college WiFi, mobile hotspot. Only the scheduler needs a public URL.

**Option A — ngrok (dev/demo):**
```bash
ngrok http 8000
# Set SCHEDULER_URL=https://abc123.ngrok.io in agent .env
```

**Option B — Render.com (production):**
1. Push to GitHub
2. New Web Service on render.com → connect repo
3. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add env vars in Render dashboard
5. Set `SCHEDULER_URL=https://your-app.onrender.com` in agent `.env`

## Worker Node Setup

```bash
curl -fsSL https://your-scheduler-url/install.sh | bash
```

Or manually:
```bash
cd agent
pip install -r requirements.txt
# Set SCHEDULER_URL and USER_TOKEN in .env
python agent.py
```

## Running Tests

```bash
pip install -r backend/requirements.txt pytest
export PYTHONPATH=$(pwd)/backend
pytest tests/ -v
```

## Demo Jobs

Three sample jobs are included:

| Job | Image | Resources |
|-----|-------|-----------|
| CSV processing | `demo/csv-process:v1` | Light (1 CPU, 2GB) |
| sklearn training | `demo/sklearn-train:v1` | Medium (2 CPU, 4GB) |
| PyTorch training | `demo/pytorch-train:v1` | ML/GPU (4 CPU, 8GB, GPU) |

Build demo images:
```bash
docker build -t localhost:5000/demo/csv-process:v1 demo/csv/
docker push localhost:5000/demo/csv-process:v1
```
