from typing import Dict

def auth_header(token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {token}"}

def register(client, email="alice@example.com", password="supersecret") -> str:
    r = client.post("/auth/register", json={"email": email, "password": password})
    assert r.status_code == 201, r.text
    return r.json()["access_token"]

def login(client, email, password) -> str:
    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    return r.json()["access_token"]

def test_register_success(client):
    r = client.post("/auth/register", json={"email": "user1@example.com", "password": "supersecret"})
    assert r.status_code == 201
    data = r.json()
    assert "access_token" in data and data["access_token"]
    assert data["token_type"] == "bearer"

def test_register_duplicate_email(client):
    payload = {"email": "dupe@example.com", "password": "supersecret"}
    r1 = client.post("/auth/register", json=payload)
    assert r1.status_code == 201
    r2 = client.post("/auth/register", json=payload)
    assert r2.status_code == 409
    assert r2.json()["detail"] == "Email already registered"

def test_login_ok_and_bad(client):
    email = "bob@example.com"
    pwd = "supersecret"
    client.post("/auth/register", json={"email": email, "password": pwd})
    ok = client.post("/auth/login", json={"email": email, "password": pwd})
    assert ok.status_code == 200
    bad = client.post("/auth/login", json={"email": email, "password": "wrongpass"})
    assert bad.status_code == 401
    assert bad.json()["detail"] == "Invalid email or password"

def test_me_returns_profile_and_posts(client):
    token = register(client, email="me@example.com")
    # create a couple posts
    for i in range(2):
        r = client.post("/posts", headers=auth_header(token), json={"title": f"T{i}", "content": "Body"})
        assert r.status_code == 201
    me = client.get("/me", headers=auth_header(token))
    assert me.status_code == 200
    data = me.json()
    assert data["user"]["email"] == "me@example.com"
    assert isinstance(data["posts"], list) and len(data["posts"]) == 2

def test_create_and_delete_post(client):
    token = register(client, email="poster@example.com")
    r = client.post("/posts", headers=auth_header(token), json={"title": "Hello", "content": "World"})
    assert r.status_code == 201, r.text
    post = r.json()
    assert post["title"] == "Hello"
    # Deleting
    d = client.delete(f"/posts/{post['id']}", headers=auth_header(token))
    assert d.status_code == 204

def test_forbid_deleting_others_post(client):
    token_a = register(client, email="a@example.com")
    token_b = register(client, email="b@example.com")
    # A creates
    r = client.post("/posts", headers=auth_header(token_a), json={"title": "Unique", "content": "text"})
    assert r.status_code == 201
    post_id = r.json()["id"]
    # B tries to delete
    d = client.delete(f"/posts/{post_id}", headers=auth_header(token_b))
    assert d.status_code == 403
    assert d.json()["detail"] == "Forbidden: not the post owner"


