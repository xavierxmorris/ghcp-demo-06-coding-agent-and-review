# Workshop: delegate a bounded change and keep the evidence

**Audience:** developers, reviewers, and engineering leads.
**Time:** 60-90 minutes plus cloud-agent queue time.
**Outcome:** an agent-ready issue, a reviewed multi-layer change, and a
defensible merge decision. Do not merge merely because a bot posted a summary.

## 1. Understand the two agents - 8 minutes

The **cloud agent** implements tasks in an isolated GitHub-hosted environment.
The separate **code review** feature examines changes and leaves feedback.
An issue assignment, a review request, and an approval are different events.

Use your own fork or an authorized workshop repository. Confirm the relevant
Copilot policies, Actions availability, and usage budget. The offline fallback
is to prepare the issue and review a local diff; label that as preparation,
not a completed Issue-to-PR run.

Current documentation, checked **2026-09-07**, makes cloud agent available on
all paid Copilot plans. Code review has separate entitlement and policy rules.
Do not assume an unavailable assignee means you need an Enterprise upgrade.

## 2. Triage the starter before assigning a feature - 12 minutes

Read [AGENTS.md](AGENTS.md), [backend/app/main.py](backend/app/main.py),
[backend/app/tasks.py](backend/app/tasks.py), and
[frontend/src/api.js](frontend/src/api.js).

| Starter gap | Why it matters | Bounded repair/evidence |
| --- | --- | --- |
| PATCH reuses `TaskIn` and requires `title` | Checkbox-only updates and the unknown-task test reach validation before lookup | Separate create/patch schemas; valid partial update and missing-ID tests |
| Instructions request 400, implementation defaults to 422 | Generated tests can disagree without a shared contract | Agree and implement the documented error envelope |
| Browser frontend calls port 8000 from a different origin | A working API can still fail in the browser | Explicit local origin allowlist or deliberate Vite proxy and matching request base |
| No committed frontend tests | Locked `npm ci` plus a production build does not establish UI correctness | Create meaningful UI tests and add them to the CI gate |
| HTTP helper does not check `response.ok` | A rejected request may look successful in the UI | Show visible failure and preserve correct state |

Treat these as starter work, not hidden success claims. The backend dependency
ranges are broad; record resolved versions and any collection/import failure.
Do not install a different version silently just to make a demo appear green.

Follow the [README setup](README.md#setup) to create the backend environment
and install both sets of declared dependencies. From `backend`, use
`.\.venv\Scripts\python.exe -m pytest -q` in PowerShell, or
`.venv/bin/python -m pytest -q` on macOS/Linux. From `frontend`, run
`npm test -- --run`; no tests found is missing evidence, not a passing result.

Workflows are protected by this repository's instructions. Make any proposed
workflow change a separately approved task; do not bypass that boundary.

## 3. Write the priority issue as a contract - 12 minutes

Start with [docs/example-issues/01-add-priority.md](docs/example-issues/01-add-priority.md).
Add a small set of acceptance examples and explicitly preserve existing data:

| Scenario | Required behavior |
| --- | --- |
| Existing client omits priority | Created task has `med` |
| Create with `low`, `med`, or `high` | Accepted and returned |
| Create/update with an invalid value | Agreed 400 error envelope; no mutation |
| PATCH priority only | Title and done unchanged |
| PATCH done only | Priority unchanged |
| Filter dropdown set to `high` | Displays high-priority tasks; does not delete or mutate others |
| Reload list | Priority survives reads within the running in-memory process |
| API request fails | UI reports failure rather than showing a success-shaped state |

This store is in-memory: "persist priority" means retain it with the task during
the process lifetime, not durability across restarts.

```text
Add priority end to end using the issue's acceptance table. Keep route handlers
thin and request calls in frontend/src/api.js. Preserve partial-update behavior
and current task IDs. No new backend dependencies, sorting feature, external
webhook, or workflow edits. Add focused backend and frontend tests and update
the README API table. Report any acceptance criterion you cannot demonstrate.
```

Attach baseline failures or their repair PR so the agent does not mistake them
for regressions caused by priority.

## 4. Delegate, inspect, and follow up - 15 minutes

Assign the issue to Copilot where supported. Record the issue URL, agent
session/branch, PR URL, and final commit SHA. Review the session output, not
only the PR description.

Trace one field through the entire change:

```text
request schema -> route -> TaskStore -> response schema
-> frontend request helper -> component state -> filter -> tests
```

Missing any link can produce a convincing but incomplete feature.
Check that a test proves false-to-true **and true-to-false** checkbox updates.

If a correction is needed, use a specific PR comment:

```text
@copilot The priority-only PATCH must preserve title and done. Add a regression
test that creates a completed task, patches only priority, and asserts all
other fields remain unchanged. Do not weaken validation or alter workflows.
```

Wait for the new commit, then evaluate that commit rather than relying on
the previous review.

## 5. Request code review separately - 10 minutes

Use **Reviewers -> Copilot -> Request** on GitHub, or approved repository
automatic-review settings. The committed
[request workflow](.github/workflows/copilot-code-review.yml) is opt-in through
`ENABLE_COPILOT_REVIEW=true`, uses `copilot-pull-request-reviewer[bot]`, and fails
on request errors. Its green status is evidence of a successful request, not
evidence that a review completed. Fork and Dependabot PRs use the approved
manual or repository-managed review path instead.

For each comment, reproduce the issue, accept a supported fix, or record why
the suggestion is not applicable. Code-review comment replies are an audit
trail for humans; current documentation says Copilot does not see or reply to
them. Request cloud-agent work via `@copilot` or request a fresh review.

**Failure drill:** make a deliberately invalid priority request and observe
the actual HTTP status/body and UI state. If the suite stays green while the
UI falsely reports success, add the missing regression before proceeding.

## 6. Make a merge decision - 10 minutes

| Evidence | What it establishes | What it does not |
| --- | --- | --- |
| Green test job with actual tests | Covered assertions passed | Whole application correctness |
| Successful review-request job | Request operation completed | Review completed or findings resolved |
| Copilot review | Additional analysis of a particular revision | Human business acceptance |
| Human approval | An accountable review decision | Deployment or operational readiness |

Copilot approvals are now a public-preview option and are off by default.
When explicitly enabled they can satisfy required approvals. This workshop
does not depend on that policy: require a human decision and real CI evidence.

Keep test logs, the acceptance matrix, a screenshot of filter/error behavior,
the final reviewed SHA, and the rationale for rejected suggestions.
Do not include tokens, webhook secrets, or production records.

## Extension, troubleshooting, and reset

For [due dates](docs/example-issues/02-add-due-dates.md), split the API/UI
feature from scheduled delivery. First specify timezone and overdue boundaries.
Only then design a separately approved job with retries, idempotency, and
secret handling; neither an in-process scheduler nor an env-var name proves
reliable delivery.

If cloud execution is unavailable, complete the same checks locally and record
the missing hosted evidence. Stop only your own foreground app processes.
Leave any draft PR clearly labelled; do not auto-merge or delete a shared branch
as a workshop reset.

## Current sources

Checked **2026-09-07**; GitHub.com features are rolling services:
[cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent),
[code review](https://docs.github.com/en/copilot/concepts/agents/code-review),
[requesting reviews and approvals](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review).
The original stack targets Python 3.11+, FastAPI/Pydantic 2, React 18, and
Vite 5/Vitest 1; record the versions actually resolved for your run.
