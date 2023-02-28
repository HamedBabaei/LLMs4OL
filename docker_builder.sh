#!/bin/bash
docker build -f Dockerfile . -t llms4ol

docker save -o assets/llms4ol.tar llms4ol

singularity build assets/llms4ol.sif docker-archive:assets/llms4ol.tar


