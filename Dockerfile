FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
  libpq-dev \
  gcc \
  curl \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install --no-cache-dir poetry

RUN poetry install --no-root

COPY . /app/

EXPOSE 8000 5678

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
