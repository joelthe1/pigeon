'''
Entry point for the receiver
'''
import asyncio

import messenger.common.utils as utils
from messenger.inbound.arbiter import (
    arbitrate
)

async def main():
    '''
    Main function for arbitration
    '''
    utils.configure_logging()
    await arbitrate()

if __name__ == '__main__':
    asyncio.run(main())
