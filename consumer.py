# _*_ coding:utf-8 _*_

import pika
import json
import requests

with open('config.json', 'r') as f:
  config = json.load(f)

def send_slackmessage(message):
  webhook_url = config['WEBHOOK_URL']
  payload = {'text': message}
  requests.post(
    webhook_url, data = json.dumps(payload),
    headers = {'Content-Type': 'application/json'}
    )

credentials = pika.PlainCredentials(
  config['RABBITMQ_CREDENTIALS']['USERNAME'], 
  config['RABBITMQ_CREDENTIALS']['PASSWORD'])

connection = pika.BlockingConnection(pika.ConnectionParameters(
  host=config['RABBITMQ_CONNECTION']['HOST'],
  port=config['RABBITMQ_CONNECTION']['PORT'],
  virtual_host=config['RABBITMQ_CONNECTION']['VHOST'],
  credentials=credentials))

channel = connection.channel()

channel.queue_declare(queue='review.create')

def review_creqte_callback(ch, method, properties, body):
  create_json = json.loads(body)
  msg = create_json['companyName'] + '의 취업 후기가 올라왔습니다.'
  send_slackmessage(msg)

def review_update_callback(ch, method, properties, body):
  update_json = json.loads(body)
  msg = update_json['companyName'] + '의 취업 후기가 업데이트되었습니다.'
  send_slackmessage(msg)

channel.basic_consume(
  queue='review.create', on_message_callback=review_creqte_callback, auto_ack=True)

channel.basic_consume(
  queue='review.update', on_message_callback=review_update_callback, auto_ack=True)

print('Start consuming.')
channel.start_consuming()
