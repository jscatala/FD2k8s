#!/bin/sh

docker run -d --rm --hostname my-rabbit --name some-rabbit -p 8080:15672 --network rana-net rabbitmq:3-management
