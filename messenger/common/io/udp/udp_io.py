'''
UDP utils for I/O (send/receive) in Pigeon
'''
import logging

from messenger import config

from messenger.common.io.udp.aioudp import (
    open_local_endpoint,
    open_remote_endpoint
)
from messenger.model.qitem import (
    Qitem
)

# logger
_LOGGER = logging.getLogger(__name__)


async def send_udp_message(message):
    '''
    Send a UDP message
    '''
    _LOGGER.debug("Starting to send passthrough message")
    udp_remote = await open_remote_endpoint(config.outbound_host,
                                            config.outbound_port,
                                            allow_broadcast=True,
                                            reuse_port=True)
    udp_remote.send(message)
    udp_remote.abort()
    _LOGGER.debug("Finished sending passthrough message")


async def udp_listener(host, port, queue):
    '''
    Await and enqueue recieved UDP messages
    '''
    _LOGGER.debug("Starting UDP listener")
    local = await open_local_endpoint(host,
                                      port,
                                      allow_broadcast=True,
                                      reuse_port=True)
    while True:
        data, address = await local.receive()
        queue.put(Qitem(message=data))
