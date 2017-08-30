#!/usr/bin/env python
# flake8: noqa
# encoding: utf-8
import os
import datetime
import time
import random
import socket
from random import choice
from jinja2 import Template

DEST = 'elk_1'
PORT = 10987
JSON = '{"@timestamp":"{{timestamp}},"message":"{{message}}"'
EOS  = ['.', '?', '!']
NUM  = 10.0
INT  = 60.0

def build_dict(words):
    """
    Build a dictionary from the words.

    (word1, word2) => [w1, w2, ...]  # key: tuple; value: list
    """
    d = {}
    for i, _ in enumerate(words):
        try:
            first, second, third = words[i], words[i+1], words[i+2]
        except IndexError:
            break
        key = (first, second)
        if key not in d:
            d[key] = []
        #
        d[key].append(third)

    return d


def generate_sentence(d):
    li = [key for key in d.keys() if key[0][0].isupper()]
    key = choice(li)

    li = []
    first, second = key
    li.append(first)
    li.append(second)
    while True:
        try:
            third = choice(d[key])
        except KeyError:
            break
        li.append(third)
        if third[-1] in EOS:
            break
        # else
        key = (second, third)
        first, second = key

    return ' '.join(li)

# #############

if __name__ == "__main__":
    pathname = os.path.realpath(__file__)
    fname = os.path.dirname(pathname) + "/seed.txt"
    with open(fname, "r") as f:
        text = f.read().decode("utf-8")

    words = text.split()
    d = build_dict(words)
    template = Template(JSON)
    sock = socket.socket(socket.AF_INET,    # Internet
                         socket.SOCK_DGRAM) # UDP

    while True:
        slept = 0
        fed = 0
        beg = datetime.datetime.now()
        rate = INT/NUM
        while fed < NUM and slept < INT:
            print slept
            now = datetime.datetime.now()
            wait = random.uniform(rate*0.7, rate*1.5)

            sent = generate_sentence(d)
            json = template.render({"message": sent})
            sock.sendto(sent.encode('utf-8'), (DEST, PORT))
            time.sleep(wait)
            fed = fed + 1
            slept = slept + wait

        spent = (now - beg).total_seconds()
        wait = INT - spent
        if wait > 0:
            time.sleep(INT - spent)
