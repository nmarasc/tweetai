set -ex

URL=$1
CNAME=$2

MODEL="checkpoint/run1"

source .creds
docker login $URL -u $GL_USER -p $GL_TOKEN

docker pull $URL:latest
if [-d $MODEL]; then
    docker run -d --rm --name $CNAME --env-file docker.env -v $PWD/$MODEL:/app/$MODEL $URL
else
    docker run -d --rm --name $CNAME --env-file docker.env $URL
fi
