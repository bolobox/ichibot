# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import time
from datetime import datetime, timedelta
import backtrader as bt
from strategies import *
import sys
import argparse

def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            'Generic Backtester'
        )
    )
    parser.add_argument('live-ichi.py')

    parser.add_argument('--compression', default=30,
                        required=False, help='Compression (Time Frame) in minutes')

    parser.add_argument('--exchange', default='poloniex',
                        required=False, help='Exchange name')
    return parser.parse_args(pargs)


if __name__ == '__main__':
    parsed_args = parse_args(sys.argv)

    #Settings
    compression =  parsed_args.compression # minutes
    backload = 77*2
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

    """
    data_ticks_btc = bt.feeds.CCXT(exchange=market, symbol="BTC/USD", name=market+"_BTC/USD",
       timeframe=bt.TimeFrame.Minutes, fromdate=hist_start_date, compression=compression, config={'rateLimit': 10000, 'enableRateLimit': True})

    cerebro.adddata(data_ticks_btc, name=market+"_BTC/USD")

    data_ticks_eth = bt.feeds.CCXT(exchange=market, symbol="XMR/USD", name=market+"_ETH/USD",
           timeframe=bt.TimeFrame.Minutes, fromdate=hist_start_date, compression=compression, config={'rateLimit': 10000, 'enableRateLimit': True})

    cerebro.adddata(data_ticks_eth, name=market+"_ETH/USD")
    """
    cerebro.addstrategy(IchimokuStrategyB)

    cerebro.run()
