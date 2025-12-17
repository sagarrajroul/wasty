import random


def get_random_string(length=12, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    """
    Return a  generated random string.
    """

    return ''.join(random.choice(allowed_chars) for _ in range(length))