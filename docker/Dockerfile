FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml /app/
RUN pip install --no-cache-dir -U pip \
 && pip install --no-cache-dir .

COPY . /app

CMD ["bash", "-lc", "alembic upgrade head && python -m app.seed && uvicorn app.main:app --host 0.0.0.0 --port 8000"]