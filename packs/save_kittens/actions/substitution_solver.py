from random import random
from math import floor

from st2actions.runners.pythonrunner import Action

__all__ = [
    'SubSolver'
]

ALPHABET = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')


def _gen_cipher_mapping():
    cipher = []
    alphabet = list(ALPHABET)

    for letter in ALPHABET:
        random_letter = int(floor(random() * len(alphabet)))
        mapping = (letter, alphabet.pop(random_letter))

        cipher.append(mapping)

    return cipher


def _get_cipher_mapping(cipher):
    cipher_map = []
    alphabet = list(ALPHABET)

    for _ in range(len(ALPHABET)):
        mapping = (alphabet.pop(0), cipher.pop(0))

        cipher_map.append(mapping)

    return cipher_map


def _get_cipher(cipher):
    cipher_text = []

    for _, mapping in cipher:
        cipher_text.append(mapping)

    return ''.join(cipher_text)


def _encrypt_letter(letter, cipher):
    if letter == ' ':
        return ' '

    for plain_text, cipher_text in cipher:
        if letter == plain_text:
            return cipher_text


def _decrypt_letter(letter, cipher):
    if letter == ' ':
        return ' '

    for plain_text, cipher_text in cipher:
        if letter == cipher_text:
            return plain_text


def _encrypt_text(text, cipher):
    encrypted_text = []
    text_list = list(text)

    for letter in text_list:
        encrypted_text.append(_encrypt_letter(letter, cipher))

    return ''.join(encrypted_text)


def _decrypt_text(text, cipher):
    decrypted_text = []
    text_list = list(text)

    for letter in text_list:
        decrypted_text.append(_decrypt_letter(letter, cipher))

    return ''.join(decrypted_text)


class SubSolver(Action):
    def run(self, encode, message, cipher=None):
        if encode:
            cipher_map = _gen_cipher_mapping()
            cipher = _get_cipher(cipher_map)
            cipher_text = _encrypt_text(message, cipher_map)

            result = {
                'cipher_text': cipher_text,
                'cipher': cipher
            }

            return result

        else:
            cipher_list = list(cipher)

            cipher_map = _get_cipher_mapping(cipher_list)
            result = {
                'message': _decrypt_text(message, cipher_map)
            }

            return result
