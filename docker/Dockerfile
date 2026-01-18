FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml /app/
RUN pip install --no-cache-dir -U pip \
 && pip install --no-cache-dir .

COPY . /app

CMD ["bash", "-lc", "alembic upgrade head && fastapi dev --port 8080 --host 0.0.0.0"]