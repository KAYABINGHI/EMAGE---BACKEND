EMAGE Backend — Revised Work Division (Kiptoo & Moen)
This document splits backend responsibilities between Kiptoo and Moen, accounting for expertise differences and creating a more balanced workload.
General rules

Work in feature branches: feat/<owner>/<short-desc>
Create small PRs (<= 300 lines) and link to an issue
Assign the other developer as reviewer
Use conventional commits: type(scope): subject


Primary areas and owners
1) Authentication & Authorization
Owner: Kiptoo (solo for JWT implementation)
Tasks:

Implement secure login/logout flows and JWT handling in app/routes/auth.py
Build JWT middleware in app/middleware/auth.py (token validation, expiry checks)
Implement refresh token logic with proper expiry
Add password hashing and rate-limiting hooks
Write comprehensive unit tests for auth middleware and route handlers
Document JWT flow for Moen's reference

Acceptance criteria:

All auth endpoints use JWT
Middleware rejects invalid/expired tokens
Tests pass with >80% coverage
Brief JWT explanation doc for team

Timeline: Days 1-5 (critical path)

2) Database & Models
Owner: Moen (primary), Kiptoo (review)
Tasks:

Set up app/db.py with connection pooling and session management
Create base models in app/models/ (user.py, journal.py, mood.py)
Add constraints, indexes, and serialization helpers (to_dict methods)
Initialize Alembic and create initial migrations under migrations/
Test migrations on clean dev DB

Acceptance criteria:

Migrations apply cleanly on fresh DB
All models have proper relationships and constraints
Model tests pass (basic CRUD)

Timeline: Days 1-4 (parallel with auth)

3) Journals Feature
Owner: Kiptoo (full ownership)
Tasks:

Complete CRUD endpoints in app/routes/journals.py
Add request validation (Flask-Marshmallow or Pydantic)
Implement pagination and filtering (by date, tags)
Add permission checks (users can only access their journals)
Write unit and integration tests

Acceptance criteria:

All journal endpoints documented and tested
Permission logic prevents unauthorized access
Pagination works correctly

Timeline: Days 6-9

4) Mood Feature
Owner: Moen (full ownership)
Tasks:

Complete CRUD endpoints in app/routes/mood.py
Implement mood tracking model logic in app/models/mood.py
Add aggregation endpoints for weekly/monthly mood stats
Write tests for aggregation logic and edge cases (missing data, etc.)

Acceptance criteria:

Mood CRUD fully functional
Aggregation endpoints return correct stats
Tests cover happy path and edge cases

Timeline: Days 5-9 (starts after DB is stable)

5) Error Handling & Middleware
Split ownership:

Kiptoo: Auth middleware (app/middleware/auth.py)
Moen: Error handling middleware (app/middleware/errors.py)

Tasks (Moen):

Centralized error handler for common HTTP errors (400, 401, 404, 500)
Consistent JSON response format: {"error": "message", "code": 400}
Request logging middleware (log method, path, status, duration)

Acceptance criteria:

All errors return consistent JSON format
Logs are clear and useful for debugging
No stack traces leaked to client in production

Timeline: Days 5-7

6) Dashboard & Aggregations
Owner: Kiptoo (moved from Moen)
Rationale: Kiptoo knows journals intimately; can build dashboard after journals are complete.
Tasks:

Implement app/routes/dashboard.py to aggregate:

Recent journals count
Mood trends (calls Moen's mood aggregation endpoints)
User activity stats


Optimize queries (use JOINs, avoid N+1)
Add simple caching if needed (Flask-Caching)

Acceptance criteria:

Dashboard returns data within 500ms in dev
Integrates cleanly with journals and mood endpoints

Timeline: Days 10-11

7) Tests & CI
Owners: Both (shared equally)
Tasks:

Create test structure under tests/ (test_auth.py, test_journals.py, test_mood.py)
Each developer writes tests for their own features
Kiptoo: Set up GitHub Actions CI workflow
Moen: Add linting config (flake8, black, isort)
Both: Ensure CI runs tests and linters on all PRs

Acceptance criteria:

CI passes on all PRs
Test coverage >70% on critical paths
Linting enforced automatically

Timeline: Days 10-12 (ongoing)

8) Documentation
Owner: Kiptoo (primary), Moen (review and contributions)
Tasks:

Update README.md with:

Setup steps (virtualenv, dependencies, DB)
Environment variables (.env.example)
Running migrations
Running the app
Running tests


Update settingup.txt with example API requests (curl or Postman)
Add JWT flow explanation for team reference

Acceptance criteria:

New developer can set up and run the app using docs alone
All endpoints documented with example requests

Timeline: Days 12-13

Revised Timeline (3-week sprint with buffer)
Week 1: Foundation

Days 1-2: Environment setup, branching strategy, linting
Days 3-5:

Kiptoo: JWT auth implementation
Moen: Database setup and models



Week 2: Core Features

Days 6-9:

Kiptoo: Journals endpoints (after auth is done)
Moen: Mood endpoints and aggregations (after DB is done)


Days 10:

Both: Start writing tests for their features



Week 3: Integration & Polish

Days 11-12:

Kiptoo: Dashboard implementation
Moen: Error handling refinement
Both: Complete test coverage


Days 13-14:

CI setup (Kiptoo)
Documentation (Kiptoo primary, Moen review)


Day 15: Buffer for bug fixes, cross-review, final testing


Integration & Handoff Points
Auth → All features

Kiptoo completes auth by Day 5
Provides Moen with:

@jwt_required decorator usage examples
get_jwt_identity() helper documentation
Test user tokens for development



DB → Features

Moen completes models by Day 4
Both developers can start building on stable DB schema

Mood → Dashboard

Moen's mood aggregation endpoints must be done by Day 10
Kiptoo calls these endpoints from dashboard


Workload Balance Check
Kiptoo (~ 55% of backend work)

✅ Auth & JWT (complex, security-critical) — 5 days
✅ Journals CRUD — 4 days
✅ Dashboard — 2 days
✅ CI setup — 1 day
✅ Documentation (primary) — 2 days
Total: ~14 days of work

Moen (~ 45% of backend work)

✅ Database & Models — 4 days
✅ Mood CRUD + aggregations — 5 days
✅ Error handling middleware — 2 days
✅ Linting setup — 1 day
✅ Documentation (review/contribute) — 1 day
Total: ~13 days of work

Balance: Much better! Moen avoids JWT complexity and focuses on data layer expertise.

PR & Review Checklist

 Small, focused PR (<300 lines)
 Includes tests (happy path + edge case)
 Adds/updates migrations if models changed
 Updates docs if API changed
 Assigned to other developer for review
 CI passes (tests + linting)


File ownership quick reference
FilePrimary OwnerBackupapp/middleware/auth.pyKiptoo—app/middleware/errors.pyMoenKiptooapp/routes/auth.pyKiptoo—app/routes/journals.pyKiptooMoenapp/routes/mood.pyMoenKiptooapp/routes/dashboard.pyKiptooMoenapp/db.pyMoenKiptooapp/models/user.pyMoenKiptooapp/models/journal.pyKiptooMoenapp/models/mood.pyMoenKiptoomigrations/MoenKiptoo

Key Changes from Original Plan

JWT isolation: Kiptoo owns all JWT logic; Moen uses it as a dependency
Dashboard moved to Kiptoo: Better fit since he owns journals
Error handling to Moen: Balances workload and uses his backend expertise
3-week sprint: Added buffer week for realistic delivery
Clearer handoff points: Auth → Features, Mood → Dashboard
More balanced workload: ~55/45 split vs original ~40/60


Next Steps

Create GitHub issues for each task with owner assignments
Set up project board (To Do, In Progress, Review, Done)
Schedule daily 15-min standups for blockers
Kiptoo: Share JWT learning resources with Moen for future work