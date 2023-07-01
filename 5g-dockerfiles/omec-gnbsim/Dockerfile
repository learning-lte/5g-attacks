FROM golang:1.18.0-stretch AS builder

LABEL maintainer="Niloy Saha <niloysaha.ns@gmail.com>"
LABEL description="OMEC gNBsim"

RUN apt-get update \
    && apt-get -y install vim ethtool \
    && cd $GOPATH/src \
    && git clone -j `nproc` https://github.com/omec-project/gnbsim.git \
    && cd $GOPATH/src/gnbsim \
    && go mod tidy && go mod vendor \
    && go build -mod=vendor

FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

# Install debugging tools
RUN apt-get update \
    && apt-get install vim iproute2 iputils-ping iperf3 net-tools -y \
    && apt-get clean

RUN mkdir -p /gnbsim/bin /gnbsim/config/

# Copy executable
COPY --from=builder /go/src/gnbsim/gnbsim /gnbsim/bin/
COPY --from=builder /go/src/gnbsim/config /gnbsim/config/

WORKDIR /gnbsim/bin
