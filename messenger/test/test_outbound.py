'''
Test code for sending messages to Pigeon
'''
import logging
import asyncio
import kafka

from messenger.common.io.udp.aioudp import (
    open_local_endpoint,
    open_remote_endpoint
)

from messenger.common.io.kafka.kafka_io import (
    send_kafka_message
)

import pigeon_pb2

# logger for the testing module
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                    filename='pigeon_test.log',
                    level=logging.DEBUG)



async def send_test_udp_message(host, port, data):
    test_data = pigeon_pb2.Header()
    test_data.via = pigeon_pb2.ViaType.UDP
    test_data.endpoint = f'{host}:{port}'
    test_data.data = data

    remote = await open_remote_endpoint('127.0.0.1', '8989')
    remote.send(test_data.SerializeToString())
    remote.abort()


async def send_test_kafka_message(topic, data):
    test_data = pigeon_pb2.Header()
    test_data.via = pigeon_pb2.ViaType.KAFKA
    test_data.endpoint = topic
    test_data.data = data

    remote = await open_remote_endpoint('127.0.0.1', '8989')
    remote.send(test_data.SerializeToString())
    remote.abort()
    

def receive_test_kafka_message(topic, data):
    try:
        # test_data = pigeon_pb2.Header()
        # test_data.via = pigeon_pb2.ViaType.KAFKA
        # test_data.endpoint = topic
        # test_data.data = data

        # Instantiate a kafka producer
        kafka_producer = kafka.KafkaProducer(
            bootstrap_servers='127.0.0.1:19092'
        )
        logging.debug("Created a kafkaProducer")
        send_kafka_message(data.encode('utf-8'), topic, kafka_producer) 
    finally:
        try:
            kafka_producer.close()
        except kafka.errors.KafkaError:
            logging.exception("Error while trying to close Kafka producer")
        finally:
            logging.info("Finished sending via Kafka")


async def main():
    logging.info('starting test')
    # await send_test_udp_message(host='127.0.0.1',
    #                        port='9090',
    #                        data='My test UDP sent data')

    # await send_test_kafka_message(topic='pigeon.test.outbound',
    #                          data='My test Kakfa sent data')

    receive_test_kafka_message('pigeon.test.inbound', 'Pigeon received Kafka data')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        raise e
