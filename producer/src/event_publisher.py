from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
import os
import time
import logging

topic = os.environ.get('PCDEMO_CHANNEL') or 'stats'


class Publisher:

    def __init__(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        self.logger = logger

        while not hasattr(self, 'producer'):
            try:
                self.producer = KafkaProducer(bootstrap_servers="kafka:9092")
            except NoBrokersAvailable as err:
                self.logger.error("Unable to find a broker: {0}".format(err))
                time.sleep(1)

    def push(self, message):
        self.logger.debug("Publishing: {0}".format(message))
        # handle dynamic topic
        # if 'topic' specified in message
        try:
            self.logger.debug("Target topic: {0}".format(message["topic"]))
            topic = message["topic"]
        except KeyError:
            self.logger.debug("Topic key not found in message")        
        try:
            if self.producer:
                self.producer.send(topic,
                                   bytes(json.dumps(message).encode('utf-8')))
        except AttributeError:
            self.logger.error("Unable to send {0}. The producer does not exist."
                              .format(message))
