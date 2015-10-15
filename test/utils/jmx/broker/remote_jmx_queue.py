from jolokia_session import JolokiaSession


class RemoteJmxQueue(object):
    def __init__(self, jolokia_session, broker_name, queue_name):
        self.jolokia_session = jolokia_session
        self.queue_bean = (
            "org.apache.activemq:type=Broker,brokerName={},"
            "destinationType=Queue,destinationName={}"
        ).format(broker_name, queue_name)

# send_text_message_payload = {
#     "type":"exec",
#     "mbean":"org.apache.activemq:type=Broker,brokerName=TEST.BROKER,destinationType=Queue,destinationName=test.req",
#     "operation":"sendTextMessage(java.lang.String)",
#     "arguments":["test message"]
# }

    def send_text_message(self, request):
        operation = {
            'type': 'exec',
            'mbean': self.queue_bean,
            'operation': 'sendTextMessage(java.lang.String)',
            'arguments': [request]
        }
        self.jolokia_session.request(operation)

    def get_size():
        pass
    # attribute = {
    #     type: 'read',
    #     mbean: queue_bean,
    #     attribute: 'QueueSize',
    # }
    # jolokia_session.request(attribute)

    def get_message_contents():
        pass
    # operation = {
    #     type: 'exec',
    #     mbean: queue_bean,
    #     operation: 'browse()',
    # }
    # result = jolokia_session.request(operation)
    # result.map  { |composite_data|
    #   if composite_data.has_key?('Text')
    #     composite_data['Text']
    #   else
    #     composite_data['BodyPreview'].to_a.pack('c*')
    #
    # }

    def purge():
        pass
    # operation = {
    #     type: 'exec',
    #     mbean: queue_bean,
    #     operation: 'purge()',
    # }
    # jolokia_session.request(operation)
    #
    #