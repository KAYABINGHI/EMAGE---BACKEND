# EMAGE Backend — Revised Work Division (Kiptoo & Moen)

This README documents the revised backend work division, rules, timelines, and acceptance criteria for the EMAGE backend project. It's a condensed, actionable version of `WORK_BREAKOUT.md` tailored for quick onboarding and task assignment.

## Table of Contents

- [General Rules](#general-rules)
- [Primary Areas & Owners](#primary-areas--owners)
  - [1) Authentication & Authorization](#1-authentication--authorization)
  - [2) Database & Models](#2-database--models)
  - [3) Journals Feature](#3-journals-feature)
  - [4) Mood Feature](#4-mood-feature)
  - [5) Error Handling & Middleware](#5-error-handling--middleware)
  - [6) Dashboard & Aggregations](#6-dashboard--aggregations)
  - [7) Tests & CI](#7-tests--ci)
  - [8) Documentation](#8-documentation)
- [Revised Timeline](#revised-timeline)
- [Integration & Handoff Points](#integration--handoff-points)
- [Workload Summary](#workload-summary)
- [PR & Review Checklist](#pr--review-checklist)
- [File Ownership Quick Reference](#file-ownership-quick-reference)
- [Next Steps](#next-steps)


## General Rules

- Work in feature branches: `feat/<owner>/<short-desc>`
- Create small PRs (<= 300 lines) and link to an issue
- Assign the other developer as reviewer
- Use conventional commits: `type(scope): subject`


## Primary Areas & Owners

### 1) Authentication & Authorization

- Owner: Kiptoo (solo for JWT implementation)

Tasks:
- Implement secure login/logout flows and JWT handling in `app/routes/auth.py`
- Build JWT middleware in `app/middleware/auth.py` (token validation, expiry checks)
- Implement refresh token logic with proper expiry
- Add password hashing and rate-limiting hooks
- Write unit tests for auth middleware and route handlers
- Document JWT flow for team reference

Acceptance criteria:
- All auth endpoints use JWT
- Middleware rejects invalid/expired tokens
- Tests pass with >80% coverage
- Provide a short JWT explanation doc

Timeline: Days 1–5 (critical path)


### 2) Database & Models

- Owner: Moen (primary), Kiptoo (review)

Tasks:
- Set up `app/db.py` with connection pooling and session management
- Create base models in `app/models/` (`user.py`, `journal.py`, `mood.py`)
- Add constraints, indexes, and `to_dict` serialization helpers
- Initialize Alembic and create initial migrations under `migrations/`
- Test migrations on a clean dev DB

Acceptance criteria:
- Migrations apply cleanly on a fresh DB
- All models have proper relationships and constraints
- Model tests pass (basic CRUD)

Timeline: Days 1–4 (parallel with auth)


### 3) Journals Feature

- Owner: Kiptoo (full ownership)

Tasks:
- Complete CRUD endpoints in `app/routes/journals.py`
- Add request validation (Flask-Marshmallow or Pydantic)
- Implement pagination and filtering (by date, tags)
- Add permission checks so users can only access their journals
- Write unit and integration tests

Acceptance criteria:
- All journal endpoints documented and tested
- Permission logic prevents unauthorized access
- Pagination works correctly

Timeline: Days 6–9


### 4) Mood Feature

- Owner: Moen (full ownership)

Tasks:
- Complete CRUD endpoints in `app/routes/mood.py`
- Implement mood model logic in `app/models/mood.py`
- Add aggregation endpoints for weekly/monthly mood stats
- Write tests for aggregation logic and edge cases (missing data)

Acceptance criteria:
- Mood CRUD fully functional
- Aggregation endpoints return correct stats
- Tests cover happy paths and edge cases

Timeline: Days 5–9 (starts after DB is stable)


### 5) Error Handling & Middleware

Split ownership:
- Kiptoo: Auth middleware (`app/middleware/auth.py`)
- Moen: Error handling middleware (`app/middleware/errors.py`)

Tasks (Moen):
- Centralized error handler for common HTTP errors (400, 401, 404, 500)
- Consistent JSON response format: `{ "error": "message", "code": 400 }`
- Request logging middleware (method, path, status, duration)

Acceptance criteria:
- All errors return consistent JSON format
- Logs are clear and useful for debugging
- No stack traces leaked to clients in production

Timeline: Days 5–7


### 6) Dashboard & Aggregations

- Owner: Kiptoo
- Rationale: Kiptoo owns journals and will integrate mood aggregations

Tasks:
- Implement `app/routes/dashboard.py` to aggregate:
  - Recent journals count
  - Mood trends (calls Moen's mood aggregation endpoints)
  - User activity stats
- Optimize queries (JOINs, avoid N+1)
- Add simple caching if needed (e.g., Flask-Caching)

Acceptance criteria:
- Dashboard returns data within 500ms in dev
- Integrates cleanly with journals and mood endpoints

Timeline: Days 10–11


### 7) Tests & CI

- Owners: Both (shared)

Tasks:
- Create test structure under `tests/` (`test_auth.py`, `test_journals.py`, `test_mood.py`)
- Each developer writes tests for their features
- Kiptoo: Set up GitHub Actions CI workflow
- Moen: Add linting config (flake8, black, isort)
- Ensure CI runs tests and linters on all PRs

Acceptance criteria:
- CI passes on all PRs
- Test coverage >70% on critical paths
- Linting enforced automatically

Timeline: Days 10–12 (ongoing)


### 8) Documentation

- Owner: Kiptoo (primary), Moen (review)

Tasks:
- Update `README.md` with:
  - Setup steps (virtualenv, dependencies, DB)
  - Environment variables (`.env.example`)
  - Running migrations
  - Running the app
  - Running tests
- Update `settingup.txt` with example API requests (curl or Postman)
- Add JWT flow explanation for team reference

Acceptance criteria:
- New developer can set up and run the app using docs alone
- All endpoints documented with example requests

Timeline: Days 12–13


## Revised Timeline (3-week sprint with buffer)

Week 1 — Foundation
- Days 1–2: Environment setup, branching strategy, linting
- Days 3–5:
  - Kiptoo: JWT auth implementation
  - Moen: Database setup and models

Week 2 — Core Features
- Days 6–9:
  - Kiptoo: Journals endpoints (after auth)
  - Moen: Mood endpoints and aggregations (after DB)
- Day 10: Both start writing tests for their features

Week 3 — Integration & Polish
- Days 11–12:
  - Kiptoo: Dashboard implementation
  - Moen: Error handling refinement
  - Both: Complete test coverage
- Days 13–14:
  - CI setup (Kiptoo)
  - Documentation (Kiptoo primary, Moen review)
- Day 15: Buffer for fixes and final testing


## Integration & Handoff Points

- Auth → All features
  - Kiptoo completes auth by Day 5 and provides:
    - `@jwt_required` decorator usage examples
    - `get_jwt_identity()` helper docs
    - Test user tokens for development

- DB → Features
  - Moen completes models by Day 4 so both devs have a stable schema

- Mood → Dashboard
  - Moen's mood aggregation endpoints must be ready by Day 10 for dashboard integration


## Workload Summary

- Kiptoo (~55%): Auth (5d), Journals (4d), Dashboard (2d), CI (1d), Docs (2d)
- Moen (~45%): DB & Models (4d), Mood (5d), Error handling (2d), Linting (1d), Docs review (1d)


## PR & Review Checklist

- Small, focused PR (<300 lines)
- Includes tests (happy path + edge case)
- Adds/updates migrations if models changed
- Updates docs if API changed
- Assigns the other developer as reviewer
- CI passes (tests + linting)


## File Ownership Quick Reference

- `app/middleware/auth.py` — Kiptoo
- `app/middleware/errors.py` — Moen (backup: Kiptoo)
- `app/routes/auth.py` — Kiptoo
- `app/routes/journals.py` — Kiptoo (backup: Moen)
- `app/routes/mood.py` — Moen (backup: Kiptoo)
- `app/routes/dashboard.py` — Kiptoo (backup: Moen)
- `app/db.py` — Moen (backup: Kiptoo)
- `app/models/user.py` — Moen (backup: Kiptoo)
- `app/models/journal.py` — Kiptoo (backup: Moen)
- `app/models/mood.py` — Moen (backup: Kiptoo)
- `migrations/` — Moen (backup: Kiptoo)


## Next Steps

- Create GitHub issues for each task and assign owners
- Set up a project board (To Do, In Progress, Review, Done)
- Schedule daily 15-min standups to surface blockers
- Kiptoo: Share JWT learning resources and examples with Moen


---

If you'd like, I can also:
- Create the GitHub Issues and a project board skeleton (requires access)
- Add a `.github/workflows/ci.yml` template for running tests
- Create simple skeleton tests under `tests/` to bootstrap CI

Tell me which of those you'd like next, or ask me to adjust the README's tone/format.