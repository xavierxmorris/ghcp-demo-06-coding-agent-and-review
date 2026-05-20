# Example issue 02 — Add due dates + overdue summary job (harder)

> Paste this as a new issue and assign to `@copilot`. This one is intentionally
> harder so you can practice iterating with the agent.

**Title:** Add due dates to tasks, with overdue badge + nightly summary

**What:**
1. Add an optional, timezone-aware `due_at` field to tasks.
2. Expose it via existing endpoints. ISO-8601 strings on the wire.
3. Frontend: show an "Overdue" red badge next to any task whose `due_at` is
   in the past and `done == false`. Use the user's local timezone.
4. Add a backend mechanism that, once a day at 09:00 UTC, POSTs a JSON
   summary of overdue tasks to a webhook URL read from `OVERDUE_WEBHOOK_URL`.

**Acceptance criteria:**
- [ ] `zoneinfo` (stdlib) is used for timezone handling — NOT `pytz`.
- [ ] Webhook URL is read from env; never logged in plaintext.
- [ ] If no webhook is configured, the job logs a warning and does nothing.
- [ ] Tests cover: serialisation, the overdue computation, and the
  payload format the webhook receives (mock the network call).
- [ ] No new backend dependencies WITHOUT discussion in a PR comment first.
  (The stdlib `sched` module plus a background thread is acceptable; do
  NOT introduce `APScheduler`, `Celery`, etc., unless the maintainer agrees.)
- [ ] README "API" table updated.

**Out of scope:**
- A real cron / external scheduler.
- A UI to set the webhook URL.

**Hints:**
- See `AGENTS.md` for the `zoneinfo`-only rule.
- Look at how `TaskStore` is already structured before deciding where the
  overdue logic should live.
