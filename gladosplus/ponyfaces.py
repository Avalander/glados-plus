import json
import random
import urllib.request

import glados



PONYFACES_URL = 'http://ponyfac.es/api.json'
GIFS = [ 1, 2, 3, 24, 33, 38, 41, 52, 55, 73, 75, 77, 79, 81, 82, 85, 89, 90, 91, 92, 97, 101, 111, 139, 144, 146, 150, 161, 162 ]

def has_content(text='Some content required'):
    def outer_wrapper(func):
        def wrapper(*args):
            content = args[2]
            if not content:
                yield from args[0].client.send_message(args[1].channel, text)
            else:
                yield from func(*args)
        return wrapper
    return outer_wrapper

def has_no_content(text=None):
    def outer_wrapper(func):
        def wrapper(*args):
            content = args[2]
            if content:
                yield from args[0].client.send_message(args[1].channel,
                    text or 'I don\'t know what to do with "{}"'.format(content))
            else:
                yield from func(*args)
        return wrapper
    return outer_wrapper

class Ponyfaces(glados.Module):
    def get_help_list(self):
        return [
            glados.Help('ponyface', '', 'Return a random pony face.'),
            glados.Help('ponyface:id', '<id>', 'Returns a pony face with the specified id.'),
            glados.Help('ponyface:tags', '', 'Returns a list of all available tags.'),
            glados.Help('ponyface:tag', '<tag>', 'Returns a pony face with the specified tag.'),
            glados.Help('ponyface:categories', '', 'Returns a list of all available categories.'),
            glados.Help('ponyface:category', '<category id>', 'Returns a pony face with the specified category id.')
        ]

    @glados.Module.commands('ponyface', 'pf')
    def ponyface(self, message, content):
        if content and content.isnumeric():
            yield from self.ponyface_id(message, content)
            return
        elif content:
            yield from self.ponyface_tag(message, content)
            return
        total_faces = int(get_json_response('{}/tags'.format(PONYFACES_URL))['total_faces'])
        pony_id = random.randint(1, total_faces)
        pony_response = get_json_response('{}/id:{}'.format(PONYFACES_URL, pony_id))
        yield from self.client.send_message(message.channel, self._find_image(pony_response))

    @glados.Module.commands('ponyface:id', 'pf:id')
    @has_content('Please, specify a pony id')
    def ponyface_id(self, message, content):
        try:
            int(content)
        except ValueError:
            yield from self.client.send_message(message.channel,
                'Pony id must be a positive integer')
            return
        pony_response = get_json_response('{}/id:{}'.format(PONYFACES_URL, content))
        yield from self.client.send_message(message.channel, self._find_image(pony_response))

    @glados.Module.commands('ponyface:tags', 'pf:tags')
    @has_no_content()
    def ponyface_tags(self, message, content):
        pony_response = get_json_response('{}/tags'.format(PONYFACES_URL))
        tags_text = '\n'.join(pony_response['tags'])
        yield from self.client.send_message(message.author, tags_text)
        yield from self.client.send_message(message.channel,
            'I\'m sending you a giantic wall of direct message with the list of tags')

    @glados.Module.commands('ponyface:tag', 'pf:tag')
    @has_content('Please, specify a tag')
    def ponyface_tag(self, message, content):
        pony_response = get_json_response('{}/tag:{}'.format(PONYFACES_URL, content))
        yield from self.client.send_message(message.channel, self._find_image(pony_response))

    @glados.Module.commands('ponyface:categories', 'pf:categories')
    @has_no_content()
    def ponyface_categories(self, message, content):
        pony_response = get_json_response('{}/categories'.format(PONYFACES_URL))
        categories_text = '\n'.join(map(lambda x: '{id}: {name}'.format(**x), pony_response['category']))
        yield from self.client.send_message(message.channel, categories_text)

    @glados.Module.commands('ponyface:category', 'pf:category', 'pf:cat')
    @has_content('Please, specify a category')
    def ponyface_category(self, message, content):
        pony_response = get_json_response('{}/category:{}'.format(PONYFACES_URL, content))
        yield from self.client.send_message(message.channel, self._find_image(pony_response))

    def _find_image(self, pony_response):
        if pony_response['faces']:
            pony_face = random.choice(pony_response['faces'])
            '''
            HACK: Discord doesn't seem to recognise gifs if the url doesn't end in .gif.
            The other solution would be to request the image and check the Content-Type, but
            I don't want to consume bandwidth downloading images, so I did this hack instead.
            '''
            image_url = pony_face['image']
            return '{}.gif'.format(image_url) if is_gif(pony_face) else image_url
        return 'No pony found :('


def is_gif(pony_face):
    return int(pony_face['id']) in GIFS


def get_json_response(url):
    with urllib.request.urlopen(urllib.parse.quote_plus(url, safe='/:')) as response:
        data = response.read()
        encoding = response.info().get_content_charset('utf-8')
        return json.loads(data.decode(encoding))
