import yfinance as yf
from collections import defaultdict
import numpy as np
import pandas as pd

from highcharts_stock.chart import Chart
from highcharts_stock.global_options.shared_options import SharedStockOptions
from highcharts_stock.options import HighchartsStockOptions
from highcharts_stock.options.plot_options.bar import BarOptions
from highcharts_stock.options.series.bar import BarSeries





class Distance_method():
    
    closing_prices  = {}
    spread          = None
    rolling_mean    = None
    rolling_std     = None
    upper_line      = None
    lower_line      = None
    profits_daily   = []
    profits_cash   = []
    trading_signal  = {}
    stock1_trade = {} 
    stock2_trade = {}
    series_package  = {}

    def __init__(self, stock1:str, stock2:str, start_date:str, end_date:str, window_size:int, n_std:int, figure_path:str = None) -> None:
        self._stock1 = stock1
        self._stock2 = stock2
        self._start_date = start_date
        self._end_date = end_date
        self._window_size = window_size
        self._n_time = n_std
        self._figure_path = figure_path

        self._stack1_data = None
        self._stack2_data = None
        self._stocks_data = None
        self._profits     = None

        self.base        = {stock1:500, stock2:500}
        self.total       = self.base[stock1] + self.base[stock2]
    
    def _strategy(self):
        ###
        # These operations are all based on stock_1, operation on stock_2 is opposite
        ###
        self.profits_cash = []
        self.profits_daily = []
        threshold = 1/100
        upper_line = True
        open_status = None

        stock1_long_series  = pd.Series(index = self.rolling_mean.index)
        stock1_short_series = pd.Series(index = self.rolling_mean.index)
        
        stock1_buy, stock1_sel = 0, 0
        stock2_buy, stock2_sel = 0, 0
        for idx, (date, rmean) in enumerate(self.rolling_mean.items()):
            upper = self.upper_line[date]
            lower = self.lower_line[date]
            if len(self.rolling_mean.keys()) > idx + 1:
                next_day = self.rolling_mean.keys()[idx + 1]
                stock1_price = self._stock1_data['Close'][next_day]
                stock2_price = self._stock2_data['Close'][next_day]
            
            if not (np.isnan(rmean) or np.isnan(lower) or np.isnan(upper)):
                if not open_status:
                    if (self.spread[date] - upper) >= 0:
                        open_status = True               
                        upper_line = True    
                        self.stock1_trade[next_day.strftime('%Y-%m-%d')]={ 
                                        'price':self._stock1_data['Close'][next_day], 
                                        'op':'sell', 
                                        'status':'open'}
                        self.stock2_trade[next_day.strftime('%Y-%m-%d')]={ 
                                        'price':self._stock2_data['Close'][next_day], 
                                        'op': 'buy', 
                                        'status':'open'}
                        stock1_short_series[date] = upper
                        stock1_sel = stock1_price
                        stock2_buy = stock2_price
                    elif not open_status and (self.spread[date] - lower) <= 0:
                        open_status = True
                        upper_line = False 
                        self.stock1_trade[next_day.strftime('%Y-%m-%d')]={
                                        'price' :self._stock1_data['Close'][next_day], 
                                        'op'    :'buy', 
                                        'status':'open'}
                        self.stock2_trade[next_day.strftime('%Y-%m-%d')]={
                                        'price' :self._stock2_data['Close'][next_day], 
                                        'op'    :'sell', 
                                        'status':'open'}
                        stock1_long_series[date] = lower
                        stock1_buy = stock1_price
                        stock2_sel = stock2_price
                    self.profits_cash.append(self.profits_cash[-1])
                    self.profits_daily.append(self.profits_daily[-1])
                elif open_status:
                    if upper_line and self.spread[date] - rmean <= 0:
                        open_status = False
                        self.stock1_trade[next_day.strftime('%Y-%m-%d')]={
                                         'price' :self._stock1_data['Close'][next_day], 
                                         'op'    :'buy', 
                                         'status':'close'}
                        self.stock2_trade[next_day.strftime('%Y-%m-%d')]={
                                        'price' :self._stock2_data['Close'][next_day], 
                                        'op'    :'sell', 
                                        'status':'close'}
                        stock1_long_series[date] = rmean
                        profits  = self._cal_profit_loss(stock1_price, stock1_sel,   self._stock1, long = False)
                        profits += self._cal_profit_loss(stock2_buy,   stock2_price, self._stock2, long = True)
                        self.profits_cash.append(self.profits_cash[-1] + profits/self.total)
                        self.profits_daily.append(self.profits_cash[-1])
                    elif not upper_line and self.spread[date] - rmean >= 0:
                        open_status = False
                        self.stock1_trade[next_day.strftime('%Y-%m-%d')]={ 
                                        'price' :self._stock1_data['Close'][next_day], 
                                        'op'    :'sell', 
                                        'status':'close'}
                        self.stock2_trade[next_day.strftime('%Y-%m-%d')]={
                                         'price' :self._stock2_data['Close'][next_day], 
                                         'op'    :'buy', 
                                         'status':'close'}
                        stock1_short_series[date] = rmean
                        profits  = self._cal_profit_loss(stock1_buy,   stock1_price, self._stock1, long = True)
                        profits += self._cal_profit_loss(stock2_price, stock2_sel,   self._stock2, long = False)
                        self.profits_cash.append(self.profits_cash[-1] + profits/self.total)
                        self.profits_daily.append(self.profits_cash[-1])
                    else:
                        if upper_line:
                            profits  = self._cal_profit_loss(stock1_price, stock1_sel,   self._stock1, long = False)
                            profits += self._cal_profit_loss(stock2_buy,   stock2_price, self._stock2, long = True)
                        else:
                            profits  = self._cal_profit_loss(stock1_buy,   stock1_price, self._stock1, long = True)
                            profits += self._cal_profit_loss(stock2_price, stock2_sel,   self._stock2, long = False)
                        self.profits_cash.append(self.profits_cash[-1])
                        self.profits_daily.append(self.profits_cash[-1] + profits/self.total)
                else:
                    self.profits_cash.append(self.profits_cash[-1])
                    self.profits_daily.append(self.profits_daily[-1])

            else:  
                self.profits_cash.append(0.0)
                self.profits_daily.append(0.0)      
        
        
        self.trading_signal = {'long':stock1_long_series, 'short':stock1_short_series}
        
    def _cal_profit_loss(self, buy, sell, stock_name, long):
        if long:
            return self.base[stock_name]/buy * (sell- buy)
        else:
            return self.base[stock_name]/sell * (sell - buy)
              
    def _load_data(self):
        self._stock1_data = yf.download(self._stock1 , self._start_date, self._end_date)
        self._stock2_data = yf.download(self._stock2 , self._start_date, self._end_date)
        #self._stocks_data = yf.download(self._stock1  + ' ' +  self._stock2, self._start_date, self._end_date)
        
    def _plot_original_price(self):
        #chart1 = Chart.from_pandas(self._stock1_data, {'x':'Date', 'y':'Close'})
        #chart2 = Chart.from_pandas(self._stock2_data, {'x':'Date', 'y':'Close'})
        #chart1.display()
        #chart2.display()

        dates = self._stock1_data.index.strftime('%Y-%m-%d').tolist()
        chart12 = Chart(options = {
            'chart': {
                'type': 'line'
            },
            'title': {
                'text': f'Stock Price'
            },
            'xAxis': {
                'categories': dates
            },
            'yAxis': {
                'title': {
                    'text': 'Stock Price (USD)'
                }
            },
            'series': [{
                'name': self._stock1,
                'data': self._stock1_data['Close'].tolist()
                },
                {
                'name': self._stock2,
                'data': self._stock2_data['Close'].tolist()
                }
              
            ]
        })
        chart12.display()
        
    def _plot_all_result(self):
        self._plot_original_price()
        self._plot_bollinger_band()
        pass

    def _plot_bollinger_band(self):
        dates = self._stock1_data.index.strftime('%Y-%m-%d').tolist()
        chart = Chart(options = {
            'chart': {
                'type': 'line'
            },
            'title': {
                'text': f'Stock Price'
            },
            'xAxis': {
                'categories': dates,
                'type': 'datetime',
            },
            'yAxis': {
                'title': {
                    'text': 'Stock Price (USD)'
                }
            },
            'series': [
                {
                'name': 'spread',
                'data': self.spread.tolist()
                },
                {
                'name': 'upper_line',
                'data': self.upper_line.tolist()
                },
                {
                'name': 'rolling_mean',
                'data': self.rolling_mean.tolist()
                },
                {
                'name': 'lower_line',
                'data': self.lower_line.tolist()
                },
                

            ], 
            'rangeSelector': {
                'selected': 1
            },
        })
        chart.add_series({
            'type': 'scatter',
            'data': self.trading_signal['short'].tolist(),
            'name': 'Short',
            'marker': {
                'name': "sell",
                'symbol': 'triangle-down',
                'fillColor': 'red',
                'lineColor': 'red',
                'lineWidth': 2,
                'enabled': True,
                'radius': 6,
            },
            'visible': True,
        })
        chart.add_series({
            'type': 'scatter',
            'data': self.trading_signal['long'].tolist(),
            'name': 'Long',
            'marker': {
                'name': "buy",
                'symbol': 'triangle',
                'fillColor': 'green',
                'lineColor': 'green',
                'lineWidth': 2,
                'enabled': True,
                'radius': 6,
            },
            'visible': True,
        })
        chart.display()

    def nan2none(self, target):
        package = {}
        for key, elem_pd in target.items():
            if type(elem_pd) is pd.Series:
                package[key] = elem_pd.replace(float('nan'), None)
            else:
                package[key] = elem_pd
        return package
    
    def pd2list(self, target):
        package = {}
        for key, elem_pd in target.items():
            if type(elem_pd) is not list and type(elem_pd) is not dict:
                package[key] = elem_pd.tolist()
            else:
                package[key] = elem_pd
        return package

    def run(self, plot_en = False):
        self.reset_attributes()
        self._load_data()
        
        self.closing_prices[self._stock1] = self._stock1_data['Close']
        self.closing_prices[self._stock2] = self._stock2_data['Close']
        self.spread                       = np.log10(self.closing_prices[self._stock1]) - np.log10(self.closing_prices[self._stock2])
        self.rolling_mean                = self.spread.rolling(self._window_size).mean()
        self.rolling_std                 = self.spread.rolling(self._window_size).std()
        self.upper_line                  = self.rolling_mean + self._n_time * self.rolling_std
        self.lower_line                  = self.rolling_mean - self._n_time * self.rolling_std

        self._strategy()
        
        if plot_en:
            self._plot_all_result()

        series_package = {
            'dates'         : self._stock1_data.index.strftime('%Y-%m-%d'),
            'stock1'        : self.closing_prices[self._stock1],
            'stock2'        : self.closing_prices[self._stock2],
            'spread'        : self.spread,
            'rolling_mean'  : self.rolling_mean,
            'rolling_std'   : self.rolling_std,
            'upper_line'    : self.upper_line,
            'lower_line'    : self.lower_line,
            'long'          : self.trading_signal['long'],
            'short'         : self.trading_signal['short'],
            'profits_cash'  : self.profits_cash,
            'profits_daily' : self.profits_daily,
            'stock1_trade':self.stock1_trade,
            'stock2_trade':self.stock2_trade,
        }
        return series_package

    def reset_attributes(self):
        self.closing_prices  = {}
        self.spread          = None
        self.rolling_mean    = None
        self.rolling_std     = None
        self.upper_line      = None
        self.lower_line      = None
        self.profits_daily   = []
        self.profits_cash   = []
        self.trading_signal  = {}
        self.stock1_trade = {} 
        self.stock2_trade = {}
        self.series_package  = {}
    
if __name__ == "__main__":
    stock_obj = Distance_method("AAPL", "GLD", "2021-01-01", "2024-01-01", 200, 2)
    stock_obj.run()
    