from cryptography.fernet import Fernet

import json

class Cryptography:
    def __init__(self):
        self.key = Fernet.generate_key()

    def enc_api_tokens( self, client_id, client_secret):
        fernet = Fernet(self.key)

        enc_client_id = fernet.encrypt(client_id.encode()).decode()
        enc_client_secret = fernet.encrypt(client_secret.encode()).decode()
        
        with open('./backend/configuration files/secret.json', 'w+') as f:
            dict = {
                "client_id": enc_client_id,
                "client_secret": enc_client_secret
            }
            f.write(json.dumps(dict))

    def dec_api_tokens(self):
        fernet = Fernet(self.key)
        with open('./backend/configuration files/secret.json', 'r') as f:
            data = json.load(f)
            enc_id, enc_secret = data['client_id'], data['client_secret']
            dec_id = fernet.decrypt(enc_id.encode()).decode()
            dec_secret = fernet.decrypt(enc_secret.encode()).decode()
            return dec_id, dec_secret
