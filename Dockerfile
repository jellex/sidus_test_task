FROM python:3.9

# Create a group and user to run our app
ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

RUN pip install -U pip

# Copy in your requirements file
COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir /code/
WORKDIR /code/
COPY . /code/
ENV PYTHONPATH=.

EXPOSE 8000

RUN chown -R ${APP_USER}:${APP_USER} tests/

# Change to a non-root user
USER ${APP_USER}:${APP_USER}

CMD ["python", "api/run.py"]
