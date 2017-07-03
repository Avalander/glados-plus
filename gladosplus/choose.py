import random

import glados
from ._validator import has_content


class Choose(glados.Module):
    def get_help_list(self):
        return [
            glados.Help('choose', '<items>', 'Chooses one of the comma-separated items.')
        ]

    @glados.Module.commands('choose')
    @has_content()
    def choose(self, message, content):
        choice = random.choice(content.split(',')).strip()
        yield from self.client.send_message(message.channel, choice)

    @glados.Module.rules('^\.choose:(\d+) (.*)$')
    def choose_many(self, message, match):
        amount = int(match.group(1))
        items = match.group(2).split(',')
        if len(items) < amount:
            yield from self.client.send_message(message.channel,
                'You asked me {} items but only provided {}.'.format(amount, len(items)))
            return
        random.shuffle(items)
        selection = ', '.join(items[:amount])
        yield from self.client.send_message(message.channel, selection)
