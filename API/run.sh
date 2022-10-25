#!/bin/sh

docker run -it --rm --name rana-api -v "$(PWD)":/app/API -p 8800:8800 --network rana-net rana_api
