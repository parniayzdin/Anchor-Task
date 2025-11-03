# AnchorTask
A minimal daily-focus app that helps you anchor your day around one priority. Pick one task, do it, add a one-line reflection, and keep a simple streak going.

## Features
- **One task per day**: set/lock today’s anchor
- **Streaks**: automatic streak counter (+ breaks if you miss a day)
- **Quick reflection**: 140-char note for “what helped / blocked”
- **Gentle nudge**: optional afternoon reminder if not completed
- **History glance**: 14-day ✅/❌ with tiny reflections

## Platform & Tooling
- **Backend**: FastAPI, Python, PostgreSQL (optionally SQLite for dev)
- **Frontend**: React + Vite
- **Dev**: Docker Compose, GitHub Actions, OpenAPI (Swagger UI)

## Getting Started (Docker)
```bash
# clone
git clone https://github.com/<you>/anchor-task.git
cd anchor-task

# env (dev defaults)
cp .env.example .env

# run
docker compose up -d

# backend: http://localhost:8000  (docs: http://localhost:8000/docs)
# frontend: http://localhost:5173  (after installing in /frontend)

<p align="center">Made with ❤️ by Parnia Yazdinia</p>
