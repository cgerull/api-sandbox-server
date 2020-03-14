# api-sandbox

Collection of containers for API and deployment testing.

## Design

- one webserver servers HTML and REST requests. Connection to several other services.
  - gunicorn
  - flask

  - for testing / persitency purpose connection to MongoDB / CosmosDB
  - state via redis
  - contexts for
    - testing
    - logging / diagnostic
    - API

## Envrionment

FLASK_ENV=development
REDIS_URL=redis://localhost
DATABASE_URL=postgres://db_test:mySecret123!@localhost:5432/db_test

## ToDo

- expose metrics for monitoring
- connect to database
- connect to messagebus
- testing
- logging / diagnostic

---
Development: ![Docker Release Image](https://github.com/cgerull/api-sandbox-server/workflows/Docker%20Release%20Image/badge.svg?branch=development)
