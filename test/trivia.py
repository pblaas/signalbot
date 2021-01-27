"""Collection of Bot functions."""

import random
import json
import urllib3
import html


def trivia():
    """Get random jokes from chucknorris API."""
    http = urllib3.PoolManager()
    req_return = http.request('GET', 'https://opentdb.com/api.php?amount=1')
    trivia_data = json.loads(req_return.data.decode('utf-8'))
    all_answers = trivia_data['results'][0]['incorrect_answers']
    all_answers.insert(0, trivia_data['results'][0]['correct_answer'])
    random.shuffle(all_answers)
    str = ","
    shuffled_string = str.join(all_answers)
    print(f"""Trivia:
    {html.unescape(trivia_data['results'][0]['question'])}
    Options: {shuffled_string}
    """)


trivia()
