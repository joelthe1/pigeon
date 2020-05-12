'''
Functionality that decided what to do with incoming
UDP Datagrams.
'''
import logging

import kafka
from messenger.common.aioudp import (
    open_local_endpoint,
    open_remote_endpoint
)

from messenger.common.kakfa_utils import (
    send_kafka_message
)

# logger
_LOGGER = logging.getLogger(__name__)

async def arbitrate():
    '''
    Arbitration logic for handling input UDP Datagrams
    '''
    local = await open_local_endpoint('127.0.0.1', '8989')
    
    while True:
        try:
            data, address = await local.receive()
            print(f'data is = {data}')

            _LOGGER.debug("Creating a kafkaProducer")
            # Instantiate a kafka producer
            kafka_producer = kafka.KafkaProducer(
                bootstrap_servers='127.0.0.1:19092'
            )
            _LOGGER.debug("Created a kafkaProducer")

            send_kafka_message(data, 'pigeon.test.outbound', kafka_producer)
        finally:
            try:
                kafka_producer.close()
            except kafka.errors.KafkaError:
                _LOGGER.exception("Error while trying to close kafka producer")
            finally:
                _LOGGER.info("Finished worker run")
