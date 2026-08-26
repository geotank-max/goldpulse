# GoldPulse

A full-stack, open-source real-time gold price tracker, built to learn how
real-time financial-data applications work end-to-end:

External Gold Data Provider → FastAPI → PostgreSQL → WebSocket → Next.js → Interactive Graph

## Stack
- Frontend: Next.js
- Backend: FastAPI
- Database: PostgreSQL
- Real-time: WebSocket
- Deployment: Docker / Docker Compose
- Charts: Recharts

## Status
Repo skeleton only — see `docs/STAGES.md` for the build plan.
Currently on **Stage 1: basic FastAPI endpoint with mock data**.

## Setup (once stages are implemented)
```
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local
docker compose up --build
```
