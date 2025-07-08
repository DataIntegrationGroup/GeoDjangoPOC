# GeoDjangoPOC

## Getting Started (Development)

### 1. Clone the Repository and cd into root

```sh
cd GeoDjangoPOC
```

---

### 2. Create and Configure Your `.env` File

Create a `.env` file in the project root (same directory as `docker-compose.yml`) and define your dev db/creds:

```ini
DB_NAME=
DB_USER=
DB_PASSWORD=
```

---

### 3. Build and Start the Dockerized App

Make sure Docker Desktop is running, then build and start the containers in detached mode:

```sh
docker compose up -d --build
```

This launches both the PostGIS database and the Django app.

---

### 4. Run Django Management Commands

To run Django management commands inside the running container, for example use:

```sh
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py seed_samplelocations
```

You can replace `makemigrations`, `migrate`, etc. with any Django command as needed.

---

### 5. Access the Application

- **Admin Portal:**  
  [http://localhost:8000/admin/](http://localhost:8000/admin/)

- **Home Page:**  
  [http://localhost:8000/](http://localhost:8000/)

- **API Docs:**  
  [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

- **Sample Locations API Endpoint Example:**  
  [http://localhost:8000/api/samplelocations/](http://localhost:8000/api/samplelocations/)

---

### 6. Stopping the App and Database

To shut down all containers:

```sh
docker compose down
```

To also remove volumes (for a clean slate - this will delete your db storage):

```sh
docker compose down -v
```

---

## Notes

- You do **not** need to install Python, GDAL, or PostGIS locally—**everything runs in Docker**.
- All Django/Python commands should be run using `docker compose exec web python manage.py ...`.
- Make sure your `.env` DB credentials match your `docker-compose.yml` and Django settings.
- Docker Desktop must be running before using `docker compose`.
- The database service must be healthy before Django can connect.