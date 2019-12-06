import time
import json

import requests as rq


def post_regobs(data_json):
    # Add secret API key to post
    data = json.dumps({'apikey': 'njskdfgl834q3q4bt3sd', 'data': json.loads(data_json)})

    request_url = 'https://api.nokken.net/v0/regobs'

    def _do_post(n_attempt):
        request = rq.post(request_url, data=data)

        # Pass successful request or raise error
        if request.status_code == 200:
            return 1
        elif request.status_code in [429]:
            # This status_code will only be returned from Nessie if the user makes to many requests
            # with a valid apikey.
            retry_after = 120
            print('Got error status {}. Will retry once after Nessie\'s requested time out.'.
                  format(request.status_code))

            # Cap max retires
            if n_attempt <= 2:
                time.sleep(retry_after)
                return _do_post(n_attempt + 1)
            else:
                raise ValueError('An error occurred. Max attempts reached. Nessie API error code {}.'.
                                 format(request.status_code))
                                 
        elif request.status_code is not None:
            raise ValueError('Error {}.'.format(request.status_code))
        else:
            raise ValueError('There was an unknown problem getting observations from Nessie.')

    return _do_post(1)
    