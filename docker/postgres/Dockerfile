FROM postgres:15

ENV POSTGRES_USER=centrauser
ENV POSTGRES_PASSWORD=centrapass
ENV POSTGRES_DB=centrahealth

# Initialize central schema on first run
COPY db/postgres/CentraHealth_CentralDB.sql /docker-entrypoint-initdb.d/
