#!/bin/bash
set -ex

URL=$1
CNAME=$2
BLOCK=$3

MODEL="checkpoint/run1"

MOUNT_OPS=""
if [ -d $MODEL ]; then
    MOUNT_OPS="$MOUNT_OPS -v $PWD/$MODEL:/app/$MODEL"
fi
if [ ! -z $BLOCK ] && [ -f $BLOCK ]; then
    MOUNT_OPS="$MOUNT_OPS -v $PWD/$BLOCK:/app/$BLOCK"
fi

source $PWD/.creds
docker login $URL -u $GL_USER -p $GL_TOKEN

docker pull $URL:latest
docker run -d --rm --name $CNAME --env-file docker.env $MOUNT_OPS $URL
