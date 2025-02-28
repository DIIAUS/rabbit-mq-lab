import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Create a single queue (shared among all consumers)
channel.queue_declare(queue='task_queue', durable=True)

# Send messages
for i in range(10):
    message = f"Task {i}"
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
