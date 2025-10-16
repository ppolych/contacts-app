# Contacts App – Flask + PostgreSQL + Nginx (Dockerized)

## Quick start

```bash
# 1) Clone your repository (GitHub user: ppolych)
#    git clone https://github.com/ppolych/contacts-app.git
#    cd contacts-app

# 2) Create and adjust .env
cp .env .env.local || true

# 3) Build & run (first boot)
docker compose up -d --build

# 4) App: http://<server-ip>:${PUBLIC_HTTP_PORT}  (default 8210)
```

## Notes
- Each service runs in its own container with its own named volume:
  - `pgdata` (PostgreSQL data)
  - `web_static` (Flask static files)
  - The database is **not** exposed outside the Docker network.
- Nginx is the only public entrypoint (port `${PUBLIC_HTTP_PORT}`).
- All code comments are in English, as requested.
