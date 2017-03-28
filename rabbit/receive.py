#!/usr/bin/env python
import pika
mq="ec2-52-11-222-159.us-west-2.compute.amazonaws.com"
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=mq))
channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()