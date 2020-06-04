'''
Entry point for the Pigeon messenger
'''
import logging
import asyncio
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager, log_to_stderr

from messenger.common import utils
from messenger.inbound.arbiter import (
    arbitrate_input_udp,
    arbitrate_input_kafka
)       
from messenger.outbound.arbiter import (
    arbitrate_output
)
from . import config

async def main(executer):
    '''
    Main function for arbitration
    '''
    queue = Manager().Queue()
    
    # TODO: Improve error handling
    # TODO: Handle keyboard interrupt signal
    
    # asyncio.get_event_loop().run_in_executor(executor, utils.reader, queue)
    asyncio.get_event_loop().run_in_executor(executor, arbitrate_input_udp, queue)
    asyncio.get_event_loop().run_in_executor(executor, arbitrate_input_kafka, queue)
    asyncio.get_event_loop().run_in_executor(executor, arbitrate_output, queue)

if __name__ == '__main__':
    # configure logger for this process
    utils.configure_logging(filename='logs/main.log',
                            log_level_param=config.log_level)
    _LOGGER = logging.getLogger(__name__)

    # log debug messages of multiprocessing
    # log_to_stderr()

    _LOGGER.info(f'Setup done with {config}')
    _LOGGER.info('Pigeon is starting to fly!')

    executor = ProcessPoolExecutor()
    asyncio.get_event_loop().create_task(main(executor))
    asyncio.get_event_loop().run_forever()
