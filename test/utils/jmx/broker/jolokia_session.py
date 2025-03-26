import json
import requests


class JolokiaSession(object):

    def __init__(self, jolokia_uri):
        self.uri = jolokia_uri

    @staticmethod
    def connect(host, admin_port):
        jolokia_url = "http://{host}:{admin_port}/api/jolokia".format(host=host, admin_port=admin_port)
        endpoint = '/version'
        response = requests.get(jolokia_url + endpoint, headers={"Origin":"http://localhost"})
        jolokia_version = json.loads(response.text)['value']['agent']
        if not jolokia_version:
            raise Exception("Failed to retrieve the right Jolokia version.")
        return JolokiaSession(jolokia_url)

    def request(self, jolokia_payload):
        http_response = requests.post(self.uri, json=jolokia_payload, headers={"Origin":"http://localhost"})
        if http_response.status_code != 200:
            msg = (
                "Failed Jolokia call: {response_code} {response_body}"
            ).format(
                response_code=http_response.status_code,
                response_body=http_response.text,
            )
            raise Exception(msg)
        jolokia_response = json.loads(http_response.text)
        return jolokia_response['value']
