# EMAGE Backend — Work Breakout (Kiptoo & Moen)

This document splits backend responsibilities between two developers: **Kiptoo** and **Moen**. Use this as a sprint planning guide, PR checklist, and onboarding reference.

## General rules
- Work in feature branches: `feat/<owner>/<short-desc>` (e.g., `feat/kiptoo/auth-refresh`).
- Create small PRs (<= 300 lines) and link to an issue.
- Assign the other developer as reviewer.
- Use conventional commits: `type(scope): subject`.

---

## Primary areas and owners

### 1) Authentication & Authorization
**Owner:** Kiptoo (primary), Moen (backup/review)

Tasks:
- Implement secure login/logout flows and JWT handling in `app/routes/auth.py` and `app/middleware/auth.py`.
- Harden password hashing and add rate-limiting hooks.
- Implement refresh token logic with proper expiry.
- Write unit tests for auth middleware and route handlers.

Acceptance criteria:
- All auth endpoints use JWT; middleware rejects invalid/expired tokens; tests pass.

### 2) Database & Models
**Owner:** Moen (primary), Kiptoo (backup/review)

Tasks:
- Ensure `app/db.py` manages connections and sessions correctly.
- Update models in `app/models/` (journal.py, mood.py, user.py) with constraints and serialization helpers.
- Add and test Alembic migrations under `migrations/`.

Acceptance criteria:
- Migrations apply cleanly; model tests pass and map to DB schema.

### 3) Journals & Mood Feature Endpoints
**Owners:**
- Journals — Kiptoo (primary)
- Mood — Moen (primary)

Tasks (Journals — Kiptoo):
- Complete CRUD endpoints in `app/routes/journals.py`.
- Add request validation, pagination, and permission checks.
- Unit & integration tests.

Tasks (Mood — Moen):
- Complete endpoints in `app/routes/mood.py` and `app/models/mood.py`.
- Implement aggregation endpoints for weekly/monthly mood stats.
- Tests for aggregation and edge cases.

Acceptance criteria:
- Endpoints documented, tested, and validated by the other developer.

### 4) Dashboard & Aggregations
**Owner:** Moen (primary), Kiptoo (support)

Tasks:
- Implement `app/routes/dashboard.py` to aggregate journals and mood data.
- Optimize queries and add simple caching if necessary.

Acceptance criteria:
- Dashboard endpoints return aggregated results with acceptable latency in dev.

### 5) API Stability, Error Handling & Middleware
**Owners:** Both (split and review each other's middleware)

Tasks:
- Add centralized error handling and consistent response formats in `app/middleware/`.
- Ensure request logging is present and useful for debugging.

Acceptance criteria:
- Clear logs, consistent API responses for success and failure.

### 6) Tests, CI, Linting
**Owners:** Both (shared)

Tasks:
- Add unit and integration tests under `tests/` (create if missing).
- Configure CI (GitHub Actions or similar) to run tests and linters on PRs.
- Add linting configs: `flake8`, `black`, `isort`, or preferred tools.

Acceptance criteria:
- CI passes on PRs; tests cover key flows.

### 7) Documentation & Onboarding
**Owner:** Kiptoo (primary doc author), Moen (review)

Tasks:
- Update `README.md` with setup steps (env vars, DB setup, migrations).
- Keep `settingup.txt` accurate and add example API requests.

Acceptance criteria:
- New dev can run the app and migrations using the documented steps.

---

## Milestones & Suggested Timeline (2-week sprint)
- Day 1-2: Setup local dev env, align on branching and PR process, fix linting issues.
- Day 3-6: Core auth flows (Kiptoo) and DB/model fixes + migrations (Moen).
- Day 7-10: Journals endpoints (Kiptoo), Mood & Dashboard (Moen).
- Day 11-12: Tests, CI, docs.
- Day 13-14: Bug fixes, cross-review, merge, retrospective.

---

## Integration & Handoff Points
- Auth tokens: agreed format and header: `Authorization: Bearer <token>`.
- DB migrations: test migrations on a safe dev DB before merging.
- Shared utilities: add `app/utils/` for helpers to avoid duplication.

---

## PR & Review Checklist
- Small, focused PR.
- Includes tests (happy path + one edge case).
- Adds/updates migrations if models changed.
- Updates docs as needed.
- Reviewer: the other dev.

---

## File ownership quick reference
- `app/middleware/auth.py` — Kiptoo
- `app/routes/auth.py` — Kiptoo
- `app/db.py` — Moen
- `app/models/user.py` — Moen
- `app/models/journal.py` — Kiptoo
- `app/models/mood.py` — Moen
- `app/routes/journals.py` — Kiptoo
- `app/routes/mood.py` — Moen
- `app/routes/dashboard.py` — Moen
- `migrations/` — Moen manages migration approval

---

## Next steps
- Create issues for each major task and assign owners.
- Start feature branches and open PRs for incremental work.

---

*If you want, I can: create the GitHub issues from this doc, add a PR template, or update the repo `README.md` with a short excerpt.*
