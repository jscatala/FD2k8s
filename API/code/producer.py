import pika

#this should be a query in redis
OPTS = ['cat', 'dog']

def add_vote(opt):
    print("Received vote for {}".format(opt))
    conn = pika.BlockingConnection(pika.ConnectionParameters('some-rabbit'))
    channel = conn.channel()
    channel.queue_declare(queue='votes')
    try:
        channel.basic_publish(exchange='',
                      routing_key='votes',
                      body=opt)
        print(" [x] Sent '{}'".format(opt))
    except:
        print("there was some unhandled error at add_vote")

    conn.close()
