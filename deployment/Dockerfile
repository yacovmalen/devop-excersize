from docker/compose:1.22.0

RUN apk add --update \
    python3 \
    && rm -rf /var/cache/apk/*

COPY . /src/code

WORKDIR /src/code/deployment

ENTRYPOINT ["python3", "deploy.py"]

