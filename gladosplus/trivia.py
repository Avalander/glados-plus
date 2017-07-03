import base64
import functools
import json
import random
import urllib.request
import urllib.parse

import glados
from ._validator import has_content, has_no_content, is_number


TRIVIA_API = 'https://opentdb.com/api.php?{}'

MULTIPLE_QUESTION = '''**Question:** {}

 (1) {}
 (2) {}
 (3) {}
 (4) {}
 
 *Answer with* `.trivia:answer`, *complete with* `.trivia:end`'''

BOOLEAN_QUESTION = '''**Question:** {}

 (1) True
 (2) False
 
 *Answer with* `.trivia:answer`, *complete with* `.trivia:end`'''

QUESTION_FORMATS = {
    'multiple': MULTIPLE_QUESTION,
    'boolean': BOOLEAN_QUESTION
}

SUMMARY = '''**Question:** {}

**Answer:** {}

**Correct answerers:** {}
'''


class Trivia(glados.Module):
    def setup_memory(self):
        self.get_memory()['open-trivias'] = {}

    def get_help_list(self):
        return [
            glados.Help('', '', '')
        ]

    @glados.Module.commands('trivia:start')
    @has_no_content()
    def start(self, message, content):
        memory = self.get_memory()
        if not message.channel in memory['open-trivias']:
            trivia = base64_wrap(query_trivia_api, {'amount': 1})[0]
            choices = trivia['incorrect_answers'] + [trivia['correct_answer']]
            random.shuffle(choices)
            trivia['choices'] = choices
            trivia['user_answers'] = {}
            memory['open-trivias'][message.channel] = trivia
        else:
            trivia = memory['open-trivias'][message.channel]
        yield from self.client.send_message(message.channel, QUESTION_FORMATS[trivia['type']].format(
            trivia['question'], *trivia['choices']))

    @glados.Module.commands('trivia:answer')
    @has_content('Please, provide an answer to the trivia.', is_number(1, 4))
    def answer(self, message, content):
        try:
            trivia = self.get_memory()['open-trivias'][message.channel]
        except KeyError:
            yield from self.client.send_message(message.channel, 'Start a new trivia with `.trivia:start`.')
        answer = trivia['choices'][int(content) - 1]
        if message.author.id in trivia['user_answers']:
            yield from self.client.send_message(message.channel, '{}, you have already answered this question.'.format(message.author.name))
            return
        trivia['user_answers'][message.author.id] = {
            'name': message.author.name,
            'answer': answer
        }
        yield from self.client.send_message(message.channel, 'Answer registered.')

    @glados.Module.commands('trivia:end')
    @has_no_content()
    def end(self, message, content):
        try:
            memory = self.get_memory()
            trivia = memory['open-trivias'][message.channel]
            del memory['open-trivias'][message.channel]
        except KeyError:
            yield from self.client.send_message(message.channel, 'Start a new trivia with `.trivia:start`.')
        answers = trivia['user_answers']
        correct_answerers = [x[1]['name'] for x in answers.items() if x[1]['answer'] == trivia['correct_answer']]
        yield from self.client.send_message(message.channel, SUMMARY.format(
            trivia['question'],
            trivia['correct_answer'],
            ', '.join(correct_answerers) if correct_answerers else 'Nobody, you losers.'
        ))


def query_trivia_api(params):
    query_params = urllib.parse.urlencode(params)
    with urllib.request.urlopen(TRIVIA_API.format(query_params)) as response:
        data = response.read()
        encoding = response.info().get_content_charset('utf-8')
        return json.loads(data.decode(encoding))

def base64_wrap(func, params):
    params['encode'] = 'base64'
    data = func(params)
    return [functools.reduce(base64_reducer, x.items(), {}) for x in data['results']]

def base64_reducer(acc, item):
    key = item[0]
    value = item[1]
    if isinstance(value, list):
        decoded = [base64.b64decode(x).decode('utf-8') for x in value]
    else:
        decoded = base64.b64decode(value).decode('utf-8')
    acc[key] = decoded
    return acc
