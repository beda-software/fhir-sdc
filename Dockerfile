FROM python:3.9
RUN pip install pipenv
RUN mkdir /app
WORKDIR /app
ENV PYTHONPATH /app
ADD Pipfile /app
ADD Pipfile.lock /app
RUN pipenv install
ADD . /app
CMD ["pipenv", "run", "gunicorn", "main:create_app", "--worker-class", "aiohttp.worker.GunicornWebWorker", "-b", "0.0.0.0:8081"]
EXPOSE 8081
