# GeoDjangoPOC

## Getting Started (Development)

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd GeoDjangoPOC
```

---

### 2. Set Up Your Python Environment

**Install [uv](https://github.com/astral-sh/uv) if you haven’t already:**

```sh
curl -Ls https://astral.sh/uv/install.sh | sh
```

**Create and sync your Python environment (this will create `.venv` automatically if needed):**

```sh
uv sync
```

This reads from `pyproject.toml` and installs all required dependencies into a local `.venv`.

**To activate the environment:**

```sh
source .venv/bin/activate
```

---

### 3. Create and Configure Your `.env` File

Create a `.env` file in the project root (same directory as `docker-compose.yml`) and define your dev db/creds:

```ini
DB_NAME=
DB_USER=
DB_PASSWORD=
```

This will be used by docker-compose and settings.py

---

### 4. Start the PostGIS Database with Docker Compose

Ensure Docker Desktop is running.

Then spin up the database container:

```sh
docker compose up -d
```

This launches a PostgreSQL/PostGIS database on `localhost:5432` using the credentials from your `.env`.

---

### 5. Run Django Migrations

With your virtual environment activated and dev db container running:

```sh
python manage.py makemigrations
python manage.py migrate
```

---

### 6. Create a Superuser for Admin Access

```sh
python manage.py createsuperuser
```

Follow the prompts to configure your admin account.

---

### 7. Run the Development Server

```sh
python manage.py runserver
```

---

### 8. Access the Application

- **Admin Portal:**  
  [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

- **Home Page (Sample Locations Table as of now):**  
  [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

- **Sample Locations API Endpoint Example:**  
  [http://127.0.0.1:8000/api/samplelocations/samplelocations](http://127.0.0.1:8000/api/samplelocations/samplelocations)

---

### 9. Stopping the Database

To shut down the PostGIS container:

```sh
docker compose down
```

---

## Notes

- `uv sync` automatically creates a `.venv` and installs dependencies from `pyproject.toml`.
- Make sure your `.env` DB credentials match your `docker-compose.yml` and Django settings.
- You must have Docker Desktop running before using `docker compose`.
- PostgreSQL must be running before Django can connect to it.

---