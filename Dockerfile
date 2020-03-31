FROM cgerull/minimal-flask-server:1.0.1
# Use alpine based flask-gunicorn image

USER web
WORKDIR /home/web

COPY --chown=1000 app /home/web/app
COPY --chown=1000 config.py /home/web/
COPY --chown=1000 LICENSE /home/web/
COPY --chown=1000 requirements.txt /home/web/
COPY --chown=1000 run_gunicorn.sh /home/web/
COPY --chown=1000 wsgi.py /home/web/

ENV PATH=$PATH:/home/web/.local/bin \
    PORT=8080 \
    ERROR_LOG=- \
    ACCESS_LOG=- \
    LOGFORMAT="%(h)s %(l)s %(t)s %({Server-IP}o)s %(l)s %(r)s %(s)s %(b)s %(a)s" \
    LOGLVL=INFO \
    SECRET_KEY=DockerFileSecret

RUN pip install -r requirements.txt

EXPOSE ${PORT}

#USER root
#
#ARG TOKEN
#RUN wget -O /microscanner https://get.aquasec.com/microscanner && \
#    chmod +x /microscanner && \
#    /microscanner $TOKEN && \
#    rm -rf /microscanner
#
#USER web
#WORKDIR /home/web

CMD sh run_gunicorn.sh
