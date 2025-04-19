# docker/airflow/Dockerfile
FROM apache/airflow:2.6.3

# Switch to root to install OS‐level deps for psycopg2
USER root
RUN apt-get update \
 && apt-get install --no-install-recommends -y \
      build-essential \
      libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Switch back to the airflow user for pip installs
USER airflow
RUN pip install --no-cache-dir \
      kafka-python \
      psycopg2-binary

# Copy your DAGs
COPY dags/ /opt/airflow/dags/
