set -ex

URL=$1

docker build --build-arg GIT_HASH=$(git rev-parse HEAD) -t $URL:latest .