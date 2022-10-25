#!/bin/sh

VOLUME_NAME='rana_mongo'
NETWORK='rana-net'

if [ $(docker volume ls | grep $VOLUME_NAME | wc -l ) -eq 0 ];
then
  echo "Create New Volume for MongoDB"
  docker volume create --name $VOLUME_NAME
fi

# works on port 27017
docker run -d --rm --name mongodb --network $NETWORK -v $VOLUME_NAME:/data/db mongo

docker run -d --rm --name mongoexpress --publish 8081:8081 --network $NETWORK -e ME_CONFIG_MONGODB_SERVER=mongodb mongo-express
