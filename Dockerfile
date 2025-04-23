FROM python:3.12-slim

# Set environment variables
ENV POETRY_VERSION=1.8.2 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install dependencies sistem
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc curl libpq-dev build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set working directory
WORKDIR /app

# Salin file konfigurasi dan dependencies
COPY pyproject.toml poetry.lock* /app/

# Install dependencies menggunakan Poetry
RUN poetry install --no-root

# Salin semua source code
COPY . /app

# Expose application port
EXPOSE 5000

# Jalankan aplikasi
# Set default command
CMD ["flask", "--app", "app", "run", "--host", "0.0.0.0"]