import argparse
import os
import logging.config
from zeep import Client
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport
import requests

# Enable Zeep debug logging for SOAP request/response details
logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'verbose': {'format': '%(name)s: %(message)s'}
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'zeep': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        }
    }
})

parser = argparse.ArgumentParser()
parser.add_argument('--url', required=True)
parser.add_argument('--username', required=True)
parser.add_argument('--password', required=True)
args = parser.parse_args()
