# Based on https://github.com/free5gc/free5gc-compose
FROM golang:1.14.4-stretch AS builder
LABEL maintainer="Niloy Saha <niloysaha.ns@gmail.com>"

# Install dependencies
RUN apt-get update \
    && apt-get -y install gcc cmake autoconf libtool pkg-config libmnl-dev libyaml-dev apt-transport-https ca-certificates

# Clean apt cache
RUN apt-get clean

# Get Free5GC
RUN cd $GOPATH/src \
    && git clone --recursive -b v3.2.0 -j `nproc` https://github.com/free5gc/free5gc.git

WORKDIR $GOPATH/src/free5gc

# update .submodules to point to custom SMF source
RUN sed -i 's#https://github.com/free5gc/smf.git#https://github.com/niloysh/smf.git#g' .gitmodules
RUN git submodule sync --recursive

# checkout and build SMF v3.0.5.1 which logs slice information
RUN cd NFs/smf && git fetch && git checkout v3.2.0-sliceinfo
RUN make smf

FROM ubuntu:20.04
LABEL maintainer="Niloy Saha <niloysaha.ns@gmail.com>"
LABEL description="Free5GC SMF v3.2.0"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get -y install vim net-tools curl \
    && apt-get clean

WORKDIR /free5gc
RUN mkdir -p config/ log/ config/TLS/

# Copy executables
COPY --from=builder /go/src/free5gc/bin/* ./
COPY --from=builder /go/src/free5gc/config/TLS/*.pem ./config/TLS/
COPY --from=builder /go/src/free5gc/config/TLS/*.key ./config/TLS/

# Config files volume
VOLUME [ "/free5gc/config" ]

# Exposed ports
EXPOSE 8000
