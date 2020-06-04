'''
Entry point for the receiver
'''
import asyncio

import messenger.common.utils as utils
from messenger.test.stress.short_circuit_udp.inbound.arbiter import (
    arbitrate_input
)

async def main():
    '''
    Main function for arbitration
    '''
    utils.configure_logging()
    await arbitrate_input()

if __name__ == '__main__':
    asyncio.run(main())
