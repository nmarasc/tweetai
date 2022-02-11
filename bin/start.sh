set -ex

URL=$1
CNAME=$2

source .creds
docker login $URL -u $GL_USER -p $GL_TOKEN

docker pull $URL:latest
docker run -d --name $CNAME --env-file docker.env --restart on-failure:5 $URL
