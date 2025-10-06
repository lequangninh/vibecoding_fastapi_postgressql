# Corrections Log (Vibecoding Output Reviews)

This log documents every time Vibecoding's output was suboptimal and what I changed.

---


## 1) Unique Constraint Omission
- **Problem:** Agent initially omitted `UNIQUE(owner_id, title)` from the migration.
- **Fix:** Added `sa.UniqueConstraint('owner_id', 'title', name='uq_owner_title')` and mirrored it in the ORM.
- **Why Better:** Prevents accidental duplicate post titles per user; aligns migration and ORM for integrity.

##) 2) config.py missing
- **Problem:** Security: don't keep secrets in .env/system env;  commit them to source. / it's difficult to find where is needed to change: DB URL, JWT secret, token expiry, etc
- **Fix:**  create config.py with class Settings(BaseSettings) and in the class Settings add class Config
- **Why Better:** keep secrets in .env/system env; never commit them to source / One place to change things: DB URL, JWT secret, token expiry, etc./ Consistency: Alembic, the API app, and tests all use the same settings.database_url

## 3) Alembic/App URL Drift
- **Problem:** Agent left Alembic reading `alembic.ini` while the app read env vars; DSNs could drift.
- **Fix:** In `alembic/env.py`, imported `settings` and set `config.set_main_option("sqlalchemy.url", settings.database_url)`.
- **Why Better:** One source of truth for DB URL avoids "works locally, fails in CI" scenarios.

## 4) Test Isolation Strategy
- **Problem:** Early test draft relied on default DB state.
- **Fix:** Introduced fixtures that drop/create all tables before and after each test.
- **Why Better:** Deterministic tests and no bleed-over between cases, even on a shared dev DB.




