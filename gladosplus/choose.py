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
