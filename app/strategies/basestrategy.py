# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import time
from datetime import datetime, timedelta
import backtrader as bt
import numpy
import telebot
import os


class BaseStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_operator(self, msg):
        TOKEN =  os.environ['TG_TOKEN'] 
        CHANNEL_ID = int(os.environ['TG_CHANNEL_ID'])

        tb = telebot.TeleBot(TOKEN)

        tb.send_message(CHANNEL_ID, msg)

    def notify_order(self, order):
        if order.status == order.Completed:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('OPERATION PROFIT, GROSS {}, NET {}'.format(trade.pnl, trade.pnlcomm))
