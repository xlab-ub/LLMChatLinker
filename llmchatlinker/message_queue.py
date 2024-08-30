import pika
import uuid

RABBITMQ_HOST = 'localhost'
INSTRUCTION_QUEUE = 'instruction_queue'

class MessageQueueClient:
    def __init__(self, queue_name=INSTRUCTION_QUEUE):
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)
        self.response = None
        self.corr_id = None
        self.callback_queue = self.channel.queue_declare(queue='', exclusive=True).method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, instruction):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=instruction
        )
        while self.response is None:
            self.connection.process_data_events()
        return self.response

def publish_message(message):
    client = MessageQueueClient()
    return client.call(message)

def publish_response(channel, message, correlation_id, reply_to):
    channel.basic_publish(
        exchange='',
        routing_key=reply_to,
        properties=pika.BasicProperties(correlation_id=correlation_id),
        body=message
    )

def init_message_queue(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    return channel, queue_name

def consume_messages(channel, queue_name, callback):
    def callback_wrapper(ch, method, properties, body):
        callback(body, properties)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=queue_name, on_message_callback=callback_wrapper)
    print(f' [*] Waiting for messages in {queue_name}. To exit press CTRL+C')
    channel.start_consuming()