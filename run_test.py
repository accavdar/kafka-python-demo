#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string
from configparser import ConfigParser

import sys
from kafka import KafkaConsumer, KafkaProducer

CONFIG_FILE = 'prod.conf'


def run_test(hostname='localhost', port=9092, num_messages=1000):
    connect_string = '{}:{}'.format(hostname, port)
    producer = KafkaProducer(bootstrap_servers=connect_string, retries=5, max_block_ms=10000,
                             value_serializer=str.encode)

    consumer = KafkaConsumer(bootstrap_servers=connect_string, group_id=None,
                             consumer_timeout_ms=10000, auto_offset_reset='earliest',
                             value_deserializer=bytes.decode)

    topic = _random_string(5)

    futures = []
    for i in range(num_messages):
        futures.append(producer.send(topic, 'msg %d' % i))
    ret = [f.get(timeout=30) for f in futures]
    assert len(ret) == num_messages
    producer.close()
    print('%d messages sent successfully' % num_messages)

    consumer.subscribe([topic])
    received_messages = set()
    for i in range(num_messages):
        try:
            received_messages.add(next(consumer).value)
        except StopIteration:
            break

    assert received_messages == set(['msg %d' % i for i in range(num_messages)])
    print('%d messages read successfully' % len(received_messages))
    print(received_messages)


def _parse_config(filename):
    config_dict = {}
    config_parser = ConfigParser()
    config_parser.read(filename)

    for section in config_parser.sections():
        config_dict[section] = {}
        for option in config_parser.options(section):
            try:
                config_dict[section][option] = config_parser.get(section, option)
            except:
                print("Exception on parsing config section %s, option %s" % section, option)
                config_dict[section][option] = None
    return config_dict


def _random_string(l):
    return "".join(random.choice(string.ascii_letters) for _ in range(l))


if __name__ == '__main__':
    config = _parse_config(CONFIG_FILE)
    messages = int(sys.argv[1]) if len(sys.argv) > 1 else int(config['request']['message_count'])
    run_test(hostname=config['kafka']['hostname'],
             port=int(config['kafka']['port']),
             num_messages=messages)
