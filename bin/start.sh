#!/bin/bash
set -ex

CNAME=$1
URL=$2
BLOCK=$3
DATA=$4

MODEL="checkpoint/run1"
TZ=`cat /etc/timezone`
LOG=".log/"

MOUNT_OPS=""
if [ -d $MODEL ]; then
    MOUNT_OPS="$MOUNT_OPS -v $PWD/$MODEL:/app/$MODEL"
fi
if [ ! -z $BLOCK ] && [ -f $BLOCK ]; then
    MOUNT_OPS="$MOUNT_OPS -v $PWD/$BLOCK:/app/$BLOCK"
fi
if [ ! -z $DATA ] && [ -f $DATA ]; then
    MOUNT_OPS="$MOUNT_OPS -v $PWD/$DATA:/app/$DATA"
fi

MOUNT_OPS="$MOUT_OPS -v $PWD/$LOG:/app/$LOG"

source $PWD/.creds
docker login $URL -u $GL_USER -p $GL_TOKEN

docker pull $URL:latest
docker run --rm -d --name $CNAME --env-file docker.env -e TZ=$TZ $MOUNT_OPS $URL
