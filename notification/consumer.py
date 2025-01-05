import pika
import sys
import os
from pymongo import MongoClient
import gridfs
from convert import to_mp3
from concurrent.futures import ThreadPoolExecutor
import logging
from send import email

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

executor = ThreadPoolExecutor(max_workers=5)

def main():
    try:
        with MongoClient("host.minikube.internal", 27017) as client:
            db_videos = client.videos
            db_mp3s = client.mp3s

            # gridfs
            fs_videos = gridfs.GridFS(db_videos)
            fs_mp3s = gridfs.GridFS(db_mp3s)

            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host="rabbitmq", heartbeat=120
                )
            )
            channel = connection.channel()

            video_queue = os.environ.get("MP3_QUEUE")
            if not video_queue:
                raise ValueError("Environment variable VIDEO_QUEUE is not set.")
            
            channel.queue_declare(queue=video_queue, durable=True)

            def callback(ch, method, properties, body):
                def process_message():
                    try:
                        logger.info(f"Received message: {body}")
                        err = email.notification(body)
                        if err:
                            ch.basic_nack(delivery_tag=method.delivery_tag)
                        else:
                            ch.basic_ack(delivery_tag=method.delivery_tag)
                    except Exception as e:
                        logger.error(f"Error processing message: {e}", exc_info=True)
                        ch.basic_nack(delivery_tag=method.delivery_tag)

                executor.submit(process_message)

            channel.basic_consume(queue=video_queue, on_message_callback=callback)

            print("Waiting for messages. To exit press CTRL+C")
            channel.start_consuming()

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)