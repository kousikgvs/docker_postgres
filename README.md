# Local Postgres with Docker

Run PostgreSQL locally with Docker and exercise it with a small Python client that creates a table, inserts a row, and reads the latest rows back.

---

## Project layout

```
app.py               # Sample Python client (psycopg)
docker-compose.yml   # Defines the postgres service
Dockerfile           # Custom Postgres image build context
requirements.txt     # Python dependencies
steps/               # Ad-hoc SQL files (e.g., your_query.sql)
```

## Prerequisites

- Docker Desktop
- Python 3.10+ (only needed for [app.py](app.py))

---

## 1. Start the stack

Build and start Postgres in the background:

```powershell
docker compose up -d --build
```

Postgres is exposed on `localhost:5432` with these defaults (see [docker-compose.yml](docker-compose.yml)):

| Setting  | Value          |
| -------- | -------------- |
| Database | `app_db`       |
| User     | `app_user`     |
| Password | `app_password` |

### Common compose commands

```powershell
docker compose up -d        # start in background
docker compose ps           # check status
docker compose logs -f      # tail logs
docker compose down         # stop & remove containers
docker compose down -v      # also remove the database volume
```

---

## 2. Run SQL from the command line

One-off query:

```powershell
docker exec -it local-postgres psql -U app_user -d app_db -c "SELECT version();"
```

Interactive psql shell:

```powershell
docker exec -it local-postgres psql -U app_user -d app_db
```

Run a SQL file from the host (e.g., [steps/your_query.sql](steps/your_query.sql)):

```powershell
Get-Content .\steps\your_query.sql | docker exec -i local-postgres psql -U app_user -d app_db
```

---

## 3. Run the Python sample client

Install dependencies:

```powershell
py -m pip install -r requirements.txt
```

> If `py` is not available, use `python -m pip install -r requirements.txt`.

Run the script:

```powershell
py app.py
```

[app.py](app.py) will:

- connect to the local Postgres container
- create a `notes` table if it does not exist
- insert one sample row
- read the latest rows and print them

---

## 4. Stop the stack

```powershell
docker compose down        # stop & remove containers
docker compose down -v     # also delete the database volume
```

---

## Appendix: running Postgres without compose

You can also run the custom image directly with `docker run`. The official `postgres` image **requires** `POSTGRES_PASSWORD` — the container won't start without it (unless you set `POSTGRES_HOST_AUTH_METHOD=trust`, which is insecure).

Defaults when env vars are not set explicitly:

- User: `postgres`
- Database: `postgres`
- Password: none → container exits with an error

Build and run:

```powershell
docker build -t my-postgres .
docker run -d --name my-postgres -e POSTGRES_PASSWORD=mysecret -p 5432:5432 my-postgres
```

Then connect with host `localhost`, port `5432`, user `postgres`, password `mysecret`, db `postgres`.

### Freeing port 5432

If a container is already publishing port `5432`, stop it before bringing up compose:

```powershell
docker ps --filter "publish=5432"
docker stop my-postgres
docker rm my-postgres
```
