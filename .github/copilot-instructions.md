# Copilot Instructions

Repo-wide guidance for Copilot Chat, completions, code review, and the
coding agent.

## Backend (Python / FastAPI)
- Python 3.11+. Type hints everywhere.
- Pydantic v2 for request/response models.
- Validation errors return 400 with a structured `{"error": "...", "field": "..."}` body.
- Tests: `pytest` + `httpx.AsyncClient` for endpoint tests.
- Logging: stdlib `logging` (the project is tiny — don't pull in structlog).

## Frontend (React / Vite)
- Function components, hooks, no class components.
- State: `useState` / `useReducer`. No global state library unless asked.
- Network calls go through `src/api.js`.
- Tests: Vitest + React Testing Library.
- Styling: inline `style={}` is fine for this demo — don't add Tailwind or CSS-in-JS.

## API design
- REST: nouns in paths, verbs in HTTP methods.
- Time fields are ISO-8601 strings on the wire; `datetime` objects in Python.
- Use `Optional[X] | None` consistently.

## Reviews
- When you suggest a code edit, prefer **one-line, mechanical** suggestions
  (GitHub's "commit suggestion" must apply cleanly).
- For architectural suggestions, write a comment, don't push code.
