FROM python:3.11-slim-bookworm AS builder
ENV VIRTUAL_ENV=/opt/venv \
    PIP_NO_CACHE_DIR=1
RUN pip install pipenv==2026.8.0 && python -m venv $VIRTUAL_ENV
WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy \
    && $VIRTUAL_ENV/bin/python -m pip uninstall -y pip setuptools

FROM python:3.11-slim-bookworm
# Packaging tools are unused at runtime and only add CVE scanner findings.
RUN python -m pip uninstall -y pip setuptools wheel packaging \
    && useradd --system --uid 10001 appuser
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PATH=/opt/venv/bin:$PATH
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY . /app
USER appuser
EXPOSE 8081
CMD ["gunicorn", "main:create_gunicorn_app", "--worker-class", "aiohttp.worker.GunicornWebWorker", "-b", "0.0.0.0:8081"]
