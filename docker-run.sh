#!/bin/bash
docker build -t base -f Dockerfile.base .
docker build -t zinzi .
docker run --rm -it -p 8012:80 zinzi