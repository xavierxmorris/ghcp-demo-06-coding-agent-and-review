# Demo 06 — Copilot Coding Agent + Copilot Code Review 🤖🔍

> **Difficulty:** ⭐⭐⭐⭐⭐
> **GHCP surfaces:**
> - **Copilot coding agent** — assign an Issue, get a Pull Request back.
> - **Copilot code review** — automatic + on-demand PR review.
> - Repository instructions from Demo 05 (`AGENTS.md` and
>   `copilot-instructions.md`). Prompt files can be brought across separately.
> **Stack:** Python FastAPI backend + React/Vite frontend (intentionally tiny).
> **Time:** ~45 minutes (most of which is waiting on the agent)

This is the headline demo: a workflow where you write *issues*, not code.
You'll learn how to set the agent up for success, what to do when it gets
something wrong, and how Copilot code review complements human reviewers.

**Go deeper:** [WORKSHOP.md](WORKSHOP.md) adds starter-gap triage, a complete
priority-field acceptance matrix, review follow-up, and a distinction between
CI checks, review requests, and approvals.

> 📣 **Important availability note**
> Checked **7 September 2026**: current GitHub documentation calls the coding
> agent **Copilot cloud agent** and makes it available on all paid Copilot
> plans, subject to policy and repository access. Code review has its own
> availability and billing controls, including eligible personal plans.
> See the workshop's first-party sources rather than assuming Business or
> Enterprise is required for every participant.

---

## What you'll learn
1. How to write an **agent-ready issue** (the prompt is the issue body).
2. The full coding-agent loop: Issue → assigned to `@copilot` → draft PR →
   review → merge.
3. How `AGENTS.md` and `.github/copilot-instructions.md` shape what the
   agent produces.
4. Triggering Copilot code review on a PR; pushing back when it's wrong.
5. The handoff: when to take over from the agent yourself.
6. Distinguishing CI checks, review requests, human approvals, and optional
   Copilot approvals.

## Prerequisites
- An eligible Copilot plan with cloud agent and code review allowed by the
  applicable policies. Use a repository or fork you control for issue creation.
- `gh` CLI authenticated.
- Node 20+ and Python 3.11+ (only if you want to actually run the app).

## Setup
```bash
gh repo clone xavierxmorris/ghcp-demo-06-coding-agent-and-review
cd ghcp-demo-06-coding-agent-and-review

```

Install the declared dependencies before baseline triage. From the repository
root in PowerShell:

```powershell
python -m venv backend\.venv
.\backend\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
npm --prefix frontend ci
```

On macOS/Linux, use `backend/.venv/bin/python` for the virtual-environment
interpreter. The frontend lockfile is committed: use `npm ci` for reproducible
installation and review lockfile changes when intentionally updating dependencies.

Before starting the app, use the workshop's baseline triage. The starter has
known gaps: PATCH uses a create schema requiring `title`; frontend tests are
not committed; browser calls to port 8000 need an explicit cross-origin/proxy
arrangement. The CI starter baseline is not proof these exercises are complete.
Run backend and frontend in separate foreground terminals
once those exercises are addressed.

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
│       ├── ci.yml                           # test jobs; see starter gaps
│       └── copilot-code-review.yml          # historical request-only example
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
   - The frontend follows the actual components and request helper in this repo.
3. **Comment on a line** like a human PR review:

   > "@copilot Keep priority changes in `App.jsx` and network requests in
   > `src/api.js`. Add a test showing that filtering does not mutate tasks."

   Submit the comment with `@copilot` to request a cloud-agent follow-up.
   There is no pre-existing `<Badge>` component in this starter.

🎯 **Lesson:** The agent is a *teammate that takes review comments*, not a
one-shot generator. Treat it like an enthusiastic junior dev.

### Phase 3 — Copilot code review on the same PR

Request review through the PR's **Reviewers** control, or configure automatic
reviews in repository settings. The optional committed workflow uses the
documented `copilot-pull-request-reviewer[bot]` API identity and surfaces request
errors. Enable it only with repository variable `ENABLE_COPILOT_REVIEW=true`
after confirming review availability. Fork and Dependabot PRs are excluded
from this write-token request path. A successful request is still not a completed
review; inspect the PR's actual review and findings.

Look for:
- Suggested code edits (one-click "Commit suggestion").
- Risk flags (missing tests, untyped public functions).
- Security smells (hard-coded secrets, SQL string concatenation).

When Copilot review is **wrong** — which it will be sometimes — **resolve the
comment with a one-line reason**. That is an audit trail for people, not a
promise that Copilot will learn from the reply. Current documentation says
replies to code-review comments are not visible to Copilot. Use `@copilot`
in a PR comment to ask the cloud agent for changes, or request a new review.

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
- Separate the due-date API/UI task from the scheduled-webhook task.
- Specify timezone, delivery retries, duplicate handling, hosting, and secret
  storage before approving an external side effect. A `sched` loop alone does
  not establish a durable production job.

🎯 **Lesson:** **Iteration is part of the workflow.** Even with great
guardrails, hard problems take 2–3 review cycles. That's still way faster
than writing it yourself — and you learned what to clarify next time.

### Phase 5 — When NOT to use the coding agent

The agent is the wrong tool for:
- **Multi-repo changes** (it works one repo at a time).
- **High-stakes refactors** with subtle semantic changes (use IDE Chat where
  you can iterate locally).
- **Tasks requiring unavailable private systems or production data** to verify.
  Do not solve an access gap by exposing credentials or data. Browsers and
  test services are not categorically unavailable; inspect the configured
  environment and keep the task independently testable.

For those, **Copilot CLI** (Demo 04) or IDE Chat (Demos 02/03) are the right
surfaces.

---

## CI integration

Use executable CI checks and repository rules for merge requirements.
Successfully requesting a review is not a quality gate. The shipped workflow
does not wait for a review or assess its findings.

By default Copilot leaves a comment review, not a required approval. Current
GitHub documentation also describes **Copilot approvals in public preview**,
disabled by default, which can count when explicitly enabled by policy.
This lab does not require that preview: retain human approval for the exercise.
Workflow changes require the explicit approval stated in `AGENTS.md`.

The backend CI command is `python -m pytest -q -rxX --starter-baseline`.
Only the known PATCH assertion is a strict expected failure under that flag;
ordinary `pytest` still exposes the exercise. A starter-only assertion also
requires the exact 422/missing-title response, rather than accepting any API
error. Missing tests, other failures and an unexpected pass fail the baseline.
When fixing PATCH, remove `--starter-baseline` from CI and run the ordinary suite.
Frontend CI runs `npm ci` and
`npm run build`, not an empty Vitest suite. Add and require meaningful UI tests
as part of the workshop. Build/test tooling uses patched Vite 6.4.3 and Vitest
3.2.7 rather than the old vulnerable majors.

## API: current starter

| Method/path | Current behavior |
| --- | --- |
| `GET /tasks` | Lists the in-memory tasks |
| `POST /tasks` | Creates `{title, done, id}`; returns 201 |
| `PATCH /tasks/{task_id}` | Uses `TaskIn`, so `title` is currently required; this is the first repair exercise |
| `DELETE /tasks/{task_id}` | Deletes or returns 404; intended success status 204 |

Pydantic request-validation errors use FastAPI's default 422 behavior in this
starter, despite the instructions' desired 400 envelope. Make that discrepancy
an explicit acceptance criterion rather than claiming it is already handled.

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

## Continue the demo suite

Back to the [demo index](https://github.com/xavierxmorris/ghcp-demos).

If you ran demos 01-06, you've completed the foundation track:
completions, Chat, the CLI, customisation, the coding agent, and code review.
The index also includes hosted agents, research, design, reconciliation, and
legacy-modernisation labs.
