"""Chuck module."""

import urllib3
import json


class Chuck:
    """Defining base class for inheritence."""

    def chuck(self):
        """Get random jokes from chucknorris API."""
        http = urllib3.PoolManager()
        req_return = http.request('GET', 'https://api.chucknorris.io/jokes/random')
        chuck = json.loads(req_return.data.decode('utf-8'))
        # pprint.pprint(chuck)
        return chuck['value']
