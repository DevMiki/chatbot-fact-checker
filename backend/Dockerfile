FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir "uv==0.2.18"

COPY pyproject.toml ./
COPY uv.lock ./

RUN uv sync --no-dev \
  && ./.venv/bin/python -m ensurepip --upgrade \
  && ./.venv/bin/python -m pip install --no-cache-dir "httpx==0.27.2"

COPY app ./app

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
