"""Trivia module."""

import urllib3
import json
import random
import html


class Trivia:
    """Defining base class for inheritence."""

    @staticmethod
    def trivia():
        """Get random questions from opentdb trivia API."""
        http = urllib3.PoolManager()
        req_return = http.request('GET', 'https://opentdb.com/api.php?amount=1')
        trivia_data = json.loads(req_return.data.decode('utf-8'))
        all_answers = trivia_data['results'][0]['incorrect_answers']
        all_answers.insert(0, trivia_data['results'][0]['correct_answer'])
        random.shuffle(all_answers)
        comma = ","
        shuffled_string = comma.join(all_answers)
        return f"""Trivia:
        {html.unescape(trivia_data['results'][0]['question'])}
        Options: {shuffled_string}
        """
