FROM python:3.9

RUN pip install cbapi requests

ENV AIR_WEBHOOK_URL ''
ENV CB_DEFENSE_SERVER ''

WORKDIR /usr/src/app/
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/usr/src/app" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid 33333 \
    integration

RUN chown -R integration:integration /usr/src/app
USER integration:integration

COPY main.py .
COPY credentials.defense /etc/carbonblack/credentials.psc

CMD ["python", "-u" ,"main.py"]
