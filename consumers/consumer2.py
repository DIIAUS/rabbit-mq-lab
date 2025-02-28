import pika
import time

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the same queue (important for durability)
    channel.queue_declare(queue='task_queue', durable=True)

    # Ensure Fair Dispatch (each consumer processes one message at a time)
    channel.basic_qos(prefetch_count=1)

    def callback(ch, method, properties, body):
        print(f"Received: {body.decode()}")
        time.sleep(2)  # Simulate processing time
        print("Task done!")
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge message

    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    print("Waiting for messages... Press Ctrl+C to exit.")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected! Closing connection...")
        channel.stop_consuming()  # Stop consuming before closing
        connection.close()
        print("Connection closed. Exiting gracefully.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")