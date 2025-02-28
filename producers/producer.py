import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Create a single queue (shared among all consumers)
channel.queue_declare(queue='task_queue', durable=True)

# Send messages
for i in range(1):
    message = f"C:/Workspace/tools-testing/rabbitmq/ATR2024_01.xlsx"
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make message persistent
        ),
    )
    print(f"Sent: {message}")

connection.close()
