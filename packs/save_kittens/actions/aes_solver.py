import json
import base64

from Crypto.Cipher import AES
from Crypto.Hash import MD5

from st2actions.runners.pythonrunner import Action

__all__ = [
    'AESDecrypt'
]


class AESDecrypt(Action):
    def run(self, message, aes_key=None, encrypt=False):
        if not aes_key:
            aes_key = "this_is_so_secure"

        key = MD5.new(aes_key).hexdigest()

        aes_handler = AES.new(key, AES.MODE_CBC, 'Save the kittens')

        if encrypt:
            padding = 16 - (len(message) % 16)

            message += chr(padding) * padding

            result = {
                'message': base64.b64encode(aes_handler.encrypt(message))
            }

            return json.dumps(result)

        else:
            message = base64.b64decode(message)
            decrypted_message = aes_handler.decrypt(message)
            unpadded_message = decrypted_message[:- ord(decrypted_message[-1])]

            result = {
                'message': unpadded_message
            }

            return json.dumps(result)
