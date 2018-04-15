# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import time
from datetime import datetime, timedelta
import backtrader as bt
from strategies import *
import sys
import argparse
import os

def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            'Generic Backtester'
        )
    )
    parser.add_argument('live-ichi.py')

    parser.add_argument('--compression', default=int(os.environ['COMPRESSION']),
                        required=False, help='Compression (Time Frame) in minutes')

    parser.add_argument('--exchange', default='poloniex',
                        required=False, help='Exchange name')
    return parser.parse_args(pargs)


if __name__ == '__main__':
    parsed_args = parse_args(sys.argv)

    #Settings
    compression = parsed_args.compression  # minutes
    backload = 77
    market = parsed_args.exchange

    exchange = getattr(ccxt, market)()
    markets = exchange.load_markets()

    hist_start_date = datetime.utcnow() - timedelta(minutes=compression*backload)

    cerebro = bt.Cerebro()

    count = 0
    for symbol in markets:
        if symbol.endswith("USDT"):
            """
            count = count+1
            if count > 2:
                continue
            """
            print("Adding symbol "+symbol)
            data_ticks = bt.feeds.CCXT(exchange=market, symbol=symbol, name=market+"_"+symbol,
                   timeframe=bt.TimeFrame.Minutes, fromdate=hist_start_date, compression=compression, config={'rateLimit': 10000, 'enableRateLimit': True})

            cerebro.adddata(data_ticks, name=market+"_"+symbol)


    cerebro.addstrategy(IchimokuStrategyB)

    cerebro.run()
