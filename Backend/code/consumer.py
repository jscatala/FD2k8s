#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
from pymongo import MongoClient, errors

import socket
from datetime import datetime as dt
from dotenv import dotenv_values
from pathlib import Path
from os import _exit as o_exit
from os import environ
from sys import exit as sexit
from sys import exc_info


env_path = Path('.') / '.env'
config = dotenv_values(dotenv_path=env_path)

def get_mongodb():
    try:
        client = MongoClient(
            config['MONGO_HOSTNAME'],
            int(config['MONGO_PORT'])
            )
        if config['MONGODB_NAME'] not in client.list_database_names():
            db = client[config['MONGODB_NAME']]
            initialize(db)

        return client[config['MONGODB_NAME']]

    except errors.ConnectionFailure as e:
        print("Could not connect to server: %s" % e)
    except errors.PyMongoError:
        #e = exc_info()[0]
        #print("%s" % e)
        print("some error")

def initialize(db):
    print("Database does not exists...")
    print("   [*] Initializing")

    collection = db['alternatives']

    def_opts = config['RANA_DEF_OPTS'].split(',')
    for opt in def_opts:
        data = {
            'option': str(opt),
            'created': dt.utcnow(),
            'votes': 0
            }
        option_id = collection.insert_one(data).inserted_id
        print("   [+] New default option: %s" % opt)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='some-rabbit'))
    channel = connection.channel()
    channel.queue_declare(queue='votes')

    def callback(ch, method, properties, body):
        # TODO: Catch exception if mongo db is not working
        opt = body.decode('utf-8')
        db = get_mongodb()
        collection_votes = db['votes']
        vote = {
            "value":  '%s' % opt,
            "date": dt.utcnow()}
        post_id = collection_votes.insert_one(vote).inserted_id

        #print(db['alternatives'].find_one(
        #    {'option': '%s' % opt}
        #    ))
        db['alternatives'].find_one_and_update(
            {'option': '%s' % opt},
            {'$inc':{'votes':1}}
            )

        ch.basic_ack(delivery_tag = method.delivery_tag)
        print(" [x] Received %s" % opt)

    channel.basic_consume(queue='votes', on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
    except socket.gaierror:
        print('Error while connecting...')
    finally:
        try:
            sexit(0)
        except SystemExit:
            o_exit(0)
