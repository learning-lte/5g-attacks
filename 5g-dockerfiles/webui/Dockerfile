FROM ghcr.io/niloysh/free5gc-base:v3.2.0 AS builder
FROM ubuntu:20.04
ENV F5GC_MODULE webui
LABEL maintainer="Niloy Saha <niloysaha.ns@gmail.com>"
LABEL description="Free5GC WebUI v3.2.0"
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get -y install vim net-tools curl \
    && apt-get clean

# Set working dir
WORKDIR /free5gc
RUN mkdir -p config/ log/ config/TLS/ public/

# Copy executable and default certs
COPY --from=builder /free5gc/${F5GC_MODULE} ./
COPY --from=builder /free5gc/public ./public

# Config files volume
VOLUME [ "/free5gc/config" ]

# Certificates (if not using default) volume
VOLUME [ "/free5gc/config/TLS" ]

# Exposed ports
EXPOSE 5000