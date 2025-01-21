from django.http import JsonResponse

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime


from django.views.decorators.csrf import ensure_csrf_cookie
#import matplotlib
#matplotlib.use('Agg')  # 使用非互動後端，避免 GUI 啟動


@ensure_csrf_cookie
def set_csrf_cookie(request):
    return JsonResponse({"message": "CSRF cookie set"})

from lib.strategy.x_distance_method import Distance_method
from lib.strategy.x_etf_rsi  import rsi_strategy
from lib.strategy.x_strategies import *

def extract_parameters(params):
    """輔助函數：提取並處理參數"""
    return {
        
        "ma_length_res_sup": int(params.get('ma_length_res_sup')) if params.get('ma_length_res_sup') else None,
        "ma_mode_res_sup": params.get('ma_mode_res_sup'),
        "method_res_sup": int(params.get('method_res_sup')) if params.get('method_res_sup') else None,
        "ma_length_kd": int(params.get('ma_length_kd')) if params.get('ma_length_kd') else None,
        "fastperiod_macd": int(params.get('fastperiod_macd')) if params.get('fastperiod_macd') else None,
        "slowperiod_macd": int(params.get('slowperiod_macd')) if params.get('slowperiod_macd') else None,
        "signalperiod_macd": int(params.get('signalperiod_macd')) if params.get('signalperiod_macd') else None,
        "ma_length_bollinger": int(params.get('ma_length_bollinger')) if params.get('ma_length_bollinger') else None,
        "timeperiod_rsi": int(params.get('timeperiod_rsi')) if params.get('timeperiod_rsi') else None,
        "timeperiod_adx": int(params.get('timeperiod_adx')) if params.get('timeperiod_adx') else None,
        "timeperiod_dmi": int(params.get('timeperiod_dmi')) if params.get('timeperiod_dmi') else None,
        "pattern_kline": params.get('pattern_kline')
    }

def distance_method_api(request):

    if request.method == 'POST':

        for key, value in request.POST.items():
            print('{} is {}'.format(key, type(value)))
        dm_obj = Distance_method(
            request.POST['stock1'],
            request.POST['stock2'],
            request.POST['start_date'],
            request.POST['end_date'],
            int(request.POST['window_size']),
            int(request.POST['n_std']),
           )
        
        pd_pack = dm_obj.run()
        pd_pack = dm_obj.nan2none(pd_pack)
        pd_pack = dm_obj.pd2list(pd_pack)
        #print(pd_pack)
        #return JsonResponse({'response1': [1, 2, 3],
        #                     'response2': f'Received message: message1'})
        return JsonResponse(pd_pack)
    elif request.method == "OPTIONS":
        # Handle preflight requests
        response = JsonResponse({"message": "Preflight OK"})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, X-CSRFToken"
        return response
    
    return JsonResponse({"error": "Method not allowed"}, status=405)


class StrategyListView(APIView):
    def get(self, request):
        strategies = {
            "distance_method": "Stock pair trading strategy using distance method.",
            "etf_rsi": "RSI-based ETF trading strategy."
        }
        return Response(strategies)

class RunStrategyView(APIView):
    def post(self, request, strategy_name):
        params = request.data  # 獲取用戶輸入的參數
        print(params)
        for key, value in params.items():
            print('{} is {} = {}'.format(key, type(value), value))
        try:
            if strategy_name == "distance_method":
                stock1 = params.get("stock1", "AAPL")
                stock2 = params.get("stock2", "GLD")
                start_date = params.get("start_date", "2021-01-01")
                end_date = params.get("end_date", datetime.today().strftime('%Y-%m-%d'))
                window_size = int(params.get("window_size", 200))
                n_std = int(params.get("n_std", 2))
                print(stock1, stock2, start_date, end_date, window_size, n_std)
                strategy = Distance_method(stock1, stock2, start_date, end_date, window_size, n_std)
                result = strategy.run()
                pd_pack = strategy.nan2none(result)
                result = strategy.pd2list(pd_pack)
            
            elif strategy_name == "backtrader":
                # TODO
                try:
                    # 獲取必要參數
                    ticker = params.get("ticker", "AAPL")
                    start_date = params.get("start_date", "2020-01-01")
                    end_date = params.get("end_date", datetime.today().strftime('%Y-%m-%d'))
                    cash = float(params.get("cash", 10000.0))
                    strategy_type = params.get("strategy_type", "rsi")  # 默認為 RSI 策略

                    # 根據策略類型提取對應參數
                    if strategy_type == "rsi":
                        rsi_period = int(params.get("rsi_period", 14))
                        overbought = int(params.get("overbought", 70))
                        oversold = int(params.get("oversold", 30))
                        strategy_class = RsiStrategy
                        strategy_params = {
                            "rsi_period": rsi_period,
                            "overbought": overbought,
                            "oversold": oversold,
                        }
                    elif strategy_type == "sma":
                        fast_period = int(params.get("fast_period", 10))
                        slow_period = int(params.get("slow_period", 30))
                        strategy_class = SmaCrossStrategy
                        strategy_params = {
                            "fast_period": fast_period,
                            "slow_period": slow_period,
                        }
                    else:
                        return JsonResponse({"error": "Unsupported strategy type."}, status=status.HTTP_400_BAD_REQUEST)

                    # 執行回測
                    result = run_backtest(strategy_class, strategy_params, ticker, start_date, end_date, cash)

                    # 返回結果
                    response_data = {
                        "initial_cash": result["initial_cash"],
                        "final_cash": result["final_cash"],
                    }

                    # 將圖片為 base64 編碼返回
                    response_data["plot_image"] = result["plot_image"]

                    return JsonResponse(response_data, status=status.HTTP_200_OK)

                except Exception as e:
                    print(e)
                    return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                # TODO
                pass
            
            elif strategy_name == "etf_rsi":
                prod = params.get("prod", "0050.TW")
                start_date = params.get("start_date", "2021-01-01")
                end_date = params.get("end_date", datetime.today().strftime('%Y-%m-%d'))
                long_period = int(params.get("long", 20))
                short_period = int(params.get("short", 5))
                
                result = rsi_strategy(prod, start_date, end_date, long_period, short_period)
            
            elif strategy_name == "pricing":
                '''
                data_config.append("stock_code", stock_code);
                data_config.append("start_date", start_date);
                data_config.append("end_date", end_date);
                data_config.append("multiplier_1", multiplier_1);
                data_config.append("multiplier_2", multiplier_2);
                data_config.append("multiplier_3", multiplier_3);
                data_config.append("multiplier_4", multiplier_4);
                data_config.append("multiplier_5", multiplier_5);
                data_config.append("multiplier_6", multiplier_6);
                '''
                stock_ticker = params.get("stock_code", "2330.TW")
                start_date = params.get("start_date", "2021-01-01")
                end_date = params.get("end_date", datetime.today().strftime('%Y-%m-%d'))
                interval = params.get("time_frame", '3mo')
                # 建立物件
                dividend_price_method = DividendPriceMethod(stock_ticker=stock_ticker, start_date=start_date, end_date=end_date)
                high_low_price_method = HighLowPriceMethod(stock_ticker=stock_ticker, start_date=start_date, end_date=end_date)
                pb_method = PBMethod(stock_ticker=stock_ticker, start_date=start_date, end_date=end_date)
                pe_method = PEMethod(stock_ticker=stock_ticker, start_date=start_date, end_date=end_date)
                river_method = RiverChartMethod(stock_ticker=stock_ticker, start_date=start_date, end_date=end_date, interval=interval)
                # 計算分類
                h_l_a_div                = dividend_price_method.fetch_dividend_and_price()
                current_price, h_l_a_hlm = high_low_price_method.fetch_high_low_price()
                current_price, h_l_a_pbm = pb_method.fetch_PB()
                current_price, h_l_a_pem = pe_method.fetch_PE()
                current_price, classify_price, river_lines, candle_line = river_method.fetch_river_chart_data()
                #data['Open'], data['High'], data['Low'], data['Close'], data['Volume']
                
                candle_data = {
                    'date':candle_line.index.strftime('%Y-%m-%d').tolist(),
                    'Open':candle_line['Open'].tolist(),
                    'Close':candle_line['Close'].tolist(),
                    'High':candle_line['High'].tolist(),
                    'Low':candle_line['Low'].tolist(),
                    'Volume':candle_line['Volume'].tolist(),
                }
                h_l_a_div = {'low_price': h_l_a_div['average_dividend'] * 15, 
                             'high_price': h_l_a_div['average_dividend'] * 30,
                             'avg_price': h_l_a_div['average_dividend'] * 20
                             }
                result = {
                    "dividend": h_l_a_div,
                    "high_low": h_l_a_hlm,
                    "pb": h_l_a_pbm,
                    "pe": h_l_a_pem,
                    "river": classify_price,
                    'river_lines':river_lines,
                    'candle_data':candle_data,
                    "current_price": current_price
                }
            
            elif strategy_name == "tracker":
                stock_code = params.get('stock_code')
                start = params.get('start_date')
                start_date = start
                # 共用參數初始化
                ma_length_res_sup = int(params.get('ma_length_res_sup')) if params.get('ma_length_res_sup') else None
                ma_mode_res_sup = params.get('ma_mode_res_sup')
                method_res_sup = int(params.get('method_res_sup')) if params.get('method_res_sup') else None

                ma_length_kd = int(params.get('ma_length_kd')) if params.get('ma_length_kd') else None

                fastperiod_macd = int(params.get('fastperiod_macd')) if params.get('fastperiod_macd') else None
                slowperiod_macd = int(params.get('slowperiod_macd')) if params.get('slowperiod_macd') else None
                signalperiod_macd = int(params.get('signalperiod_macd')) if params.get('signalperiod_macd') else None

                ma_length_bollinger = int(params.get('ma_length_bollinger')) if params.get('ma_length_bollinger') else None

                timeperiod_rsi = int(params.get('timeperiod_rsi')) if params.get('timeperiod_rsi') else None
                timeperiod_adx = int(params.get('timeperiod_adx')) if params.get('timeperiod_adx') else None
                timeperiod_dmi = int(params.get('timeperiod_dmi')) if params.get('timeperiod_dmi') else None

                pattern_kline = params.get('pattern_kline')

                # 計算所有技術指標
                results = {}

                # Resistance Support Line
                if ma_length_res_sup and ma_mode_res_sup and method_res_sup:
                    results['res_sup'] = Res_Sup_line(stock_code, start, ma_length_res_sup, ma_mode_res_sup, method_res_sup)

                # KD Line
                if ma_length_kd:
                    results['kd'] = KD_line(stock_code, start, ma_length_kd)

                # MACD
                if fastperiod_macd and slowperiod_macd and signalperiod_macd:
                      results['macd'] = nan2none(MACD(stock_code, start_date, fastperiod_macd, slowperiod_macd, signalperiod_macd))

                # Bollinger Channel
                if ma_length_bollinger:
                    results['bollinger'] = nan2none(Bollinger_Channel(stock_code, start_date, ma_length_bollinger))

                # RSI
                if timeperiod_rsi:
                    results['rsi'] = nan2none(RSI(stock_code, start_date, timeperiod_rsi))

                # ADX
                if timeperiod_adx:
                    results['adx'] = nan2none(ADX(stock_code, start_date, timeperiod_adx))

                # DMI
                if timeperiod_dmi:
                    results['dmi'] = nan2none(DMI(stock_code, start_date, timeperiod_dmi))

                # K Line Status
                if pattern_kline:
                    results['kline_status'] = nan2none(K_Line_Status(stock_code, start_date, pattern_kline))
                
                # 返回所有結果
                signals = backtest_signals(stock_code, start_date, **extract_parameters(params))
                results['signals'] = signals
                result = results
            
            else:
                return JsonResponse({"error": "Unknown strategy."}, status=status.HTTP_400_BAD_REQUEST)
            
            return JsonResponse(result, status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            traceback.print_exc()  # 打印完整的錯誤日誌到控制台
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)