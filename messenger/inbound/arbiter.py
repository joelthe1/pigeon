'''
Functionality that decides what to do with incoming
traffic to Pigeon
'''
import logging
import os
import asyncio

from messenger.common import utils

import messenger.exceptions as pigeon_exceptions
from messenger import config

from messenger.common.io.udp.udp_io import (
    udp_listener
)
from messenger.common.io.kafka.kafka_io import (
    kafka_listener
)

def arbitrate_input_udp(queue):
    '''
    Arbitration logic for handling input UDP Datagrams
    '''
    # configure logger for this process
    utils.configure_logging(filename='logs/input_udp.log',
                            log_level_param=config.log_level)
    _LOGGER = logging.getLogger(__name__)

    for _ in range(int(config.udp_listener_count)):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.get_event_loop().create_task(udp_listener(config.inbound_host,
                                                          config.inbound_port,
                                                          queue))
        asyncio.get_event_loop().run_forever()


def arbitrate_input_kafka(queue):
    '''
    Arbitration logic for handling input Kafka messages
    '''
    # configure logger for this process
    utils.configure_logging(filename='logs/input_kafka.log',
                            log_level_param=config.log_level)
    _LOGGER = logging.getLogger(__name__)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().create_task(kafka_listener(config.kafka_host,
                                                        config.kafka_port,
                                                        config.inbound_kafka_topic,
                                                        queue))
    asyncio.get_event_loop().run_forever()
