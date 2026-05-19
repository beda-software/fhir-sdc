FROM python:3.11-bullseye
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/
RUN mkdir /app
WORKDIR /app
ENV PYTHONPATH /app
COPY pyproject.toml uv.lock /app/
RUN uv sync --frozen --no-dev
ADD . /app
CMD ["uv", "run", "gunicorn", "main:create_gunicorn_app", "--worker-class", "aiohttp.worker.GunicornWebWorker", "-b", "0.0.0.0:8081"]
EXPOSE 8081
