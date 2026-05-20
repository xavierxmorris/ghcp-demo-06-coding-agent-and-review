# Demo 06 — Copilot Coding Agent + Copilot Code Review 🤖🔍

> **Difficulty:** ⭐⭐⭐⭐⭐
> **GHCP surfaces:**
> - **Copilot coding agent** — assign an Issue, get a Pull Request back.
> - **Copilot code review** — automatic + on-demand PR review.
> - All the customisation surfaces from Demo 05 (`AGENTS.md`, instructions,
>   prompt files) — they're what make the agent's output match your house style.
> **Stack:** Python FastAPI backend + React/Vite frontend (intentionally tiny).
> **Time:** ~45 minutes (most of which is waiting on the agent)

This is the headline demo: a workflow where you write *issues*, not code.
You'll learn how to set the agent up for success, what to do when it gets
something wrong, and how Copilot code review complements human reviewers.

> 📣 **Important availability note**
> The Copilot coding agent and Copilot code review are **Copilot Business /
> Enterprise** features and may need to be enabled for your org. If you're on
> a personal Copilot plan, you can still walk through the README and use the
> prepared issue templates — just open the PRs yourself.

---

## What you'll learn
1. How to write an **agent-ready issue** (the prompt is the issue body).
2. The full coding-agent loop: Issue → assigned to `@copilot` → draft PR →
   review → merge.
3. How `AGENTS.md` and `.github/copilot-instructions.md` shape what the
   agent produces.
4. Triggering Copilot code review on a PR; pushing back when it's wrong.
5. The handoff: when to take over from the agent yourself.
6. Wiring Copilot review into CI for required checks.

## Prerequisites
- Copilot Business or Enterprise seat with **coding agent** enabled
  (Settings → Copilot → Coding agent → enabled for this repo).
- `gh` CLI authenticated.
- Node 20+ and Python 3.11+ (only if you want to actually run the app).

## Setup
```bash
gh repo clone xavierxmorris/ghcp-demo-06-coding-agent-and-review
cd ghcp-demo-06-coding-agent-and-review

# Optional: run it locally first so you understand what the agent is editing.
(cd backend && python -m venv .venv && source .venv/bin/activate && \
   pip install -r requirements.txt && uvicorn app.main:app --reload) &
(cd frontend && npm install && npm run dev) &
```

---

## Repo anatomy

```
.
├── AGENTS.md                                # "How to be a good agent here"
├── .github/
│   ├── copilot-instructions.md              # House style rules
│   ├── ISSUE_TEMPLATE/
│   │   ├── good-first-issue.md              # designed for the coding agent
│   │   └── bug-report.md
│   └── workflows/
│       ├── ci.yml                           # tests + lint
│       └── copilot-code-review.yml          # auto-request review on PRs
├── backend/
│   ├── app/
│   │   ├── main.py                          # FastAPI app
│   │   └── tasks.py                         # in-memory task store
│   └── tests/
│       └── test_tasks.py
└── frontend/
    └── src/
        └── App.jsx
```

---

## Walkthrough

### Phase 1 — Hand a small task to the coding agent

1. Open the repo on GitHub → **Issues** → **New issue** → pick
   `good-first-issue`.
2. Use this body (it's also saved as `docs/example-issues/01-add-priority.md`):

   > **Title:** Add `priority` field (low|med|high) to tasks
   >
   > **What:** Persist a `priority` field on each task (default `med`). Expose
   > it via GET/POST/PATCH endpoints, render a coloured pill in the frontend
   > task list, and add a filter dropdown in the toolbar.
   >
   > **Acceptance criteria:**
   > - [ ] Backend validates priority against `{low, med, high}`; returns 400
   >   for invalid values.
   > - [ ] All existing tests still pass; new tests cover create/update with
   >   each priority and the invalid case.
   > - [ ] Frontend filter is a dropdown, not separate buttons.
   > - [ ] No new backend dependencies.
   > - [ ] Update README's "API" table.
   >
   > **Out of scope:** sorting by priority (separate issue).

3. **Assign the issue to `@copilot`** (the assignee picker shows Copilot for
   eligible repos).
4. Wait. Copilot creates a draft PR (usually within minutes), pushing commits
   to a `copilot/...` branch. The PR includes a checklist of what it did and
   an explanation of its design choices.

🎯 **Lessons embedded:**
- A *good* agent issue is **scoped, testable, and bounded** — almost a spec.
- `AGENTS.md` told the agent how to run the tests; it'll iterate until they're
  green.
- The agent will refuse / flag changes that violate AGENTS.md rules (it won't
  touch `.github/workflows/*` here without you saying so).

### Phase 2 — Review the agent's PR

When the PR is ready:

1. Read the **PR description** first — it's the agent's own narrative of
   what it did and why.
2. Open **Files changed**. Notice:
   - Types and tests match the conventions in `copilot-instructions.md`.
   - The frontend uses the existing components (it read them).
3. **Comment on a line** like a human PR review:

   > "Use the existing `<Badge>` component instead of inline span styling."

   Submit the comment. The agent will push a follow-up commit responding to
   your feedback.

🎯 **Lesson:** The agent is a *teammate that takes review comments*, not a
one-shot generator. Treat it like an enthusiastic junior dev.

### Phase 3 — Copilot code review on the same PR

If `.github/workflows/copilot-code-review.yml` is enabled, **Copilot review**
posts a structured review automatically when the PR opens. You can also
trigger it manually with the **"Request review from Copilot"** button.

Look for:
- Suggested code edits (one-click "Commit suggestion").
- Risk flags (missing tests, untyped public functions).
- Security smells (hard-coded secrets, SQL string concatenation).

When Copilot review is **wrong** — which it will be sometimes — **resolve the
comment with a one-line reason**. That's the audit trail; future review runs
will see your reasoning.

🎯 **Lesson:** Copilot review is best as a **first pass** that frees humans
to focus on architecture, naming, and business logic — not formatting nits.

### Phase 4 — A harder issue (the agent might struggle)

Open the prepared issue `docs/example-issues/02-add-due-dates.md`:

> Add **due dates** to tasks, including:
> - A timezone-aware backend field (`due_at: datetime | None`).
> - An overdue badge in the frontend.
> - A nightly "overdue summary" job that POSTs to a webhook configured
>   via env var.

Assign to `@copilot`. This one tests:
- Whether the agent picks the right datetime library (`zoneinfo` not `pytz` —
  see instructions).
- Whether it asks before adding a scheduler dependency (it should — AGENTS.md
  forbids unannounced deps).
- How it handles the webhook secret (env var, not hard-coded).

You'll likely need to:
- Comment to push the agent toward a stdlib `sched` loop instead of `APScheduler`.
- Provide a specific webhook payload contract in a follow-up comment.

🎯 **Lesson:** **Iteration is part of the workflow.** Even with great
guardrails, hard problems take 2–3 review cycles. That's still way faster
than writing it yourself — and you learned what to clarify next time.

### Phase 5 — When NOT to use the coding agent

The agent is the wrong tool for:
- **Multi-repo changes** (it works one repo at a time).
- **High-stakes refactors** with subtle semantic changes (use IDE Chat where
  you can iterate locally).
- **Anything that requires running a real database, browser, or production
  data** to verify — the agent's sandbox is limited.

For those, **Copilot CLI** (Demo 04) or IDE Chat (Demos 02/03) are the right
surfaces.

---

## CI integration

`.github/workflows/copilot-code-review.yml` shows the minimal config to
**require** a Copilot review pass before merge. Add the workflow's status
check to your branch protection rules to make it gating.

## Try it yourself

1. Write an issue for a **bug fix** (not a feature). Does the agent
   reproduce, then fix, then add a regression test?
2. Write an **intentionally ambiguous** issue. Does the agent ask
   clarifying questions in a PR comment, or guess?
3. Disable `AGENTS.md` for one issue and see what the agent does without
   it — restore it for the next.
4. Use the **`/pre-commit-review`** prompt file (copy from Demo 05) and
   invoke it via Chat on the agent's PR for a second-opinion review.

## Talking points
- The coding agent is a **force multiplier for backlog grooming**: small,
  well-defined issues become PRs in minutes.
- Quality of output is **directly proportional** to:
  1. Quality of `AGENTS.md` + instructions (Demo 05),
  2. Quality of your issue (the prompt),
  3. Quality of your test suite (what the agent iterates against).
- Copilot code review **doesn't replace human reviewers** — it removes the
  busy-work so humans can do the high-judgement bits.
- Treat agent commits with the same review rigour as any teammate's. The
  agent will sign its commits clearly.

---

## You finished the demo suite 🎉

← back to the [demo index](../)

If you ran all six, you've now touched every major Copilot surface:
completions, Chat, the CLI, customisation, the coding agent, and code review.
The next step is to apply this on **your own** repo — start with Demo 05's
customisation files and grow from there.
