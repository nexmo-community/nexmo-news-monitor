# https://github.com/jpadilla/pyjwt -- pip3 install PyJWT
import jwt
import time
import json
import requests
from uuid import uuid4
from pprint import pprint


class SMSClient:

    def __init__(self, app_id, filename, expiry):

        f = open(filename, 'r')
        self.private_key = f.read()
        f.close()

        self.app_id = app_id
        self.expiry = expiry

        return

    def send_message(self, sms_sender, sms_recipient, msg):

        print("Sending SMS message -> from: %s to: %s msg: %s" %
              (sms_sender, sms_recipient, msg))

        data_body = {
            "from": {
                "type": "sms",
                "number": sms_sender
            },
            "to": {
                "type": "sms",
                "number": sms_recipient
            },
            "message": {
                "content": {
                    "type": "text",
                    "text": msg
                }
            }
        }

        data_body = json.dumps(data_body)

        self.payload = {
            'application_id': self.app_id,
            'iat': int(time.time()),
            'jti': str(uuid4()),
            'exp': int(time.time()) + self.expiry,
        }

        gen_jwt = jwt.encode(self.payload, self.private_key, algorithm='RS256')
        auth = b'Bearer '+gen_jwt
        headers = {'Authorization': auth, 'Content-Type': 'application/json'}
        r = requests.post('https://api.nexmo.com/v0.1/messages',
                          headers=headers, data=data_body)
        j = r.json()
        pprint(j)
