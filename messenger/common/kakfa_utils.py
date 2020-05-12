'''
Kafka utils for send/receive
'''
# Core Python
import logging
import pprint

# Third party
import kafka

# logger
_LOGGER = logging.getLogger(__name__)

def stringify_kafka_msg(msg, succinct: bool = True):
    """Stringify kafka msg obj for succinct logging"""
    if succinct:
        text_data = dict(
            key=getattr(msg, 'key', None),
            offset=getattr(msg, 'offset', None),
            topic=getattr(msg, 'topic', None),
        )
        msg_value = getattr(msg, 'value', None)
        if msg_value is not None:
            text_data['value_len'] = len(msg_value)
        text = str(text_data)
    else:
        text = str(msg)
    return text

def kafka_on_send_success(record_metadata):
    """Callback used by the Kafka producer for on-success events"""
    if _LOGGER.isEnabledFor(logging.DEBUG):
        _LOGGER.debug("Successfully sent message: %s", stringify_kafka_msg(record_metadata, succinct=True))
    else:
        _LOGGER.info("Successfully sent message: %s", stringify_kafka_msg(record_metadata, succinct=True))


def kafka_on_send_error(exc_info):
    """Callback used by the Kafka producer for on-error events"""
    _LOGGER.error("Failed to send message", exc_info=exc_info)

def send_kafka_message(kafka_message_value: bytes, kafka_topic: str, kafka_producer: kafka.KafkaProducer):
    """
    Send the kafka message synchronously
    """
    _LOGGER.debug("Sending kafka message to topic '%s'", str(kafka_topic))
    future_result = kafka_producer.send(kafka_topic, kafka_message_value).add_callback(
        kafka_on_send_success).add_errback(kafka_on_send_error)
    result = future_result.get()
    _LOGGER.debug("Result of Kafka producer send() was %s", pprint.pformat(result))
