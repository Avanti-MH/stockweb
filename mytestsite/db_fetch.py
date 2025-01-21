import os
import django

import sys

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# 將上一層目錄添加到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 現在可以導入 utils 模組
from api_dir.func_api.lib.strategy.x_strategies import *
from db_handle.db_operate import *


# 設定 Django 環境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mytestsite.settings")  # 替換為你的專案名稱.settings
django.setup()

from stockapp.models import UserSubscription  # 匯入你的模型

def fetch_all_subscriptions():
    # 從資料庫提取所有訂閱資料
    subscriptions = UserSubscription.objects.select_related('user').all()

    if not subscriptions.exists():
        print("No subscriptions found in the database.")
        return

    # 格式化輸出
    for sub in subscriptions:
        user = sub.user
        data = sub.data  # 提取 JSONField 的內容

        print(f"User: {user.username}")
        print(f"Email: {user.email}")
        
        subscriptions_data = data
        for stock_code, stock_data in subscriptions_data.items():
            print(f"Stock Code: {stock_code}")

            parameters = stock_data.get("parameters", {})
            param = {k:v for k,v in parameters.items() if k != 'start_date' }
            print(f"  Parameters:")
            for k, v in parameters.items():
                print(f"    {k} = {v}")
            signals = stock_data.get("signals", {})
            if signals:
                print(signals)
                print("  Signals:")
                for date, signal in signals.items():
                    print(f"    {date} :")
                    for k, v in signal.items():
                        print(f"        {k} = {v}")
            else:
                print("  No signals found.")

        print("-" * 30)

def run_subscription():
    # 從資料庫提取所有訂閱資料
    subscriptions = UserSubscription.objects.select_related('user').all()

    if not subscriptions.exists():
        print("No subscriptions found in the database.")
        return

    # 格式化輸出
    for sub in subscriptions:
        user = sub.user
        data = sub.data  # 提取 JSONField 的內容
        
        subscriptions_data = data
        for stock_code, stock_data in subscriptions_data.items():
            parameters = stock_data.get("parameters", {})
            info_en = False
            if parameters:
                start_date = parameters['start_date']
                param = {k:v for k,v in parameters.items() if k != 'start_date' }
                date, signals = market_signal_with_patterns(stock_code, start_date, **param)
                add_signal(user_subscription=sub, stock_code=stock_code, date=date, signal=signals)
                for k, v in signals.items():
                    if k == 'price':
                        pass
                    elif v:
                        info_en = True
                if info_en:
                    send_email(user.email, stock_code, date, signals)

        print("-" * 30)

def send_email(receiver_email, stock_code, date, signals={}):
    # 發送者和接收者的電子郵件地址
      # 使用應用程式密碼
    sender_email = "k195516@gmail.com"
    app_password = "item diig pufl uutr"
    # 建立郵件內容
    subject = f"[{date}] {stock_code} signal information"
    # body = "這是一封測試郵件，\n使用 Python 發送。"
    body = ""
    if signals:
        body += "  Signals:" + "\n"
        for k, v in signals.items():
            body += f"        {k} = {v}" + "\n"
    else:
        print("  No signals found.")
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:

            server.ehlo() # 驗證SMTP伺服器
            server.login(sender_email,app_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
               # 登入寄件者gmail
            print("郵件發送成功！")
    except Exception as e:
        print(f"郵件發送失敗：{e}")



if __name__ == "__main__":
    # send_email("mr.white9032@gmail.com")
    run_subscription()
    fetch_all_subscriptions()
    