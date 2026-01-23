FROM python:3.11-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
ENV PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml .
RUN uv sync --no-dev

COPY data ./data
COPY app ./app
COPY main.py .

EXPOSE 8000

CMD ["fastapi", "run", "main.py"]
