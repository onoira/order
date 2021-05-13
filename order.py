#!/usr/bin/env python3
import os
import sys
import re
import time
import pickle
from difflib import get_close_matches
from pprint import pprint
from typing import Any, Callable, IO, TypeVar

TOP_COUNT = 10
_PICKLE = 'blacklist.pickle'
_RET = TypeVar('_RET')


def timed(f: Callable[..., _RET]) -> Callable[..., _RET]:

    def inner(*args: Any) -> Any:

        tfrom = time.time()
        retval = f(*args)
        ttill = time.time()

        print(f'({(ttill - tfrom)*1000.0:.2f}ms)')

        return retval

    return inner


@timed
def get_blacklist() -> set[str]:

    def new() -> set[str]:

        blacklist = list[str]()

        with open('words/1-1000.txt', 'r') as fp:
            blacklist += fp.readlines()

        with open('blacklist.txt', 'r') as fp:
            blacklist += fp.readlines()

        r = set(blacklist)

        jar: IO[bytes]
        with open(_PICKLE, 'wb') as jar:
            pickle.dump(r, jar)

        return r

    def load() -> set[str]:

        r: set[str]

        with open(_PICKLE, 'rb') as jar:
            r = pickle.load(jar)

        return r

    f: Callable[[], set[str]]
    if os.path.exists(_PICKLE):
        f = load
    else:
        f = new

    return f()


@timed
def read_file(filename: str) -> str:
    with open(filename, 'r') as fp:
        return fp.read()


@timed
def get_order(text: str) -> list[str]:
    return re.findall(r'\b[A-Za-z0-9]+\b', text)


@timed
def get_ord_frequency(order: list[str], blacklist: set[str]) -> dict[str, int]:

    freq = dict[str, int]()
    for idx, ord in enumerate(order):

        print(f'{idx} / {len(order)}', end='\r')

        if len(ord) == 1:
            continue

        if ord.isnumeric():
            continue

        k = ord.lower()
        if len(get_close_matches(k, blacklist)) > 0:
            continue

        k_match = (get_close_matches(k, freq.keys()) or [k, ])[0]
        freq[k_match] = freq.get(k_match, 0) + 1

    print()
    return freq


@timed
def get_freq_top(freq: dict[str, int]) -> list[tuple[str, int]]:
    return [
        (k, freq[k])
        for k in sorted(freq, key=freq.__getitem__, reverse=True)[:TOP_COUNT]
    ]


def main(*argv: str) -> None:

    if len(argv) < 1:
        print('usage: order [filename]')
        sys.exit(1)

    filename = argv[0]

    print(f'reading contents of {filename}...', end='')
    text = read_file(filename)

    print('extracting order...', end='')
    order = get_order(text)

    print('reading blacklist...', end='')
    blacklist = get_blacklist()

    print('counting ord frequency...')
    freq = get_ord_frequency(order, blacklist)

    print(f'finding top {TOP_COUNT}...', end='')
    freq_top = get_freq_top(freq)

    pprint(freq_top)


if __name__ == '__main__':
    try:
        main(*sys.argv[1:])
    except KeyboardInterrupt:
        pass
