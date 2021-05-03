#!/usr/bin/env python3
import sys
import re
from difflib import get_close_matches
from pprint import pprint


def get_blacklist() -> set[str]:

    blacklist = list[str]()

    with open('words/1-1000.txt', 'r') as fp:
        blacklist += fp.readlines()

    with open('blacklist.txt', 'r') as fp:
        blacklist += fp.readlines()

    return set(blacklist)


def main() -> None:

    if len(sys.argv) < 2:
        print('usage: order [filename]')
        sys.exit(1)

    text: str
    with open(sys.argv[1], 'r') as fp:
        text = fp.read()

    order: list[str] = re.findall(r'\b[A-Za-z0-9]+\b', text)
    blacklist = get_blacklist()

    freq = dict[str, int]()
    for idx, ord in enumerate(order):

        print(f'Reading ord {idx} / {len(order)}', end='\r')

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
    pprint(sorted(freq, key=freq.__getitem__, reverse=True)[:10])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
