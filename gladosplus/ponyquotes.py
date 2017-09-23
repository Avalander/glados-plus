import json
import urllib

import glados


PONY_QUOTES_API = 'http://api.ponyquotes.com/v1'

class PonyQuotes(glados.Module):
    def get_help_list(self):
        return [
            glados.Help('pquote', '<pony?>', 'Returns a pony quote.')
        ]

    @glados.Module.commands('pquote')
    def pony_quote(self, message, content):
        query_string = urllib.parse.urlencode({
            'pony': content
        }) if content else ''
        try:
            result = get_json_response('{}?{}'.format(PONY_QUOTES_API, query_string))
            yield from self.client.send_message(message.channel,
                '"{quote}" --*{pony}*'.format(**result))
        except urllib.error.HTTPError as error:
            yield from self.client.send_message(message.channel, 'No quotes found.')

def get_json_response(url):
    with urllib.request.urlopen(url) as response:
        data = response.read()
        encoding = response.info().get_content_charset('utf-8')
        return json.loads(data.decode(encoding))
