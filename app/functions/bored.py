"""Bored module."""

import urllib3
import json


class Bored:
    """Defining base class for inheritence."""

    def bored(self):
        """Get random jokes from chucknorris API."""
        http = urllib3.PoolManager()
        req_return = http.request('GET', 'https://www.boredapi.com/api/activity?type=recreational')
        activity_data = json.loads(req_return.data.decode('utf-8'))
        # pprint.pprint(chuck)
        return activity_data['activity']
