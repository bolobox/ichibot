# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import time
from datetime import datetime, timedelta
import backtrader as bt
from strategies import BaseStrategy
import ccxt

class IchimokuStrategyB(BaseStrategy):
    params = dict(warmup=52)

    def start(self):
        self.log('Started', datetime.utcnow())

    def prenext(self):
        self.log("prenext", datetime.utcnow())


    def __init__(self):
        self.inds = dict()
        for i, d in enumerate(self.datas):
            self.inds[d] = dict()
            self.inds[d]['ichimoku'] = bt.indicators.Ichimoku(d, plot=True)


    def next(self):
        self.log("next called", datetime.utcnow())
        for i, d in enumerate(self.datas):
            name = d._name
            data0 = d
            ichimoku = self.inds[d]['ichimoku']
            if len(data0.close)>1 and len(ichimoku.senkou_span_a) > 1 and len(ichimoku.senkou_span_b) > 1 :
                if (data0.close[0] > max([ichimoku.senkou_span_a[0], ichimoku.senkou_span_b[0]])
                    and data0.close[-1] < max([ichimoku.senkou_span_a[-1], ichimoku.senkou_span_b[-1]])):
                    msg = "*Buy* signal on %s" % (name)
                    self.log(msg)
                    self.notify_operator(msg)
                    self.log('------ %s PRICE %.6f - timestamp %s' % (name, data0.close[0], bt.num2date(data0.datetime[0]).isoformat()), datetime.utcnow())

                if (data0.close[0] < min([ichimoku.senkou_span_a[0], ichimoku.senkou_span_b[0]])
                    and data0.close[-1] > min([ichimoku.senkou_span_a[-1], ichimoku.senkou_span_b[-1]])):
                    msg = "*Sell* signal on %s" % (name)
                    self.log(msg)
                    self.notify_operator(msg)
                    self.log('------ %s PRICE %.6f - timestamp %s' % (name, data0.close[0], bt.num2date(data0.datetime[0]).isoformat()), datetime.utcnow())
