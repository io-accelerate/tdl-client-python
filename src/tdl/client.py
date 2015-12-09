__author__ = 'tdpreece'
__author__ = 'tdpreece'
import logging
import time
import json
from collections import OrderedDict

import stomp

logger = logging.getLogger('tdl.client')
logger.addHandler(logging.NullHandler())


class Client(object):
    def __init__(self, hostname, port, username):
        self.hostname = hostname
        self.port = port

    def go_live_with(self, implementation_map):
        handling_strategy = RespondToAllRequests(implementation_map)
        self.run(handling_strategy)

    def trial_run_with(self, implementation_map):
        handling_strategy = PeekAtFirstRequest(implementation_map)
        self.run(handling_strategy)

    def run(self, handling_strategy):
        try:
            remote_broker = RemoteBroker(self.hostname, self.port)
            remote_broker.subscribe(handling_strategy)
            time.sleep(1)
            remote_broker.close()
        except Exception as e:
            logger.exception('Problem communicating with the broker.')


class HandlingStrategy(object):
    def __init__(self, implementation_map):
        self.implementation_map = implementation_map

    def respond_to(self, message):
        decoded_message = json.loads(message)
        method = decoded_message['method']
        params = decoded_message['params']
        id = decoded_message['id']
        implementation = self.implementation_map[method]
        try:
           result = implementation(params)
        except Exception as e:
           logger.info('The user implementation has thrown an exception: {}'.format(e.message))
           result = None
        params_str = ", ".join([str(p) for p in params])
        print('id = {id}, req = {method}({params}), resp = {result}'.format(id=id, method=method, params=params_str,
                                                                           result=result))
        if result is not None:
            response = OrderedDict([
                ('result', result),
                ('error', None),
                ('id', id),
                ])
        return response

class RespondToAllRequests(HandlingStrategy):
    def process_next_message_from(self, remote_broker, headers, message):
        response = self.respond_to(message)
        if response is not None:
            remote_broker.acknowledge(headers)
            remote_broker.publish(response)

class PeekAtFirstRequest(HandlingStrategy):
    def process_next_message_from(self, remote_broker, headers, message):
        self.respond_to(message)

class Listener(stomp.ConnectionListener):
    def __init__(self, remote_broker, handling_strategy):
        self.remote_broker = remote_broker
        self.handling_strategy = handling_strategy

    def on_message(self, headers, message):
        self.handling_strategy.process_next_message_from(self.remote_broker, headers, message)



class RemoteBroker(object):
    def __init__(self, hostname, port):
        hosts = [(hostname, port)]
        self.conn = stomp.Connection(host_and_ports=hosts)
        self.conn.start()
        self.conn.connect(wait=True)

    def acknowledge(self, headers):
        self.conn.ack(headers['message-id'], headers['subscription'])

    def publish(self, response):
        self.conn.send(
            body=json.dumps(response, separators=(',', ':')),
            destination='test.resp'
        )

    def subscribe(self, handling_strategy):
        listener = Listener(self, handling_strategy)
        self.conn.set_listener('listener', listener)
        self.conn.subscribe(destination='test.req', id=1, ack='client-individual')

    def close(self):
        self.conn.disconnect()