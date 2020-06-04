'''
Stress test Pigeon I/O
'''
import sys
import logging
# logger for the testing module
# logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
#                     filename='pigeon_test.log',
#                     level=logging.DEBUG)

from aiokafka import AIOKafkaConsumer
import kafka
import asyncio

from messenger.common.io.udp.aioudp import (
    open_local_endpoint,
    open_remote_endpoint
)

import pigeon_pb2

formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

def setup_logger(name, log_file, formatter=formatter, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# first file logger
logger = setup_logger('first_logger', 'pigeon_test.log', level=logging.DEBUG)

# second file logger
output_logger = setup_logger('output_logger', 'output.log', formatter=logging.Formatter('%(message)s'))


async def test_bulk_send_kafka(host, port):
    remote = await open_remote_endpoint('127.0.0.1', '8989')
    for iteration in range(10000):
        test_data = pigeon_pb2.Header()
        test_data.via = pigeon_pb2.ViaType.KAFKA
        test_data.endpoint = 'pigeon.test.outbound'
        test_data.data = str(iteration+1)
        remote.send(test_data.SerializeToString())
    remote.abort()


async def test_bulk_read_kafka(host, port):
    try:
        consumer = AIOKafkaConsumer(
            "pigeon.test.outbound",
            bootstrap_servers=f'{host}:{port}')
        # Get cluster layout and topic/partition allocation
        await consumer.start()
        logger.debug('Starting for loop for reading Kafka Topic')
        async for message in consumer:
            logger.debug(f'Found message in for loop: {message.value}')
            output_logger.info(message.value.decode('utf-8'))
    except Exception as e:
        logger.exception(f'Error while producing a Kakfa message: {e}')
    finally:
        logger.debug('Closing reading Kafka Topic')
        await consumer.stop()
        logger.debug('Closed reading Kafka Topic')    


async def run_test_bulk_send_kafka():
    await test_bulk_send_kafka('127.0.0.1', '19092')

async def run_test_bulk_read_kakfa():
    await test_bulk_read_kafka('127.0.0.1', '19092')

if __name__ == '__main__':
    logger.info('starting test')
    try:
        if sys.argv[1].lower() == 'send':
            asyncio.run(run_test_bulk_send_kafka())
        else:
            asyncio.run(run_test_bulk_read_kakfa())
    except Exception as e:
        logger.exception(e)
        raise e
