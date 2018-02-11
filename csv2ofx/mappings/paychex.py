from __future__ import absolute_import

from operator import itemgetter

mapping = {
    'has_header': True,
    'is_split': False,
    'currency': 'USD',
    'delimiter': ',',
    'date': itemgetter('Date'),
    'amount': itemgetter('Amount'),
    'price': itemgetter('Price'),
    'shares': itemgetter('Shares'),
    'investment': itemgetter('InvestmentName'),
    'ticker': itemgetter('Ticker'),
    'desc': itemgetter('Transaction'),
}
