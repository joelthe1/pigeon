'''
Functionality that decides what to do with outgoing
traffic from Pigeon
'''
import logging
import asyncio

from messenger import exceptions as pigeon_exceptions
from messenger.common import utils
from messenger import config

from messenger.common.io.kafka.kafka_io import (
    send_kafka_message
)
from messenger.common.io.udp.udp_io import (
    send_udp_message
)

# configure logger for this process
utils.configure_logging(filename='logs/arbitrate_output.log',
                        log_level_param=config.log_level)
_LOGGER = logging.getLogger(__name__)


async def handle_message(queue):
    '''
    Generic message handler that dispatches
    messages to appropriate channels.
    '''
    # TODO: Set flavor type from env e.g. Kakfa, gRPC, etc.
    # Kafka flavor
    while True:
        try:
            qitem = queue.get()

            # Handle passthrough to UDP
            if qitem.passthrough:
                await send_udp_message(qitem.message)
            else:
                await send_kafka_message(qitem.message)
        except pigeon_exceptions.OutboundException as e:
            _LOGGER.exception('Outbound error. Will put message back on queue')
            # put back message in queue for re-attempting
            # TODO: Do this only n times.
            queue.put(qitem)


def arbitrate_output(queue):
    '''
    Arbitration logic for handling output messages
    '''

    for _ in range(int(config.output_handler_count)):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.get_event_loop().create_task(handle_message(queue))
        asyncio.get_event_loop().run_forever()
