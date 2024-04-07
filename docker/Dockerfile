ARG IMAGE_PYTHON=${IMAGE_PYTHON:-python:3.10-slim-bullseye}
FROM ${IMAGE_PYTHON}

RUN apt-get update &&\
    apt-get -y install wget &&\
    apt-get install -y rsyslog &&\
    apt-get install -y libgdal-dev &&\
    apt-get install -y g++


# Define working directory
ARG PROJECT_DIR=/project
ENV PROJECT_DIR=${PROJECT_DIR}
WORKDIR ${PROJECT_DIR}
COPY src ${PROJECT_DIR}/src/
COPY docker/rsyslog.conf /etc/rsyslog.conf

# Install requirements package for python with poetry
ARG POETRY_VERSION=1.8.1
ENV POETRY_VERSION=${POETRY_VERSION}
RUN pip install --user "poetry==$POETRY_VERSION"
ENV PATH="${PATH}:/root/.local/bin"

# Backend
ENV PYTHONPATH=${PROJECT_DIR}/backend/
COPY backend/pyproject.toml backend/poetry.lock backend/alembic.ini ${PROJECT_DIR}/backend/
COPY docker/standalone docker/backend/backend docker/backend/scheduler /usr/local/bin/

ENV PATH=/venv/bin:$PATH \
    VIRTUAL_ENV=/venv
RUN python -m venv /venv &&\
    cd ${PROJECT_DIR}/backend/ &&\
	echo "source /venv/bin/activate" > /root/.bashrc &&\
    poetry install

# Launch cron services
RUN DEBIAN_FRONTEND=noninteractive apt-get -y --no-install-recommends install -y cron \
    # Remove package lists for smaller image sizes
    && rm -rf /var/lib/apt/lists/* \
    && which cron \
    && rm -rf /etc/cron.*/*

# Create cron task inside container
# Due to the fact that cron process doesn't access to declared ENV vars and doesn't load user profiles
# The entrypoint.sh script stores ENV vars at runtime in the ~/.env file as key=value pairs
# Then the cron line include some command to load these ENV vars from file before launching app.py
# This mecanism allows to give access to the same ENV vars for app.py launch in terminal and launch via cron
RUN echo "*/15 * * * * root export \$(cat /root/.env | grep -v -E '^#' | xargs);/venv/bin/python3 /project/backend/tasks/load_spire_data_from_api.py 2>/proc/1/fd/2 1>/proc/1/fd/1" > /etc/cron.d/trawlwatcher &&\
	chmod a+x /etc/cron.d/trawlwatcher

COPY docker/entrypoint.sh /entrypoint.sh
RUN ["chmod", "+x", "/entrypoint.sh"]

# ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
# https://manpages.ubuntu.com/manpages/trusty/man8/cron.8.html
# -f | Stay in foreground mode, don't daemonize.
# -L loglevel | Tell  cron  what to log about jobs (errors are logged regardless of this value) as the sum of the following values:
CMD ["cron","-f", "-L", "2"]
