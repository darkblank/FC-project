#!/usr/bin/env bash
docker build -t base -f Dockerfile.base .
docker tag base bookpark/zinzi-base
docker push bookpark/zinzi-base
