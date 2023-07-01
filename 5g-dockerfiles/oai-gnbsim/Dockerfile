FROM golang:1.18.0-stretch AS builder

LABEL maintainer="Niloy Saha <niloysaha.ns@gmail.com>"
LABEL description="OAI gNBsim"

RUN apt-get update \
    && apt-get -y install vim ethtool \
    && cd $GOPATH/src \
    && git clone -j `nproc` https://gitlab.eurecom.fr/kharade/gnbsim.git \
    && cd $GOPATH/src/gnbsim \
    && cd $GOPATH/src/gnbsim/gnbsim/cmd  && go build . \
    && cd $GOPATH/src/gnbsim/example && go build .


FROM ubuntu:20.04
ENV DEBIAN_FRONTEND noninteractive

# Install debugging tools
RUN apt-get update \
    && apt-get install vim iproute2 iputils-ping iperf3 net-tools -y \
    && apt-get clean

RUN mkdir -p /gnbsim/bin
WORKDIR /gnbsim/bin

COPY --from=builder /go/src/gnbsim/example/example .
COPY --from=builder /go/src/gnbsim/docker/example.json .
COPY --from=builder /go/src/gnbsim/docker/entrypoint.sh .

