FROM google/cloud-sdk:278.0.0 AS gcloud
FROM python:3.7 AS base

COPY . /usr/src/custom_container_tfx
WORKDIR /usr/src/custom_container_tfx

ENTRYPOINT ["bash"]