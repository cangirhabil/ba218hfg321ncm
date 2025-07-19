#!/bin/bash

docker stop $(docker ps -a -q)
docker system prune --all --force
docker volume prune --all --force