# Vibecoding Prompts History

> COMPLETE history of prompts I issued to the Vibecoding agent during development.

---

## 1. Kickoff (PostgreSQL-first)
**Prompt:**  
"Build a minimal FastAPI backend that uses **PostgreSQL** (SQLAlchemy 2.0 only psycopg), supports registration/login with JWT (HS256), creating posts, deleting only the owner's post, and /me to fetch the user's profile & posts. Add Pydantic v2 validation, clear HTTP errors, and Alembic migrations."

**Agent Output:**  
Proposed app structure and JWT approach with jose and bcrypt.
Missing: some installed libraries are missing , not ensure source to postgresql db, initial version missed unique constraint, config.py is missing

---
## 2. config.py
**Prompt:**  create config.py with class Settings(BaseSettings) and in the class Settings add class Config 
**Agent Output:** config.py

---
## 3. Data Model & Constraints
**Prompt:**  
"Add `UNIQUE(owner_id,title)` and timestamps"

**Agent Output:**  
Models created 

---

## 4. Alembic + Config Unification
**Prompt:**  
"Update Alembic env to read `database_url` from the app settings so app and migrations always use the same DSN."

**Agent Output:**  
Added `from app.config import settings` and `config.set_main_option('sqlalchemy.url', settings.database_url)`.

---

## 5. Tests
**Prompt:**  
"Write pytest tests for register, duplicate register, login ok/bad, `/me`, create/delete post, forbid deleting others. Use Postgres and recreate schema before and after each test for isolation."

**Agent Output:**  
Provided tests using TestClient and schema recreation hooks.

---

## 6. Documentation
**Prompt:**  
"Write README with Postgres, Alembic usage, curl examples, and ERD in Mermaid."

**Agent Output:**  
Delivered outline, refined wording for clarity.
