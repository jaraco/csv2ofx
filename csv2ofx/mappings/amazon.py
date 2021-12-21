from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os
import functools
import collections
from operator import itemgetter


def all_but_the_last_n(iterable, count):
    q = collections.deque()
    i = iter(iterable)
    for n in range(count):
        q.append(next(i))
    for item in i:
        q.append(item)
        yield q.popleft()


all_but_last = functools.partial(all_but_the_last_n, count=1)


def parse_cards(setting):
    if setting is None:
        return []
    return setting.split(',')


def exclude_cards(records):
    setting = os.environ.get('AMAZON_EXCLUDE_CARDS', None)
    cards = parse_cards(setting)
    filter_ = lambda row: not any(card in row['payments'] for card in cards)
    return filter(filter_, records)


def exclude_bad_rows(records):
    """
    Workaround for philipmulcahy/azad#174.
    """
    filter_ = lambda row: 'Grand Total' not in row['total']
    return filter(filter_, records)


# from jaraco.functools
def compose(*funcs):
    def compose_two(f1, f2):
        return lambda *args, **kwargs: f1(f2(*args, **kwargs))

    return functools.reduce(compose_two, funcs)


mapping = {
    'has_header': True,
    'process_records': compose(exclude_cards, all_but_last, exclude_bad_rows),
    'delimiter': ',',
    'bank': 'Amazon Purchases',
    'account_id': os.environ.get('AMAZON_PURCHASES_ACCOUNT', '100000001'),
    'date': itemgetter('date'),
    'amount': itemgetter('total'),
    'payee': 'Amazon',
    'desc': itemgetter('items'),
    'id': itemgetter('order id'),
    'type': 'DEBIT',
}
