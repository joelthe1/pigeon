'''
Pigeon specific exceptions
'''

class PigeonException(Exception):
    """Parent exception class for custom exceptions raised from this project"""


class ConfigException(PigeonException):
    """Parent exception class for Configuration exceptions"""

class InboundException(PigeonException):
    """Parent exception class for Inbound exceptions"""

class OutboundException(PigeonException):
    """Parent exception class for Outbound exceptions"""

class InternalError(PigeonException):
    """Parent exception class for errors raised from a variety of low-level internal plumbing"""
