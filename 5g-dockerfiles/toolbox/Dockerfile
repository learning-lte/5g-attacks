FROM ubuntu:20.04
LABEL maintainer="Niloy Saha <niloysaha.ns@gmail.com>"
LABEL description="Toolbox v1.0.0"

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get install iproute2 iputils-ping iptables -y \
    && apt-get install vim iperf3 net-tools tcpdump python3-scapy nmap -y \
    && apt-get install -y software-properties-common \
    && apt-get clean

RUN add-apt-repository -y ppa:wireshark-dev/stable \
    && apt install -y tshark

WORKDIR /toolbox
