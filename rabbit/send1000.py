#!/usr/bin/env python
import pika

mq="ec2-52-11-222-159.us-west-2.compute.amazonaws.com"
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=mq))
channel = connection.channel()

channel.queue_declare(queue='hello')
for i in range(1000):
	channel.basic_publish(exchange='',
                      routing_key='hello',
                      #body='Hello World! ' + str(i))
					  body=str(i) + ' msg ' * (i % 29))
	print(" [x] Sent " + str(i))
connection.close()