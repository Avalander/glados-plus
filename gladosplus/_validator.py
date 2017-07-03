def has_content(text='Some content required', validator=None):
    def outer_wrapper(func):
        def wrapper(*args):
            content = args[2]
            if not content:
                yield from args[0].client.send_message(args[1].channel, text)
            else:
                if validator:
                    try:
                        validator(content)
                    except ValueError as error:
                        yield from args[0].client.send_message(args[1].channel, error)
                        return
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

def is_number(min_value=None, max_value=None):
    def validator(content):
        value = int(content)
        if min_value and value < min_value:
            raise ValueError('Value should be a number between {} and {}.'.format(min_value, max_value)
                if max_value else 'Value should be a number equal or greater than {}.'.format(min_value))
        if max_value and value > max_value:
            raise ValueError('Value should be a number between {} and {}.'.format(min_value, max_value)
                if min_value else 'Value should be equal or less than {}.'.format(max_value))
    return validator
