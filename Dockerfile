# Multi-stage build on a slim, security-patched base.
#
# python:3.11-bullseye (Debian 11 "oldstable") ships a large buildpack base
# (including an ImageMagick/perl toolchain this service never uses) and carries a
# substantial backlog of fixable OS CVEs. This rebases onto python:3.11-slim-bookworm
# (Debian 12), confines the build toolchain to a builder stage, keeps only the
# runtime shared libraries, and runs as a non-root user.
FROM python:3.11-slim-bookworm AS builder
ENV PIPENV_VENV_IN_PROJECT=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libxml2-dev \
        libxslt1-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pipenv
WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy

FROM python:3.11-slim-bookworm
ENV PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/app/.venv/bin:$PATH
RUN apt-get update && apt-get install -y --no-install-recommends \
        libxml2 \
        libxslt1.1 \
        libpq5 \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*
# The base image's bundled pip/setuptools/wheel under /usr/local are unused at
# runtime (the app runs from /app/.venv) and only add fixable CVE surface.
RUN rm -rf /usr/local/lib/python3.11/site-packages/setuptools* \
           /usr/local/lib/python3.11/site-packages/pkg_resources \
           /usr/local/lib/python3.11/site-packages/wheel* \
           /usr/local/lib/python3.11/site-packages/pip* \
           /usr/local/lib/python3.11/site-packages/_distutils_hack \
           /usr/local/lib/python3.11/site-packages/distutils-precedence.pth \
           /usr/local/bin/pip /usr/local/bin/pip3 /usr/local/bin/wheel
RUN useradd --system --uid 10001 --create-home appuser
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
# pip is not used at runtime; drop it from the venv too (its bundled _vendor
# pins old packages that scanners flag though nothing runtime-reachable uses them).
RUN rm -rf /app/.venv/lib/python3.11/site-packages/pip \
           /app/.venv/lib/python3.11/site-packages/pip-*.dist-info \
           /app/.venv/lib/python3.11/site-packages/pip-*.virtualenv \
           /app/.venv/bin/pip /app/.venv/bin/pip3 /app/.venv/bin/pip3.11
COPY . /app
USER appuser
EXPOSE 8081
# Invoke gunicorn via the venv interpreter so it does not depend on the
# console-script shebang path baked at build time.
CMD ["/app/.venv/bin/python", "-m", "gunicorn", "main:create_gunicorn_app", \
     "--worker-class", "aiohttp.worker.GunicornWebWorker", \
     "-b", "0.0.0.0:8081"]
