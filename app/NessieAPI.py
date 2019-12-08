import time
import json

import requests as rq

from Configuration import Configuration


# Load configuration
config = Configuration()


def post_regobs(data_json):
    # Add secret API key to post
    data = json.dumps({'apikey': config['api']['apikey'], 'data': json.loads(data_json)})

    request_url = 'https://api.nokken.net/v0/regobs'


    # Lan post
    def _post_lan(n_attempt):
        request = rq.post(request_url, data=data)

        # Pass successful request or raise error
        if request.status_code == 200:
            return 1
        elif request.status_code in [429]:
            # This status_code will only be returned from Nessie if the user 
            # makes to many requests with a valid apikey.
            if n_attempt <= 2:
                time.sleep(120)
                return _do_post(n_attempt + 1)
            else:
                return request.status_code
                                 
        elif request.status_code is not None:
            return request.status_code
        else:
            return 0


    def _post_serialat(n_attempt):
        # TODO: Implement
        return 0


    # Do post
    if config['reporting']['connection'] == 'lan':
        return _post_lan(1)
    elif config['reporting']['connection'] == 'serial':
        return _post_serialat(1)
    else:
        return 0
