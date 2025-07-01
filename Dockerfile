FROM python:3.12-slim AS base

# packages needed for GeoDjango/PostGIS
RUN apt-get update && apt-get install -y --no-install-recommends \
    binutils libproj-dev gdal-bin postgis \
    libgdal-dev libgeos-dev libpq-dev curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# install uv (fast dependency manager)
RUN curl -Ls https://astral.sh/uv/install.sh | sh -s -- v0.7.17 && \
    cp /root/.local/bin/uv /usr/local/bin/uv

# set workdir
WORKDIR /app

# copy dependencies first to leverage Docker cache
COPY pyproject.toml uv.lock* requirements*.txt* ./

ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
RUN uv sync --locked --no-dev

# copy the full project source
COPY . .

WORKDIR /app/geodjango

# expose Django’s default dev port
EXPOSE 8000

# default command (run the development server)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
