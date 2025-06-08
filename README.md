# DRF Assignment

## What it does

This project is a Django REST Framework (DRF) application that provides APIs for managing loans and customers.
It includes features like:

- JWT-based authentication
- Data seeding via a script (`upload.py`) that loads sample loan and customer data
- Dockerized setup for easy deployment and development

---

## How to run with Docker Compose

1. Clone the repo and navigate into it:

```bash
git clone https://github.com/sasank-pankam/DRF-Assignment.git
cd DRF-Assignment
```

2. Run the whole app (Django + PostgreSQL) using Docker Compose:

Configure the env variables in `docker-compose.yaml` file

```bash
docker-compose up --build
```

3. The API server will start on [http://localhost:8000](http://localhost:8000)

4. To seed initial data, the `upload.py` script runs automatically after migrations (if set up), or run manually:

```bash
docker exec -it <container_name> python manage.py shell < upload.py
```

---

## Curl Commands to Use the API

### Get JWT Token

```bash
curl -X POST http://localhost:8000/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "guest", "password": "guest"}'
```

This returns a JSON response with `access` and `refresh` tokens.

### Refresh JWT Token

```bash
curl -X POST http://localhost:8000/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<your_refresh_token>"}'
```

### Access Protected API Endpoint Example

Use the `access` token received above:

```bash
curl -X GET -H "Authorization: Bearer <your_access_token>" http://localhost:8000/api/view-loan/<loan_id>
```

---

## Important Note on Users and JWT Authentication

- The users who authenticate via JWT **must exist in Django’s default `auth_user` table**.
- For example, the username `"guest"` used in the curl command should be a valid user in your Django database with the correct password set.
