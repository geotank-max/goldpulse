# GoldPulse Build Stages

- [ ] Stage 1 — Basic FastAPI: GET /api/gold/current with mock data
- [ ] Stage 2 — PostgreSQL: gold_prices table, insert/retrieve historical prices
- [ ] Stage 3 — Historical Graph: Next.js fetches + renders history from FastAPI
- [ ] Stage 4 — Real Data Provider: replace mock with real external gold API
- [ ] Stage 5 — WebSocket: /ws/gold, mock live prices first
- [ ] Stage 6 — Combine Everything: external API -> FastAPI -> Postgres -> WS -> Next.js
- [ ] Stage 7 — Docker: containerize and run via Docker Compose
- [ ] Stage 8 — Testing: pytest with mocked external provider
