# api-sandbox

Collection of containers for API and deployment testing.

## Design

- one webserver servers HTML and REST requests. Connection to several other services.
  - gunicorn
  - flask
  - expose metrics for monitoring
  - for testing / persitency purpose connection to MongoDB / CosmosDB
  - state via redis
  - contexts for
    - testing
    - logging / diagnostic
    - API
 

---
![Docker Release Image](https://github.com/cgerull/api-sandbox-server/workflows/Docker%20Release%20Image/badge.svg?branch=master)
