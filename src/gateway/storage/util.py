import pika, json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload(f, fs, channel, access):

    try:
        fid = fs.put(f)
    except Exception as err:
        logger.info(f"{err}")
        return "[storage.util.1] Internal server error.", 500
    
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"]
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )

    except Exception as err:
        logger.info(f"{err}")
        fs.delete(fid)
        return "[storage.util.2] Internal server error.", 500