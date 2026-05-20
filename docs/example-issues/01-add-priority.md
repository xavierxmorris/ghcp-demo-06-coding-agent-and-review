# Example issue 01 — Add `priority` field to tasks

> Paste this as a new issue and assign to `@copilot`.

**Title:** Add `priority` field (low|med|high) to tasks

**What:**
Persist a `priority` field on each task (default `med`). Expose it via
GET/POST/PATCH endpoints, render a coloured pill in the frontend task list,
and add a filter dropdown in the toolbar.

**Acceptance criteria:**
- [ ] Backend validates priority against `{low, med, high}`; returns 400
  with `{"error":"...", "field":"priority"}` for invalid values.
- [ ] All existing tests still pass; new tests cover create/update with
  each priority and the invalid case.
- [ ] Frontend filter is a dropdown, not separate buttons.
- [ ] No new backend dependencies.
- [ ] Update README's "API" table.

**Out of scope:**
- Sorting by priority (separate issue).

**Hints:**
- See `AGENTS.md` for the test commands.
- The frontend's network layer is `frontend/src/api.js` — keep all fetch
  calls there.
