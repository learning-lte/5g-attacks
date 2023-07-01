# About
This repository contains Dockerfiles for the [Free5gc](https://github.com/free5gc/free5gc) and [UERANSIM](https://github.com/aligungr/UERANSIM) projects.
The container images can be used to run a 5G network using Kubernetes. Details on how this can be done, including Kubernetes manifest files can be found at [5gc-manifests](https://github.com/niloysh/5gc-manifests).

# Usage
These images are based on the Ubuntu docker image. Thus, you can run them as:
```
$ docker run -it <image> /bin/bash
```
Check out [5gc-manifests](https://github.com/niloysh/5gc-manifests) to see how you can run a 5G network based on these images using Kubernetes.




# Notes on the container images
You should probably use the `aio` image, which is built on Ubuntu:20.04. 
- `aio`: All in one image, which conatains executables for all of the free5GC functions.
- `base`: Used as base image for multi-stage build. The `aio` image depends on this.

The `aio` image is around 220 Mb in size. The Ubuntu image is used for ease-of-use and experimentation; the focus is not on reducing the size of the image. Using other images such as [minideb](https://github.com/bitnami/minideb) or [alpine](https://hub.docker.com/_/alpine) can be used for reducing the size of the container images. Please note that the UPF does not support alpine.

- `upf-exporter`: Prometheus exporter which relies on [libgtp5gnl](https://github.com/free5gc/libgtp5gnl). It collects Rx and Tx PDR statistics for each PDR and exposes these PDR statistics in [Prometheus format](https://prometheus.io/docs/concepts/metric_types/).

# Credit
These are heavily inspired by the [free5gc-compose](https://github.com/free5gc/free5gc-compose) project.
