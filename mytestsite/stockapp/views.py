from django.shortcuts import render
from .models import UserSubscription
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
import json
from .x_distance_method import *
from .x_etf_rsi import *
import requests

from django.contrib import messages
from django.shortcuts import redirect
import logging
from django.template.loader import render_to_string
from django.db import models
import datetime
logger = logging.getLogger(__name__)

def extract_parameters(params):
    """輔助函數：提取並處理參數"""
    return {
        "start_date": params.get('start_date'),
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
def index_home(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Sorry! Please log in.')
        return redirect("http://127.0.0.1:7999/account/login")  # Update as needed

    user = request.user

    # Check for AJAX GET request
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        subscription = UserSubscription.objects.filter(user=user).first()
        if subscription:
            data = {
                "subscriptions": subscription.data,
                "created_at": subscription.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            return JsonResponse(data, status=200)

        return JsonResponse({"error": "No subscriptions found."}, status=404)

    # Render home.html for non-AJAX GET requests
    if request.method == 'GET':
        return render(request, '../templates/home.html')

    # Handle POST requests (if needed)
    if request.method == 'POST':
        # Example logic for handling POST (if required)
        pass


def html_interface(request):
    
    if not request.user.is_authenticated:
        messages.success(request, 'Sorry ! Please Log In.')
        return redirect("http://127.0.0.1:7999/account/login")  # //////////////////要修改////////////////////////  
    elif '/distance_method' in request.path :
        print(request.path)
        return render(request, '../templates/distance_method.html')
        #return redirect("http://127.0.0.1:8000/stockapp/distance_method")
    
    elif '/etf_rsi' in request.path :
        print(request.path)
        if request.method == 'POST':
            for key, value in request.POST.items():
                print('{} is {} = {}'.format(key, type(value), value))        
            url = "http://127.0.0.1:8001/api/strategies/etf_rsi/run/"
            headers = {"Content-Type"  : "application/json"}
            data = {key: value for key, value in request.POST.items()}
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # 確保沒有 HTTP 錯誤

            # 返回後端 API 的 JSON 結果
            return JsonResponse(response.json(), status=response.status_code)
        return render(request, '../templates/etf.html')
        #return redirect("http://127.0.0.1:8000/stockapp/etf_rsi")
    # backtrader
    elif '/backtrader' in request.path :
        print(request.path)
        return render(request, '../templates/backtrader.html')
    
    elif '/pricing' in request.path :
        print(request.path)
        return render(request, '../templates/pricing.html')
    
    elif '/tracker' in request.path:
        return render(request, '../templates/tracker.html')
    
    elif '/delete' in request.path:
        if request.method == 'POST':
            for key, value in request.POST.items():
                print('{} is {} = {}'.format(key, type(value), value))     
            user = request.user
            user_subscription = UserSubscription.objects.filter(user=user).first()
            data = user_subscription.data
            stock_code = request.POST.get("stock_code")
            if stock_code not in data:
                raise ValueError(f"Stock code {stock_code} does not exist in the user's subscriptions.")

            # 刪除指定股票代碼及其所有資訊
            del data[stock_code]

            # 更新資料庫
            user_subscription.data = data
            user_subscription.save()
            print(f"Deleted stock code {stock_code} and its information.")
            return JsonResponse({"message": f"Stock {stock_code} deleted successfully."}, status=200)
        return redirect("http://127.0.0.1:8000/stockapp")
    
    elif '/subscription' in request.path:
        if request.method == 'POST':
            # 提取 POST 請求中的所有參數
            params = request.POST
            for key, value in params.items():
                print(f"{key} is {type(value)} = {value}")

            # 提取並處理參數
            parameters = extract_parameters(params)
            stock_code = params.get('stock_code')
            user = request.user

            try:
                # 確認用戶是否已有訂閱記錄
                subscription = UserSubscription.objects.filter(user=user).first()

                if subscription:
                    # 檢查該股票代碼是否已存在於訂閱資料中
                    subscriptions_data = subscription.data
                    if stock_code in subscriptions_data:
                        messages.warning(request, f"訂閱已存在: {stock_code}")
                        print(f"訂閱已存在: {stock_code}")

                        # 返回用戶所有訂閱資料
                        data = {
                            "subscriptions": subscriptions_data,
                            "created_at": subscription.created_at.strftime("%Y-%m-%d %H:%M:%S")
                        }
                        return JsonResponse(data, status=200)

                    # 新增股票代碼到訂閱資料
                    subscriptions_data[stock_code] = {
                        "created_at" :datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "parameters": parameters,
                        "signals": {}
                    }
                    subscription.save()
                    messages.success(request, f"新增訂閱成功: {stock_code}")
                    print(f"新增訂閱成功: {stock_code}")
                    return JsonResponse({"message": "新增成功"}, status=201)

                # 若用戶無訂閱記錄，創建新訂閱
                data = {
                        stock_code: {
                        "created_at" :datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "parameters": parameters,
                        "signals": {}
                        }
                    }
                UserSubscription.objects.create(user=user, data=data)
                messages.success(request, f"訂閱創建成功: {stock_code}")
                print(f"訂閱創建成功: {stock_code}")
                return JsonResponse({"message": "訂閱創建成功"}, status=201)

            except Exception as e:
                # 錯誤處理
                logger.error(f"訂閱處理失敗: {e}")
                messages.error(request, "訂閱處理失敗，請稍後再試")
                return JsonResponse({"message": f"訂閱處理失敗: {str(e)}"}, status=500)
    
    else:
        print('Something wrong')
        return render(request, '../templates/stockapp.html')


# the following is the original code
# and are all included in html_interface(request)
def index_distance_method(request):

    # if request.method == 'POST':
    #     for key, value in request.POST.items():
    #         print('{} is {} = {}'.format(key, type(value), value))
    #     dm_obj = Distance_method(
    #         request.POST['stock1'],
    #         request.POST['stock2'],
    #         request.POST['start_date'],
    #         request.POST['end_date'],
    #         int(request.POST['window_size']),
    #         int(request.POST['n_std']),
    #        )
    #     pd_pack = dm_obj.run()
    #     pd_pack = dm_obj.nan2none(pd_pack)
    #     pd_pack = dm_obj.pd2list(pd_pack)
    #     #print(pd_pack)
    #     #return JsonResponse({'response1': [1, 2, 3],
    #     #                     'response2': f'Received message: message1'})
    #     return JsonResponse(pd_pack)
    '''
    if request.method == 'POST':
        for key, value in request.POST.items():
            print('{} is {} = {}'.format(key, type(value), value))        
        url = "http://127.0.0.1:8001/api/strategies/distance_method/run/"
        headers = {"Content-Type"  : "application/json"}
        data = {key: value for key, value in request.POST.items()}
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # 確保沒有 HTTP 錯誤

        # 返回後端 API 的 JSON 結果
        return JsonResponse(response.json(), status=response.status_code)
    '''

    return render(request, '../templates/distance_method.html')

def index_etf(request):

    # if request.method == 'POST':

    #     for key, value in request.POST.items():
    #         print('{} is {} type = {}'.format(key, type(value), value))

    #     pd_pack = rsi_strategy(
    #                         prod = request.POST['stock'], 
    #                         st   = request.POST['start_date'], 
    #                         en   = request.POST['end_date'], 
    #                         long = int(request.POST['LongRSI']), 
    #                         short= int(request.POST['ShortRSI'])
    #                         )

    #     return JsonResponse(pd_pack, safe = False)
    if request.method == 'POST':
        for key, value in request.POST.items():
            print('{} is {} = {}'.format(key, type(value), value))        
        url = "http://127.0.0.1:8001/api/strategies/etf_rsi/run/"
        headers = {"Content-Type"  : "application/json"}
        data = {key: value for key, value in request.POST.items()}
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # 確保沒有 HTTP 錯誤

        # 返回後端 API 的 JSON 結果
        return JsonResponse(response.json(), status=response.status_code)
    return render(request, '../templates/etf.html')