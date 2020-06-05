'''
Kafka utils for I/O (send/receive) in Pigeon
'''
# Core Python
import logging
import asyncio

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import kafka.errors

from messenger import config
from messenger import exceptions as pigeon_exceptions
from messenger.model.qitem import (
    Qitem
)

# logger
_LOGGER = logging.getLogger(__name__)


async def send_kafka_message(message):
    '''
    Send a Kafka message
    '''
    try:
        loop = asyncio.get_event_loop()
        _LOGGER.debug('Creating a kafkaProducer')
        # Instantiate a kafka producer
        kafka_producer = AIOKafkaProducer(
            loop=loop, bootstrap_servers=f'{config.kafka_host}:{config.kafka_port}',
            enable_idempotence=True)

        for attempt in range(1, config.max_retries+1):
            try:
                await kafka_producer.start()
                _LOGGER.info('Successfully connected to Kafka')

                for topic in config.outbound_kafka_topics.split():
                    await kafka_producer.send_and_wait(topic, message)
                    
                break
            except kafka.errors.KafkaConnectionError as e:
                _LOGGER.error('Error connecting to Kafka')
                if attempt == config.max_retries:
                    raise pigeon_exceptions.InboundException(f'Unable to connect to Kafka after {max_attempts} attempts.')
                
                _LOGGER.info(f'Will retry in {config.retry_delay**attempt} seconds...')
                await asyncio.sleep(config.retry_delay**attempt)

    except Exception as e:
        raise pigeon_exceptions.OutboundException(f'Error while trying to send Kafka message: {e}')
    finally:
        try:
            await kafka_producer.stop()
        except kafka.errors.KafkaError:
            _LOGGER.exception('Error while trying to close Kafka producer')
        except Exception as e:
            _LOGGER.exception(f'Error while trying to close kafka connection: {e}')
            raise pigeon_exceptions.OutboundException(f'Error while trying to close kafka connection: {e}')
        finally:
            _LOGGER.debug('Exiting code for sending via Kafka')


async def kafka_listener(host, port, topic, queue):
    '''Await and enqueue recieved Kafka message'''
    try:
        consumer = AIOKafkaConsumer(topic,
                                    bootstrap_servers=f'{host}:{port}')

        for attempt in range(1, config.max_retries+1):
            try:
                # Get cluster layout and topic/partition allocation
                await consumer.start()
                _LOGGER.info('Successfully connected to Kafka')

                _LOGGER.debug('Starting for loop for reading Kafka Topic')
                async for message in consumer:
                    _LOGGER.debug(f'Found message in for loop: {message.value}')
                    queue.put(Qitem(message=message.value,
                                    passthrough=True))
            
                break
            except kafka.errors.KafkaConnectionError as e:
                _LOGGER.error('Error connecting to Kafka')
                if attempt == config.max_retries:
                    raise pigeon_exceptions.InboundException(f'Unable to connect to Kafka after {max_attempts} attempts.')
                
                _LOGGER.info(f'Will retry in {config.retry_delay**attempt} seconds...')
                await asyncio.sleep(config.retry_delay**attempt)
        
    except Exception as e:
        raise pigeon_exceptions.InboundException(f'Error while listening/consuming Kakfa message: {e}')
    finally:
        try:
            _LOGGER.debug('Closing reading Kafka Topic')
            await consumer.stop()
            _LOGGER.debug('Closed reading Kafka Topic')
        except kafka.errors.KafkaError:
            _LOGGER.exception('Error while trying to close Kafka consumer')
        except Exception as e:
            _LOGGER.exception(f'Error while trying to close kafka connection: {e}')
            raise pigeon_exceptions.InboundException(f'Error while trying to close kafka consumer: {e}')
        finally:
            _LOGGER.debug('Exiting code for consuming via Kafka')
