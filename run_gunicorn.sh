#!/bin/sh
#
gunicorn wsgi:app \
--bind 0.0.0.0:${PORT} \
--workers 2 \
--access-logfile ${ACCESSLOG} \
--access-logformat "${LOGFORMAT}" \
--error-logfile ${ERRLOG} \
--log-level ${LOGLVL}
