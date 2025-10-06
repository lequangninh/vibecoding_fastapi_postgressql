# Minimal FastAPI Backend (PostgreSQL + SQLAlchemy 2.0 + psycopg, JWT HS256, Pydantic v2, Alembic)


Supports:
- Register & login (JWT HS256)
- Create posts
- Delete post (owner-only)
- `/me` for user profile + posts
- Pydantic v2 validation
- Clear HTTP errors
- Alembic migrations

## Stack
- FastAPI
- SQLAlchemy 2.x
- **PostgreSQL** (default via `sqlalchemy.url`)
- jose (JWT), passlib+bcrypt for password hashing
- Alembic for migrations
- pytest + httpx for tests

## Quick Start
### 0) Open pgAdmin 4 & connect to your server:
```
-Launch pgAdmin 4.

-In the left “Browser” pane, right-click Servers → Register → Server….

-General tab → Name: e.g., Local Postgres.

-Connection tab:

  Host name/address: localhost

  Port: 5432 (default)

  Maintenance database: postgres

  Username: postgres (or another superuser)

  Password: your real postgres password

-Check Save password? (optional)

-Click Save. You should now see the server expand in the tree.
```

```
Create app database (e.g., fastapi_min) : 

-Expand server → Databases.

-Right-click Databases → Create → Database…

-General:

  Database: fastapi_min

-Click Save.
```
### 1) Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate.bat
pip install -U pip
pip install -e .

# configure env
cp .env.example .env
# edit database_url , jwt_secret and algorithm

# migrate
python -m alembic upgrade head

# run
python -m uvicorn app.main:app --reload
```
Docs: `http://127.0.0.1:8000/docs`

#### Endpoints
- POST `/auth/register`
- POST `/auth/login`
- GET `/me`
- POST `/posts`
- DELETE `/posts/{post_id}`

##### Example curl

```bash
# Register
curl -s -X POST http://localhost:8000/auth/register   -H 'Content-Type: application/json'   -d '{"email":"a@b.com","password":"supersecret"}'

# Login
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login   -H 'Content-Type: application/json'   -d '{"email":"a@b.com","password":"supersecret"}' | jq -r .access_token)

# Create post
curl -s -X POST http://localhost:8000/posts   -H "Authorization: Bearer $TOKEN"   -H 'Content-Type: application/json'   -d '{"title":"Hello","content":"World"}'

# Me
curl -s http://localhost:8000/me -H "Authorization: Bearer $TOKEN"

# Delete post
curl -s -X DELETE http://localhost:8000/posts/1 -H "Authorization: Bearer $TOKEN" -i
```
### 2)Validation & Error Handling
- Email format, password length (>=8), title/body lengths enforced by Pydantic.
- Error codes: 401 invalid creds/token, 403 on deleting others' posts, 404 post not found, 409 email exists.

### 3)Tests
Run all tests (ensure your `sqlalchemy.url` points to a Postgres you control):
```bash
python -m pytest -q
```

## Files
- `app/` Python code
- `alembic/` migration env & versions
- `ERD.md` diagram (Mermaid)
- `prompts.md` **(Vibecoding prompts history, mandatory)**
- `agent_corrections.md` **(Corrections you made to agent outputs)**

## Design Notes

- Entities & relationship

    users and posts with a 1-to-many (User.posts).

    posts.owner_id has a FK → users.id with ON DELETE CASCADE so deleting a user cleans up their posts automatically.

- Primary keys

    Simple INTEGER autoincrement PKs (users.id, posts.id) for speed and straightforward joins.

- Uniqueness & lookups

    users.email is UNIQUE: each account is distinct.

    posts has UNIQUE(owner_id, title): prevents accidental duplicates within the same user while still allowing identical titles across different users.

    Indexes on users.email and posts.owner_id support frequent queries (auth lookups, “my posts”).

- Timestamps

    created_at with DB-side server_default NOW() 


- Auth alignment

    JWT sub stores the user id (stable PK) rather than email, avoiding issues if the email changes.

- Tooling & safety

    Alembic manages schema evolution.

    SQLAlchemy 2.0 declarative mapping keeps models explicit and type-safe.

    DB session via dependency.
