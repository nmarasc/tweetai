set -ex

URL=$1

VERSION=`python3 tweetai/__version__.py`

git pull

bin/build.sh $URL

git add --all
git commit -m "Release version $VERSION"
git tag -a "$VERSION" -m "version $VERSION"
git push
git push --tags

docker tag $URL:latest $URL:$VERSION

docker push $URL:latest
docker push $URL:$VERSION
