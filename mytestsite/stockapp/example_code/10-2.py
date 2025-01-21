# 載入必要套件
from Data import getFMPriceAndRevenue
from BackTest import ChartTrade, Performance
import pandas as pd
import mplfinance as mpf

# 取得回測資料
prod = '2618'
data = getFMPriceAndRevenue(prod, '2010-01-01', '2022-05-20')

# 繪製副圖
addp = []
addp.append(mpf.make_addplot(
    data['revenue'], panel=1, type='bar', color='red', secondary_y=False))

# 繪製K線圖與交易明細
ChartTrade(data, addp=addp, v_enable=False)
