# AGENTS.md — Project Charter

This is a full-stack task-tracker demo (FastAPI + React). Tiny on purpose so
agentic changes are easy to follow.

## Layout
- `backend/`  — FastAPI app (`app/main.py`, `app/tasks.py`).
- `frontend/` — Vite + React (`src/App.jsx`).
- Tests live next to the code they cover (`backend/tests/`, `frontend/src/__tests__`).

## How to run things
- Backend tests: `cd backend && pytest -q`
- Backend dev:   `cd backend && uvicorn app.main:app --reload`
- Frontend dev:  `cd frontend && npm install && npm run dev`
- Frontend tests:`cd frontend && npm test`

## Definition of done
1. `pytest -q` passes in `backend/`.
2. `npm test -- --run` passes in `frontend/`.
3. New backend endpoints have a request/response schema and an integration test.
4. README "API" table is updated for any new endpoint.

## Hard rules
- **No new backend dependencies** without an explicit note in the PR description.
- **Do not modify** `.github/workflows/*.yml` without explicit approval in the
  issue body.
- **Do not** hard-code secrets or webhook URLs. Use environment variables.
- Use `zoneinfo` from the stdlib for timezones — never `pytz`.

## House style
- Python 3.11+; type hints on every public function.
- FastAPI route handlers stay thin — business logic in `app/<module>.py`.
- React components: function components + hooks. No class components.
- Frontend network calls go through `src/api.js` (one place to mock in tests).

## When the agent is unsure
Open a PR review comment asking for clarification instead of guessing.
Small, surgical PRs > sprawling ones.
