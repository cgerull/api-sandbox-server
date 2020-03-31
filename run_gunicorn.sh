#!/bin/sh
#
# export PORT=8000
# export ACCESS_LOG='./access.log'
# export ERR_LOG='./error.log'
# export LOGFORMAT='%(h)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\"'
# export LOGLVL=INFO

gunicorn wsgi:app \
--bind 0.0.0.0:${PORT} \
--workers 2 \
--access-logfile ${ACCESS_LOG} \
--access-logformat "${LOGFORMAT}" \
--error-logfile ${ERROR_LOG} \
--log-level ${LOGLVL}
