'''
Functionality that decided what to do with incoming
UDP Datagrams.
'''
import logging
import os
import asyncio

import messenger.exceptions as messenger_exceptions
from messenger.test.stress.short_circuit_udp.inbound import config

from messenger.common.io.udp.udp_io import (
    udp_producer
)

from messenger.common.io.kafka.kafka_io import (
    kafka_producer
)

from messenger.test.stress.short_circuit_udp.outbound.arbiter import (
    arbitrate_output
)

# logger
_LOGGER = logging.getLogger(__name__)

async def arbitrate_input():
    '''
    Arbitration logic for handling input UDP Datagrams
    '''
    # TODO: Set these values from the environment
    _LOGGER.info(f'App setup with {config}')
    _LOGGER.info('Pigeon is starting to fly!')
    queue = asyncio.Queue()

    # fire up the both producers and consumers
    _LOGGER.info(f'{config}')
    producers = [asyncio.create_task(udp_producer(config.inbound_host, config.inbound_port, queue))]

    consumers = [asyncio.create_task(arbitrate_output(queue))]

    await asyncio.gather(*producers)
    # await queue.join()
