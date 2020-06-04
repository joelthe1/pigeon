'''
Functionality that decided what to do with outgoing
data
'''
import logging
import os

import grpc
import kafka

from messenger.inbound import config

from messenger.common.utils import (
    setup_adhoc_logger
)

from messenger.common.io.udp.aioudp import (
    open_remote_endpoint
)

from messenger.common.io.kafka.kafka_io import (
    send_kafka_message
)

# logger
_LOGGER = logging.getLogger(__name__)

# test output file logger
output_logger = setup_adhoc_logger('output_logger',
                                   'output.log',
                                   formatter=logging.Formatter('%(message)s'))

async def arbitrate_output(queue):
    '''
    Arbitration logic for handling output
    '''
    while True:
        # TODO: Add better error handling

        qitem = await queue.get()
        message = qitem.message
        
        # Handle passthrough to UDP
        if qitem.passthrough:
            _LOGGER.debug("Starting to send passthrough message")
            udp_remote = await open_remote_endpoint(config.outbound_host,
                                                    config.outbound_port,
                                                    allow_broadcast=True,
                                                    reuse_port=True)
            udp_remote.send(message)
            udp_remote.abort()
            _LOGGER.debug("Finished sending passthrough message")
            queue.task_done()

        # Short circuit code to log only
        # This is for testing if incoming UDP messages are received 
        else:
            try:
                output_logger.info(f'{message}')
                queue.task_done()
            except Exception as e:
                _LOGGER.exception(f"Error while logging message: {e}")

                # put back message in queue for re-attempting
                # TODO: Do this only n times.
                await queue.put(qitem)
                queue.task_done()

