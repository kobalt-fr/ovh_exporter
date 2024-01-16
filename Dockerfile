FROM python:3.12 as builder
WORKDIR /ovh_exporter
COPY dist/ /dist
RUN pip --no-cache-dir install virtualenv && \
    virtualenv /ovh_exporter && \
    /ovh_exporter/bin/pip install --no-cache-dir /dist/*.whl

FROM python:3.12
RUN apt-get update && \
    apt-get dist-upgrade -y && \
    rm -rf /var/cache/apt/*
WORKDIR /app
COPY --from=builder /ovh_exporter /ovh_exporter
CMD ["/ovh_exporter/bin/ovh_exporter", "server"]
