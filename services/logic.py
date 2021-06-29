import random


def create_code(n: int = 10):
    """Generates a unique code"""
    code_characters = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    return ''.join([code_characters[random.randrange(0, len(code_characters))] for i in range(n)])
