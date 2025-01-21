import yfinance as yf
from datetime import datetime, timedelta
import requests
import pandas as pd
from bs4 import BeautifulSoup
import io
import talib
import math
import numpy as np
import backtrader as bt
import base64
import io
# 創建一個 RSI 策略類別
class RsiStrategy(bt.Strategy):
    params = (
        ("rsi_period", 14),  # RSI 指標的週期
        ("overbought", 70),  # 超買區間
        ("oversold", 30),    # 超賣區間
    )

    def __init__(self):
        # 初始化 RSI 指標
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)

    def next(self):
        # 檢查是否已有部位
        if self.position:
            # 如果 RSI 超過超買水平，賣出
            if self.rsi > self.params.overbought:
                self.close()

        else:
            # 如果 RSI 低於超賣水平，買入
            if self.rsi < self.params.oversold:
                self.buy()

# 創建一個 SMA 策略類別
class SmaCrossStrategy(bt.Strategy):
    params = (
        ("fast_period", 10),  # 快速均線週期
        ("slow_period", 30),  # 慢速均線週期
    )

    def __init__(self):
        # 初始化均線指標
        self.fast_sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.fast_period)
        self.slow_sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.slow_period)

    def next(self):
        # 檢查是否已有部位
        if self.position:
            # 如果快速均線跌破慢速均線，賣出所有部位
            if self.fast_sma < self.slow_sma:
                self.close()

        else:
            # 如果快速均線突破慢速均線，買入
            if self.fast_sma > self.slow_sma:
                self.buy()

# 通用回測函數
def run_backtest(strategy_class, strategy_params, ticker, start_date, end_date, cash):
    def figure_to_base64(fig):
        """將 Matplotlib 圖像轉換為 Base64 編碼字串"""
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        base64_str = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        return base64_str
    import matplotlib
    matplotlib.use('Agg')  # 使用非互動後端，避免 GUI 啟動

    # 創建 Backtrader 引擎
    cerebro = bt.Cerebro()

    # 使用 yfinance 下載數據
    df = yf.download(ticker, start=start_date, end=end_date)

    # 將數據轉換為 Backtrader 格式
    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data)

    # 加入策略
    cerebro.addstrategy(strategy_class, **strategy_params)

    # 設定初始現金
    cerebro.broker.setcash(cash)

    # 準備保存圖像的緩存
    # img_buf = io.BytesIO()

    # 執行回測並繪製結果
    cerebro.run()

    # 禁止使用 show，直接保存圖像
    fig = cerebro.plot()[0][0]  # 獲取圖形

    
    fig.savefig('./output.png')  # 保存至內存緩存
    print('cerebro.broker.getvalue(),')
    print(cerebro.broker.getvalue(),)
    return {
        "initial_cash": cash,
        "final_cash": cerebro.broker.getvalue(),
        "plot_image": figure_to_base64(fig)
    }


class HistoryStockInfo():
    '''
    fetch the history stock information from goodinfo.tw
    stock_ticker: The stock ticker of the stock.
    start_date: The start date of the calculation.
    end_date: The end date of the calculation.
    set_confg: Set the configuration of the request.
        headers: The headers of the request.
        params: The parameters of the request.
        url: The url of the request.
    fetch_history_sheet: Fetch the history sheet of the stock.
        return: The history sheet of the stock.
    '''
    def __init__(self, stock_ticker:str, start_date:str, end_date:str) -> None:
        self._stock_ticker = stock_ticker[0:-3]
        self._start_date = start_date
        self._end_date = end_date
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            #'Cookie': 'CLIENT%5FID=20250102011324032%5F140%2E116%2E20%2E180; IS_TOUCH_DEVICE=F; SCREEN_SIZE=WIDTH=2560&HEIGHT=1440; _ga=GA1.1.1506703594.1735751607; _cc_id=e8f043dc8ff3fe9fe6cb8a6178fdf8d6; panoramaId_expiry=1736356406980; panoramaId=af235bb25110a2cf158fb874fac316d53938fdd832b0dab732a7c4fa2ee70efe; panoramaIdType=panoIndiv; TW_STOCK_BROWSE_LIST=2330%7C1303; cto_bundle=zyPWMV9WdzY5Qkc5T3QyNXdhaTBNdTlwRzdtZnMwZyUyRkhUOUZ6bVQlMkZQYTlxciUyQmJwZ05oNGxhWXlMUEo4ZDl6WkphTk15NXJxODFPbm9uJTJCaDRZQ1lKOUMlMkJWaU5icG03bFQxVmpQZkc5OTZldksxMmpEeEhtMGhLJTJCSWpyOUV3UExBOHIwTmNvd1dFd1JwOGk1N1RVejVNVklZVmtBdmYxbjlrbSUyQlZIT2RuQUYlMkYlMkZDMU8lMkZHWjJsTkFsbkVsVTM2OTlER1VwYmZuN2xDaVNwMEhUMjdLWW15MGprd2RmQzdjeVlkWG1vZ3hlekpwYkcySGpWUFJiSFNhTllobiUyRlJiaDEwMU54cnJ0eUZDUkZXbERuUFBPRUQlMkJ2eGVhZVNtNzZJZlVGM0FUVXY5JTJCaDRaQk8xSDlDZyUyRmM0WldyZmkxSzk4bEFNJTJGNQ; cto_bidid=5wU7A182RDBlZTFrWnh2UXRoTmlWVVlJR1FOM25NSFdQVDFWb0htdkYwY3FnRThXVHJyQ1p2MFhidzUzSVhwNVlOSnBWalBQTXVNYjRVeEclMkY1WlBnMFkxaDFXU2J2cjdDQ1Voc1pINW9NdmxNdHF3JTNE; FCNEC=%5B%5B%22AKsRol-ovw94-KaNEDUV-gL9wmTlnzTF33TQmpB4ldrIOgDdpnFe3C01yP9TFR1ytDo1RlKIHmC6ll4IFhgnvd-yzCPqfRNkFMRIJUgZ1Oyb-xrcecXeVFoeGAJDYAmNt0BGvE2ywKZ4sc7KdkI4W4xrD0VqS0Falw%3D%3D%22%5D%5D; __gads=ID=33431fb4f4a17e93:T=1735751607:RT=1736175838:S=ALNI_MZtWrVElolVIFSs7-UAwrjR3fWM5Q; __gpi=UID=00000fcf8e1cf468:T=1735751607:RT=1736175838:S=ALNI_MZjhazlBGLHLqJwUEHFPqMSPaXVjw; __eoi=ID=ee2c7f7ab64dd559:T=1735751607:RT=1736175838:S=AA-AfjazLHTzMaY5fZ_ZGIgsphod; _ga_0LP5MLQS7E=GS1.1.1736175837.4.0.1736175840.57.0.0; cto_bundle=tT-VPF9WdzY5Qkc5T3QyNXdhaTBNdTlwRzd1TDhOMWZqT0x1Z3JTN0twWXFKOU5iQ3k1Y0FLRjJ1SjZMQnE0VUg3dHh2c1ljclhuV1BXdDFtcnJNRnhvYTFhZGd2QWNnSSUyRjJBUmZGZ0VZdEFaRDNUV2drS1pVa2U1bVdZZWtaWFppTiUyRnpzYzZtblZsdHpYSVNaSnJoMmhyVmw2R0FLRDBIcHVCJTJCblNxZDE4bk9CY2Y1Rkx3dG5RdjZkUjBrV1VkS0hKRk1VWlN0VEhmbjZFUzBGTXA0JTJGTU9wQzUyUnlDMTZkQ25qdSUyRk9SWGFOdGtHdEpXQ2klMkJkQUZLWjVodCUyQkxKM004a21HNVIlMkZwczRGSnB5RFhYanolMkI1bE1TNVNaQ1lRMWpoamxnYXpVRnk3S2dIekZKN1JMbzglMkIwVWN1NldraEk5TTVU',
            'Cookie':  'CLIENT%5FID=20250102011324032%5F140%2E116%2E20%2E180; IS_TOUCH_DEVICE=F; SCREEN_SIZE=WIDTH=2560&HEIGHT=1440; _ga=GA1.1.1506703594.1735751607; _cc_id=e8f043dc8ff3fe9fe6cb8a6178fdf8d6; panoramaId_expiry=1737095901500; panoramaId=af235bb25110a2cf158fb874fac316d53938fdd832b0dab732a7c4fa2ee70efe; panoramaIdType=panoIndiv; TW_STOCK_BROWSE_LIST=1303%7C2330; cto_bidid=u_nnE182RDBlZTFrWnh2UXRoTmlWVVlJR1FOM25NSFdQVDFWb0htdkYwY3FnRThXVHJyQ1p2MFhidzUzSVhwNVlOSnBWalBQTXVNYjRVeEclMkY1WlBnMFkxaDFVRTBCR2xDWjZuUVE3a2lVb1BuNFlBJTNE; cto_bundle=hw1g0V9WdzY5Qkc5T3QyNXdhaTBNdTlwRzd1M1loMVcwWUJmVnk5aWJ1Rk9obGlLcVJWOHN4ZzNVSFA2M2JzQzlRa2ZFc1BFb0pFUGk2RGZ3clp3ZXV3enpSaEF0S0NnN1JVMU0lMkZQJTJCUWljTjQzaFJjMFBXMHRUajA3QzFINXNhWGZudnRRWDZvRGdvVzQyZzNZODNxODhrZHliMjE3YXRwdWM4dW45Z2hDVzN0cHlDOFVMUnpZZEJaUVNQeno5Ukk3WGdKJTJCdW9RSVhRTFIyWVRwMEs4aWZIOUZkd1FVeVA0S2gyOGtSMzk1JTJGNnB6S202ZVJ5QmNBT2hsRVFwcTdsaFVMbm5nZTM1SEZ2SzYwdEJIWUZJM3hoQjJ0b3pLTkV3Q1ZDNnFmeFFZU0pJOUNnOFhScWFyMzdlblhka2t4ZkNRMGho; FCNEC=%5B%5B%22AKsRol-xra8nEe2ivTsOdBC69PYNoj_YozcuBghjC_s7XZuT-3F7bWDxswGbINkc8GTPlyovvx_gVjc52WdPUySgYE5160pnZ-6wHs-_gsQDlkT_DIoj2Xd65W7kullkEd9EcdTz5EITSNUQVZOAHUXIlvKsViXIuw%3D%3D%22%5D%5D; __gads=ID=33431fb4f4a17e93:T=1735751607:RT=1736695515:S=ALNI_MZtWrVElolVIFSs7-UAwrjR3fWM5Q; __gpi=UID=00000fcf8e1cf468:T=1735751607:RT=1736695515:S=ALNI_MZjhazlBGLHLqJwUEHFPqMSPaXVjw; __eoi=ID=ee2c7f7ab64dd559:T=1735751607:RT=1736695515:S=AA-AfjazLHTzMaY5fZ_ZGIgsphod; _ga_0LP5MLQS7E=GS1.1.1736695513.10.1.1736695516.57.0.0; cto_bundle=-2HAO19WdzY5Qkc5T3QyNXdhaTBNdTlwRzdyOUE3cFVvMlZQUXlxMGNPR2pIYUh6SjJ6bWZramFzcXlWRlliY3llSmVCaURvYUlsYWZlSWpUQ2JQS00weWkzaXJQaHdMVWRqVmZoeEQlMkJ6cjRWNmtqdkhjd3hjMHF5S3BRZ2tBa25WSkFNJTJCejAwT2c1S1lDMHVMUmo4T3FwREc0MWZ2YThicnYlMkZTUENNTzRpNE5OakloODMwOGoyNDV6OVdDciUyQnQ5RUFRbWs5V0haUU1lTTBKejZFT1Y1WlBFNm8zQ1RJTUk2eUozRGlzWm94c0NQaHRGejFJSlVLaUcwMFZzdmxJeUdpUXhYTU9wJTJCZHQlMkZhVWklMkJZRjElMkJJWXRkRzdIcmlRUm1VTWZaR2VrUEk4MDgyY3FRNFN6M3l1cXN4NXBSdXJlRUN2TTc'
        }
        self._params = {
            'STOCK_ID': self._stock_ticker,
            'SHEET':'PER/PBR',
        }
        self._url = 'https://goodinfo.tw/tw/StockBzPerformance.asp'

    def set_confg(self, headers:dict = None, params:dict = None, url:str = None):
        if type(headers) is dict:
            self._headers = headers
        if type(params) is dict:
            self._params = params
        if type(url) is str:
            self._url = url
    def fetch_history_sheet(self):
        res = requests.get(self._url, headers=self._headers, params=self._params)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        data = soup.select_one('#txtFinDetailData')
        html_data = io.StringIO(data.prettify())
        dfs = pd.read_html(html_data)
        dfs[0].set_index(dfs[0]['年度']['年度'], inplace=True)
        return dfs[0]
    def fetch_history_river_sheet(self):
        res = requests.get(self._url, headers=self._headers, params=self._params)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        data = soup.select_one('#divDetail')
        html_data = io.StringIO(data.prettify())
        dfs = pd.read_html(html_data)
        no_need = dfs[0].keys()[0][0]
        
        dfs[0] = dfs[0][~dfs[0].isin([no_need]).any(axis=1)]
        #print(dfs[0][no_need][no_need])
        dfs[0].index = list(dfs[0][no_need][no_need])
        return dfs[0]

class DividendPriceMethod():
    '''
    This class is used to calculate the classification of the stock price based on the dividend.
    stock_ticker: The stock ticker of the stock.
    start_date: The start date of the calculation.
    end_date: The end date of the calculation.
    fetch_dividend_and_price: Fetch the dividend and the current price of the stock.
        return: The average dividend and the current price of the stock.
        {"average_dividend": avg_dividend, "current_price": current_price}
    calculate_price_classification: Calculate the classification of the stock price based on the dividend.
        time_gate: The time gate of the classification. Default is [15, 20, 30].
        cheap: The price is less than the dividend * time_gate[0].
        reasonable: The price is less than the dividend * time_gate[1].
        expensive: The price is less than the dividend * time_gate[2].
        extremely expensive: The price is more than the dividend * time_gate[2].
    '''

    def __init__(self, stock_ticker:str, start_date:str, end_date:str) -> None:
        self._stock_ticker = stock_ticker
        self._start_date = start_date
        self._end_date = end_date

    def fetch_dividend_and_price(self):
        stock = yf.Ticker(self._stock_ticker)

        # Fetch the dividend
        dividends = stock.dividends[self._start_date:self._end_date]
        if dividends.empty:
            return {"error": f"Cannot fetch the dividend of {self._stock_ticker}."}

        total_dividend = dividends.sum()
        num_years = (datetime.strptime(self._end_date, "%Y-%m-%d") - datetime.strptime(self._start_date, "%Y-%m-%d")).days / 365.25
        avg_dividend = total_dividend / num_years

        
        stock_info = stock.history(period="1d")
        if stock_info.empty:
            return {"error": f"Cannot fetch the current price of {self._stock_ticker}."}
        # Fetch the current price
        current_price = stock_info['Close'].iloc[-1]

        return {"average_dividend": avg_dividend, "current_price": current_price}

    def calculate_price_classification(self, time_gate:list = [15, 20, 30]):
        data = self.fetch_dividend_and_price()
        if "error" in data:
            return data

        avg_dividend = data["average_dividend"]
        current_price = data["current_price"]

        price_15_years = avg_dividend * time_gate[0]
        price_20_years = avg_dividend * time_gate[1]
        price_30_years = avg_dividend * time_gate[2]

        if current_price < price_15_years:
            print("current {} < price_15_years {}".format(current_price, price_15_years))   
            classification = "cheap"
        elif current_price <= price_20_years:
            print("current {} <= price_20_years {}".format(current_price, price_20_years))
            classification = "reasonable"
        elif current_price <= price_30_years:
            print("current {} <= price_30_years {}".format(current_price, price_30_years))
            classification = "expensive"
        else:
            print("current {} > price_30_years {}".format(current_price, price_30_years))
            classification = "extremely expensive"

        return classification

class HighLowPriceMethod():
    '''
    This class is used to calculate the classification of the stock price based on the high and low price.
    fetch_high_low_price: Fetch the high and low price of the stock.
        return: The current price and the average high, low, and price of the stock.
        {"current_price": current_price, "low_price": AvgLowPrice, "avg_price": AvgPrice, "high_price": AvgHighPrice}
    calculate_price_classification: Calculate the classification of the stock price based on the high and low price.
        cheap: The current prcie is Less than the Low average price.
        reasonable: The current price is Less than the average price.
        expensive: The current price is Less than the High average price.
        extremely expensive: The current price is more than the High average price.
    '''
    def __init__(self, stock_ticker:str, start_date:str, end_date:str) -> None:
        self._stock_ticker = stock_ticker
        self._start_date = start_date
        self._end_date = end_date
    
    def fetch_high_low_price(self):
        def history_table(stock_ticker:str, start_date:str, end_date:str):
            stock = yf.Ticker(stock_ticker)
            for id in range((datetime.strptime(end_date, "%Y-%m-%d").year-datetime.strptime(start_date, "%Y-%m-%d").year)+1):
                if id == 0:
                    start=datetime.strptime(start_date, "%Y-%m-%d")
                else:
                    start="{}-{}-{}".format(start.year+1, 1, 1)
                    start=datetime.strptime(start, "%Y-%m-%d")
                
                end=start+timedelta(days=364)
                if end > datetime.strptime(end_date, "%Y-%m-%d"):
                    end = datetime.strptime(end_date, "%Y-%m-%d")
                stock_info = stock.history(start=start, end=end)
                #print(id, start, end)
                #print((end-start),stock_info['High'].mean())
                result = {"year":start.year, 
                          "avg_high_price":stock_info['High'].mean(),              
                          "avg_low_price":stock_info['Low'].mean(), 
                          "avg_price":(stock_info['High'].mean()
                                                    +
                                       stock_info['Low'].mean()) / 2}
                #print(result)
                yield result
                #yield stock_info
        
        stock = yf.Ticker(self._stock_ticker)
        stock_info = stock.history(start=self._start_date, end=self._end_date)

        if stock_info.empty:
            return {"error": f"Cannot fetch the price of {self._stock_ticker}."}

        history_avg_price = history_table(self._stock_ticker, self._start_date, self._end_date)
        # Fetch the current price
        current_price = stock.history(period="1d")['Close'].iloc[-1]
        history_high_min_avg = {idx:i for idx, i in enumerate(history_avg_price)}
        length = len(history_high_min_avg)
        AvgLowPrice = sum([i['avg_low_price'] for i in history_high_min_avg.values()])/length
        AvgPrice = sum([i['avg_price'] for i in history_high_min_avg.values()])/length
        AvgHighPrice = sum([i['avg_high_price'] for i in history_high_min_avg.values()])/length
        result = {'low_price':AvgLowPrice, 'avg_price':AvgPrice, 'high_price':AvgHighPrice}
        return current_price, result

    def calculate_price_classification(self):
        '''
        cheap: The current prcie is Less than the Low average price.
        reasonable: The current price is Less than the average price.
        expensive: The current price is Less than the High average price.
        extremely expensive: The current price is more than the High average price.
        '''
        current_price, result = self.fetch_high_low_price()
        if "error" in result:
            return result

        #print(AvgLowPrice, AvgPrice, AvgHighPrice)
        if current_price < result['low_price']:
            print("current {} < AvgLowPrice {}".format(current_price, result['low_price']))
            classification = "cheap"
        elif current_price <= result['avg_price']:
            print("current {} <= AvgPrice {}".format(current_price, result['avg_price']))
            classification = "reasonable"
        elif current_price <= result['high_price']:
            print("current {} <= AvgHighPrice {}".format(current_price, result['high_price']))
            classification = "expensive"
        else:
            print("current {} > AvgHighPrice {}".format(current_price, result['high_price']))   
            classification = "extremely expensive"
        return classification

class PBMethod():
    '''
    This class is used to calculate the classification of the stock price based on the PB.
    fetch_PB: Fetch the PB of the stock.
        return: The current price and the average high, low, and price of the stock.
        current_price, max_min_avg_pb_price = {'lowest_pb_price': 0, 'highest_pb_price': 0, 'avg_pb_price': 0}
    calculate_price_classification: Calculate the classification of the stock price based on the PB.

    '''
    def __init__(self, stock_ticker:str, start_date:str, end_date:str) -> None:
        self._stock_ticker = stock_ticker
        self._start_date = start_date
        self._end_date = end_date

    def fetch_PB(self):
        def history_max_min_avg_pb(history_stock_info, start_date, end_date):
            lowest_pb = []
            highest_pb = []
            avg_pb = []
            years = range(datetime.strptime(start_date, "%Y-%m-%d").year, datetime.strptime(end_date, "%Y-%m-%d").year+1)
            length = len(years)
            for y in years:
                y = '24Q3' if y == 2024 else y
                lowest_pb.append(float(history_stock_info['本淨比(PBR)統計']['最低  PBR'][f'{y}']))
                highest_pb.append(float(history_stock_info['本淨比(PBR)統計']['最高  PBR'][f'{y}']))
                avg_pb.append(float(history_stock_info['本淨比(PBR)統計']['平均  PBR'][f'{y}']))
            return {"lowest_pb":sum(lowest_pb)/length, "highest_pb":sum(highest_pb)/length, "avg_pb":sum(avg_pb)/length}
        history_stock_info = HistoryStockInfo(self._stock_ticker, self._start_date, self._end_date)
        
        stock = yf.Ticker(self._stock_ticker)
        
        # Fetch the current price
        current_price = stock.history(period="1d")['Close'].iloc[-1]
        bookvalue = stock.info['bookValue']
        
        # Fetch pbr, high, low, avg
        sheet = history_stock_info.fetch_history_sheet()
        max_min_avg_pb = history_max_min_avg_pb(sheet, self._start_date, self._end_date)
        max_min_avg_pb_price = {k+'_price':v*bookvalue for k, v in max_min_avg_pb.items()}
        return current_price, max_min_avg_pb_price

    def calculate_price_classification(self):
        '''
        cheap: The current prcie is Less than the Book Value.
        reasonable: The current price is Less than the Book Value * 1.5.
        expensive: The current price is Less than the Book Value * 2.
        extremely expensive: The current price is more than the Book Value * 2.
        '''
        current_price, current_PB_price = self.fetch_PB()
        if "error" in current_PB_price:
            return current_PB_price

        if current_price < current_PB_price["lowest_pb_price"]:
            print("current {} < {}".format(current_price, current_PB_price["lowest_pb_price"]))
            classification = "cheap"
        elif current_price <= current_PB_price["avg_pb_price"]:
            print("current {} <= {}".format(current_price, current_PB_price["avg_pb_price"]))
            classification = "reasonable"
        elif current_price <= current_PB_price["highest_pb_price"]:
            print("current {} <= {}".format(current_price, current_PB_price["highest_pb_price"]))
            classification = "expensive"
        else:
            print("current {} > {}".format(current_price, current_PB_price["highest_pb_price"]))
            classification = "extremely expensive"
        return classification

class PEMethod():
    '''
    This class is used to calculate the classification of the stock price based on the PE.
    fetch_PE: Fetch the PE of the stock.
        return: The current price and the average high, low, and price of the stock.
        current_price, max_min_avg_pe_price = {'lowest_pe_price': 0, 'highest_pe_price': 0, 'avg_pe_price': 0}
    '''
    def __init__(self, stock_ticker:str, start_date:str, end_date:str) -> None:
        self._stock_ticker = stock_ticker
        self._start_date = start_date
        self._end_date = end_date
    
    def fetch_PE(self):
        def history_max_min_avg_pe(history_stock_info, start_date, end_date):
            lowest_pe = []
            highest_pe = []
            avg_pe = []
            years = range(datetime.strptime(start_date, "%Y-%m-%d").year, datetime.strptime(end_date, "%Y-%m-%d").year+1)
            length = len(years)
            for y in years:
                y = '24Q3' if y == 2024 else y
                lowest_pe.append(float(history_stock_info['本益比(PER)統計']['最低  PER'][f'{y}']))
                highest_pe.append(float(history_stock_info['本益比(PER)統計']['最高  PER'][f'{y}']))
                avg_pe.append(float(history_stock_info['本益比(PER)統計']['平均  PER'][f'{y}']))

            return {"lowest_pe":sum(lowest_pe)/length, "highest_pe":sum(highest_pe)/length, "avg_pe":sum(avg_pe)/length}
        def history_avg_final_eps(history_stock_info, start_date, end_date):
            eps = []

            years = range(datetime.strptime(start_date, "%Y-%m-%d").year, datetime.strptime(end_date, "%Y-%m-%d").year+1)
            length = len(years)
            for y in years:
                y = '24Q3' if y == 2024 else y
                eps.append(float(history_stock_info['本益比(PER)統計']['EPS  (元)'][f'{y}']))

            return sum(eps)/length, eps[-1]
        history_stock_info = HistoryStockInfo(self._stock_ticker, self._start_date, self._end_date)
        
        stock = yf.Ticker(self._stock_ticker)
        
        # Fetch the current price
        current_price = stock.history(period="1d")['Close'].iloc[-1]
        
        # Fetch per, high, low, avg
        sheet = history_stock_info.fetch_history_sheet()
        max_min_avg_pe = history_max_min_avg_pe(sheet, self._start_date, self._end_date)
        avg_eps, final_eps = history_avg_final_eps(sheet, self._start_date, self._end_date)
        max_min_avg_pe_price = {k+'_price':v * (final_eps + avg_eps) / 2 for k, v in max_min_avg_pe.items()}
        return current_price, max_min_avg_pe_price

    def calculate_price_classification(self):
        '''
        cheap: The current prcie is Less than the Book Value.
        reasonable: The current price is Less than the Book Value * 1.5.
        expensive: The current price is Less than the Book Value * 2.
        extremely expensive: The current price is more than the Book Value * 2.
        '''
        current_price, current_PE_price = self.fetch_PE()
        if "error" in current_PE_price:
            return current_PE_price

        if current_price < current_PE_price["lowest_pe_price"]:
            print("current {} < {}".format(current_price, current_PE_price["lowest_pe_price"]))
            classification = "cheap"
        elif current_price <= current_PE_price["avg_pe_price"]:
            print("current {} <= {}".format(current_price, current_PE_price["avg_pe_price"]))
            classification = "reasonable"
        elif current_price <= current_PE_price["highest_pe_price"]:
            print("current {} <= {}".format(current_price, current_PE_price["highest_pe_price"]))
            classification = "expensive"
        else:
            print("current {} > {}".format(current_price, current_PE_price["highest_pe_price"]))
            classification = "extremely expensive"
        return classification

class RiverChartMethod():
    def __init__(self, stock_ticker:str, start_date:str, end_date:str, interval:str) -> None:
        self._stock_ticker = stock_ticker
        self._start_date = start_date
        self._end_date = end_date
        self._interval = interval

    def get_candle_info(self, start, end, interval):
        '''
        interval = 1d 1wk 1mo 3mo 1y
        data['Open'], data['High'], data['Low'], data['Close'], data['Volume']
        '''
        stock = yf.Ticker(self._stock_ticker)
        data = stock.history(start=start, end=end, interval=interval)
        current_price = stock.history(period="1d")['Close'].iloc[-1]
        return current_price, data
    
    def get_river_line(self, start, end, interval):
        h = HistoryStockInfo(stock_ticker=self._stock_ticker, start_date=start, end_date=end)

        if interval == '1wk':
            time_frame = 'WEEK'
        elif interval == '1mo':
            time_frame = 'MONTH'
        elif interval == '3mo':
            time_frame = 'QUAR'
        elif interval == '1y':
            time_frame = 'YEAR'
        elif interval == '1d':
            time_frame = 'DATE'
        else:
            time_frame = 'MONTH'
        h._params['CHT_CAT'] = time_frame
        h._params['RPT_CAT'] = 'PER'
        h._params['START_DT']=start
        h._params['END_DT']  =end
        h._url = 'https://goodinfo.tw/tw/ShowK_ChartFlow.asp'
        
        return h.fetch_history_river_sheet()

    def PER_river(self, start, end, interval):
        sheet = self.get_river_line(start, end, interval)
        factors = sheet['本益比換算價格'].keys()
        line_datas = []
        for idx in factors:
            buf = []
            for t in sheet.index:
                buf.append(float(sheet['本益比換算價格'][idx][t]))
            
            line_datas.append(buf[::-1])
        print('len river: ', len(line_datas[0]))
        return line_datas
    
    def fetch_river_chart_data(self):
        river_lines = self.PER_river(self._start_date, self._end_date, self._interval)
        current_price, candle_line = self.get_candle_info(self._start_date, self._end_date, self._interval)

        low_price = river_lines[0][-1]
        avg_price = (river_lines[2][-1] + river_lines[3][-1])/2
        high_price = river_lines[5][-1]
        classify_price = {'lowest_price':low_price,
                          'avg_price':avg_price,
                          'highest_price':high_price
                          }
        return current_price, classify_price, river_lines, candle_line

    def calculate_price_classification(self):
        current_price, classify_price, river_lines, candle_line = self.fetch_river_chart_data()
        if "error" in classify_price:
            return classify_price

        if current_price < classify_price["lowest_price"]:
            print("current {} < {}".format(current_price, classify_price["lowest_price"]))
            classification = "cheap"
        elif current_price <= classify_price["avg_price"]:
            print("current {} <= {}".format(current_price, classify_price["avg_price"]))
            classification = "reasonable"
        elif current_price <= classify_price["highest_price"]:
            print("current {} <= {}".format(current_price, classify_price["highest_price"]))
            classification = "expensive"
        else:
            print("current {} > {}".format(current_price, classify_price["highest_price"]))
            classification = "extremely expensive"
        return classification
    
def Res_Sup_line(stock_code, start, ma_len, ma_mode, method = 1):
    def nan2none(target):
        package = {}
        for key, elem_pd in target.items():
            if type(elem_pd) is pd.Series:
                package[key] = elem_pd.replace(float('nan'), None)
            else:
                package[key] = elem_pd
        return package
    stock_data = yf.download(stock_code, start=start)
    candle_data = {
        'date':stock_data.index.strftime('%Y-%m-%d').tolist(),
        'Open':stock_data['Open'].tolist(),
        'Close':stock_data['Close'].tolist(),
        'High':stock_data['High'].tolist(),
        'Low':stock_data['Low'].tolist(),
        'Volume':stock_data['Volume'].tolist(),
    }
    if ma_mode == 'WMA':
        ma_result = talib.WMA(stock_data['Close'], timeperiod = ma_len)
    else:
        ma_result = talib.SMA(stock_data['Close'], timeperiod = ma_len)
    ma_volume = talib.SMA(stock_data['Volume'], timeperiod = 20)
    bias = []
    neg_bias = 0
    pos_bias = 0
    res_line = []
    sup_line = []
    less_than_sup = []
    higher_than_res = []
    #print(nan2none(ma_result))
    for date, value in ma_result.items():
        if not math.isnan(value):
            bias.append((stock_data['Close'][date] - value)/value)
    pos_bias = sorted([num for num in bias if num >= 0])
    neg_bias = sorted([num for num in bias if num < 0])
    if method == 1 or method == 3:
        pos_bias = pos_bias[round(len(pos_bias)*0.95)]
        neg_bias = neg_bias[round(len(neg_bias)*0.05)]
        print('pos_bias', pos_bias)
        print('neg_bias', neg_bias)
        for date, value in ma_result.items():
            if not math.isnan(value):
                res_line.append(value * pos_bias + value)
                sup_line.append(value * neg_bias + value)
            else:
                res_line.append(None)
                sup_line.append(None)
            if res_line[-1]:
                if method == 1:
                    if (res_line[-1] < stock_data['Close'][date] and res_line[-1] < stock_data['Open'][date]): 
                        higher_than_res.append([date.strftime('%Y-%m-%d'), stock_data['Close'][date]])
                    elif (sup_line[-1] > stock_data['Close'][date] and sup_line[-1] > stock_data['Open'][date]):
                        less_than_sup.append([date.strftime('%Y-%m-%d'), stock_data['Close'][date]])
                elif not math.isnan(ma_volume[date]) and ma_volume[date] < stock_data['Volume'][date]:
                    if (res_line[-1] < stock_data['Close'][date] and res_line[-1] < stock_data['Open'][date]):
                        higher_than_res.append([date.strftime('%Y-%m-%d'), stock_data['Close'][date]])
                    elif (sup_line[-1] > stock_data['Close'][date] and sup_line[-1] > stock_data['Open'][date]):
                        less_than_sup.append([date.strftime('%Y-%m-%d'), stock_data['Close'][date]])

    elif method == 2:
        pos_bias = np.mean(pos_bias) + 2 * np.std(pos_bias)
        neg_bias = np.mean(neg_bias) - 2 * np.std(neg_bias)
        print('pos_bias', pos_bias)
        print('neg_bias', neg_bias)
        for date, value in ma_result.items():
            if not math.isnan(value):
                res_line.append(value * pos_bias + value)
                sup_line.append(value * neg_bias + value)
            else:
                res_line.append(None)
                sup_line.append(None)
            if res_line[-1]:
                if (res_line[-1] < stock_data['Close'][date] and res_line[-1] < stock_data['Open'][date]):
                    higher_than_res.append([date.strftime('%Y-%m-%d'), stock_data['Close'][date]])
                elif (sup_line[-1] > stock_data['Close'][date] and sup_line[-1] > stock_data['Open'][date]):
                    less_than_sup.append([date.strftime('%Y-%m-%d'), stock_data['Close'][date]])
    result = {
        'candle_data':candle_data,
        'res_line':res_line,
        'ma_result':ma_result.replace(float('nan'), None).tolist(),
        'sup_line':sup_line,
        'higher_than_res':higher_than_res,
        'less_than_sup':less_than_sup
    }
    return result

def KD_line(stock_code, start, ma_len,):
    df = yf.download(stock_code, start=start)
    df['Lowest Low'] = df['Low'].rolling(window=ma_len).min()
    df['Highest High'] = df['High'].rolling(window=ma_len).max()
    df['RSV'] = (df['Close'] - df['Lowest Low']) / (df['Highest High'] - df['Lowest Low']) * 100
    df['K']   = df['RSV'].ewm(com=2, adjust=False).mean()
    df['D']   = df['K'].ewm(com=2, adjust=False).mean()
    buy_signal = []
    sell_signal = []
    for date in df.index:
        if df['K'][date] and df['D'][date]:
            if df['K'][date] > 80 and df['D'][date] > 80:
                sell_signal.append([date.strftime('%Y-%m-%d'), df['Close'][date]])
            elif df['K'][date] < 20 and df['D'][date] < 20:
                buy_signal.append([date.strftime('%Y-%m-%d'), df['Close'][date]])
    #print(df)
    result = {
        'K':df['K'].replace(float('nan'), None).tolist(),
        'D':df['D'].replace(float('nan'), None).tolist(),
        'sell_kd':sell_signal,
        'buy_kd':buy_signal
    }
    return result


def nan2none(target):
    package = {}
    for key, elem_pd in target.items():
        if type(elem_pd) is pd.Series:
            package[key] = elem_pd.replace(float('nan'), None).tolist()
        else:
            package[key] = elem_pd
    return package
def fetch_stock_data(stock_code, start_date):
    """
    Fetch historical stock data using yfinance.
    """
    data = yf.download(stock_code, start=start_date)
    data['Date'] = data.index
    data.reset_index(drop=True, inplace=True)
    return data

def MACD(stock_code, start_date, fastperiod, slowperiod, signalperiod):
    data = fetch_stock_data(stock_code, start_date)
    macd, macdsignal, macdhist = talib.MACD(
        data['Close'], fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod
    )
    return {"macd": macd, "macdsignal": macdsignal, "macdhist": macdhist}

def Bollinger_Channel(stock_code, start_date, ma_length):
    data = fetch_stock_data(stock_code, start_date)
    upper, middle, lower = talib.BBANDS(
        data['Close'], timeperiod=ma_length, nbdevup=2, nbdevdn=2, matype=0
    )
    return {"upper": upper, "middle": middle, "lower": lower}

def RSI(stock_code, start_date, timeperiod):
    data = fetch_stock_data(stock_code, start_date)
    rsi = talib.RSI(data['Close'], timeperiod=timeperiod)
    return {"rsi": rsi}

def ADX(stock_code, start_date, timeperiod):
    data = fetch_stock_data(stock_code, start_date)
    adx = talib.ADX(data['High'], data['Low'], data['Close'], timeperiod=timeperiod)
    return {"adx": adx}

def DMI(stock_code, start_date, timeperiod):
    data = fetch_stock_data(stock_code, start_date)
    plus_di = talib.PLUS_DI(data['High'], data['Low'], data['Close'], timeperiod=timeperiod)
    minus_di = talib.MINUS_DI(data['High'], data['Low'], data['Close'], timeperiod=timeperiod)
    return {"plus_di": plus_di, "minus_di": minus_di}

def K_Line_Status(stock_code, start_date, pattern):
    """
    Identify specific candlestick patterns using TA-Lib.
    """
    data = fetch_stock_data(stock_code, start_date)
    
    patterns = {
        "CDL3WHITESOLDIERS":talib.CDL3WHITESOLDIERS,
        "CDL3BLACKCROWS":talib.CDL3BLACKCROWS,
        "DOJI": talib.CDLDOJI,
        "CDLEVENINGSTAR":talib.CDLEVENINGSTAR,
        "MORNINGSTAR": talib.CDLMORNINGSTAR,
        "HAMMER": talib.CDLHAMMER,
        "ENGULFING": talib.CDLENGULFING,
        "SHOOTINGSTAR": talib.CDLSHOOTINGSTAR
    }
    
    if pattern not in patterns:
        raise ValueError(f"Unsupported pattern: {pattern}")
    
    result = patterns[pattern](data['Open'], data['High'], data['Low'], data['Close'])
    return {"pattern": result}

def market_signal_with_patterns(stock_code, start_date, **arg):
    """
    Analyze indicators and candlestick patterns to decide buy, sell, or hold signals.
    """

    if not arg:
        arg = {
        "ma_length_res_sup": 20,
        "ma_mode_res_sup": 'SMA',
        "method_res_sup": 1,
        "ma_length_kd": 20,
        "fastperiod_macd": 12,
        "slowperiod_macd": 26,
        "signalperiod_macd": 9,
        "ma_length_bollinger": 20,
        "timeperiod_rsi": 14,
        "timeperiod_adx": 14,
        "timeperiod_dmi": 14,
        "pattern_kline":"DOJI",
    }
    else:
        print('market_signal_with_patterns: using input arg, not default arg.', arg)
    # Combine Signals
    today = datetime.now().strftime("%Y-%m-%d")
    data = fetch_stock_data(stock_code, start_date)
    signals = {}
    
    signals['price'] = data['Close'].iloc[-1]
    # Calculate Indicators
    ressup = Res_Sup_line(stock_code, start_date, arg["ma_length_res_sup"], arg["ma_mode_res_sup"], arg["method_res_sup"])
    kd = KD_line(stock_code, start_date, arg["ma_length_kd"],)
    for i in ressup['higher_than_res']:
        if datetime.now().strftime("%Y-%m-%d") in i:
            signals["Res_Sup_line"] = False
            break
        else:
            signals["Res_Sup_line"] = None
    for i in ressup['less_than_sup']:
        if datetime.now().strftime("%Y-%m-%d") in i:
            signals["Res_Sup_line"] = True
    for i in kd['sell_kd']:
        if datetime.now().strftime("%Y-%m-%d") in i:
            signals["Res_Sup_line"] = False
            break
        else:
            signals["KD_line"] = None
    for i in kd['buy_kd']:
        if datetime.now().strftime("%Y-%m-%d") in i:
            signals["KD_line"] = True

    macd_result = MACD(stock_code, start_date, arg["fastperiod_macd"], arg["slowperiod_macd"], arg["signalperiod_macd"])
    bollinger_result = Bollinger_Channel(stock_code, start_date, arg["fastperiod_macd"])
    rsi_result = RSI(stock_code, start_date, arg["timeperiod_rsi"])
    adx_result = ADX(stock_code, start_date, arg["timeperiod_adx"])
    dmi_result = DMI(stock_code, start_date, arg["timeperiod_dmi"])

    # Get K-Line Pattern Signal
    kline_result = K_Line_Status(stock_code, start_date, arg["pattern_kline"])["pattern"]
    kline_signal = None
    if kline_result.iloc[-1] > 0:  # Bullish Pattern
        kline_signal = True  # Buy
    elif kline_result.iloc[-1] < 0:  # Bearish Pattern
        kline_signal = False  # Sell



    # MACD Signal
    macd, macdsignal = macd_result["macd"], macd_result["macdsignal"]
    if macd.iloc[-1] > macdsignal.iloc[-1] and macd.iloc[-2] <= macdsignal.iloc[-2]:
        signals["MACD"] = True  # Buy
    elif macd.iloc[-1] < macdsignal.iloc[-1] and macd.iloc[-2] >= macdsignal.iloc[-2]:
        signals["MACD"] = False  # Sell
    else:
        signals["MACD"] = None  # Hold

    # RSI Signal
    rsi = rsi_result["rsi"]
    if rsi.iloc[-1] < 30:
        signals["RSI"] = True  # Buy
    elif rsi.iloc[-1] > 70:
        signals["RSI"] = False  # Sell
    else:
        signals["RSI"] = None  # Hold

    # Bollinger Bands Signal
    upper, lower = bollinger_result["upper"], bollinger_result["lower"]
    if data['Close'].iloc[-1] < lower.iloc[-1]:
        signals["Bollinger"] = True  # Buy
    elif data['Close'].iloc[-1] > upper.iloc[-1]:
        signals["Bollinger"] = False  # Sell
    else:
        signals["Bollinger"] = None  # Hold

    # ADX Signal
    adx = adx_result["adx"]
    plus_di, minus_di = dmi_result["plus_di"], dmi_result["minus_di"]
    if adx.iloc[-1] > 25:
        if plus_di.iloc[-1] > minus_di.iloc[-1]:
            signals["ADX"] = True  # Buy
        elif plus_di.iloc[-1] < minus_di.iloc[-1]:
            signals["ADX"] = False  # Sell
        else:
            signals["ADX"] = None  # Hold
    else:
        signals["ADX"] = None  # Hold

    # Add K-Line Signal
    signals["K-Line"] = kline_signal

    return today, signals

def backtest_signals(stock_code, start_date, **arg):
    """
    Backtest historical buy and sell signals for indicators.
    Returns a dictionary with buy/sell signals for each indicator.
    """
    if not arg:
        arg = {
            "ma_length_res_sup": 20,
            "ma_mode_res_sup": 'SMA',
            "method_res_sup": 1,
            "ma_length_kd": 20,
            "fastperiod_macd": 12,
            "slowperiod_macd": 26,
            "signalperiod_macd": 9,
            "ma_length_bollinger": 20,
            "timeperiod_rsi": 14,
            "timeperiod_adx": 14,
            "timeperiod_dmi": 14,
            "pattern_kline": "DOJI",
        }

    data = fetch_stock_data(stock_code, start_date)
    signals = {
        "MACD": {"buy": [], "sell": []},
        "RSI": {"buy": [], "sell": []},
        "Bollinger": {"buy": [], "sell": []},
        "ADX": {"buy": [], "sell": []},
        "K-Line": {"buy": [], "sell": []}
    }

    # MACD Backtest
    macd_result = MACD(stock_code, start_date, arg["fastperiod_macd"], arg["slowperiod_macd"], arg["signalperiod_macd"])
    macd, macdsignal = macd_result["macd"], macd_result["macdsignal"]
    for i in range(1, len(data)):
        if macd.iloc[i] > macdsignal.iloc[i] and macd.iloc[i - 1] <= macdsignal.iloc[i - 1]:
            signals["MACD"]["buy"].append((str(data['Date'].iloc[i]), data['Close'].iloc[i]))
        elif macd.iloc[i] < macdsignal.iloc[i] and macd.iloc[i - 1] >= macdsignal.iloc[i - 1]:
            signals["MACD"]["sell"].append((str(data['Date'].iloc[i]), data['Close'].iloc[i]))

    # RSI Backtest
    rsi_result = RSI(stock_code, start_date, arg["timeperiod_rsi"])
    rsi = rsi_result["rsi"]
    for i in range(len(data)):
        if rsi.iloc[i] < 30:
            signals["RSI"]["buy"].append((str(data['Date'].iloc[i]), data['Close'].iloc[i]))
        elif rsi.iloc[i] > 70:
            signals["RSI"]["sell"].append((str(data['Date'].iloc[i]), data['Close'].iloc[i]))

    # Bollinger Backtest
    bollinger_result = Bollinger_Channel(stock_code, start_date, arg["ma_length_bollinger"])
    upper, lower = bollinger_result["upper"], bollinger_result["lower"]
    for i in range(len(data)):
        if data['Close'].iloc[i] < lower.iloc[i]:
            signals["Bollinger"]["buy"].append((str(data['Date'].iloc[i]), data['Close'].iloc[i]))
        elif data['Close'].iloc[i] > upper.iloc[i]:
            signals["Bollinger"]["sell"].append((str(data['Date'].iloc[i]), data['Close'].iloc[i]))

    # ADX Backtest
    adx_result = ADX(stock_code, start_date, arg["timeperiod_adx"])
    dmi_result = DMI(stock_code, start_date, arg["timeperiod_dmi"])
    adx = adx_result["adx"]
    plus_di, minus_di = dmi_result["plus_di"], dmi_result["minus_di"]
    for i in range(len(data)):
        if adx.iloc[i] > 25:
            if plus_di.iloc[i] > minus_di.iloc[i]:
                signals["ADX"]["buy"].append((str(data['Date'].iloc[i]), data['Close'].iloc[i]))
            elif plus_di.iloc[i] < minus_di.iloc[i]:
                signals["ADX"]["sell"].append((str(data['Date'].iloc[i]), data['Close'].iloc[i]))

    # K-Line Backtest
    kline_result = K_Line_Status(stock_code, start_date, arg["pattern_kline"])["pattern"]
    for i in range(len(data)):
        if kline_result.iloc[i] > 0:  # Bullish Pattern
            signals["K-Line"]["buy"].append((str(data['Date'].iloc[i]), data['Close'].iloc[i]))
        elif kline_result.iloc[i] < 0:  # Bearish Pattern
            signals["K-Line"]["sell"].append((str(data['Date'].iloc[i]), data['Close'].iloc[i]))

    return signals