'''
App level configurations
'''
import typing
import logging
from dataclasses import dataclass, field


@dataclass
class Configuration:
    log_level: str = field(default=logging.INFO,
                           metadata={'env_var_name': 'ASED_PIGEON_LOG_LEVEL'})
    inbound_host: str = field(default=None,
                              metadata={'env_var_name': 'ASED_PIGEON_INBOUND_HOST'})
    inbound_port: str = field(default=None,
                              metadata={'env_var_name': 'ASED_PIGEON_INBOUND_PORT'})
    outbound_host: str = field(default=None,
                               metadata={'env_var_name': 'ASED_PIGEON_OUTBOUND_HOST'})
    outbound_port: str = field(default=None,
                               metadata={'env_var_name': 'ASED_PIGEON_OUTBOUND_PORT'})
    kafka_host: str = field(default=None,
                            metadata={'env_var_name': 'ASED_PIGEON_KAFKA_HOST'})
    kafka_port: str = field(default=None,
                            metadata={'env_var_name': 'ASED_PIGEON_KAFKA_PORT'})
    inbound_kafka_topic: str = field(default=None,
                                     metadata={'env_var_name': 'ASED_PIGEON_INBOUND_KAKFA_TOPIC'})
    outbound_kafka_topics: str = field(default=None,
                                       metadata={'env_var_name': 'ASED_PIGEON_OUTBOUND_KAKFA_TOPICS'})
    output_handler_count: str = field(default="1",
                                metadata={'env_var_name': 'ASED_PIGEON_OUTPUT_HANDLER_COUNT'})
    udp_listener_count: str = field(default="1",
                                    metadata={'env_var_name': 'ASED_PIGEON_UDP_LISTENER_COUNT'})
