


def add_or_update_stock_code(user_subscription, stock_code, parameters):
    data = user_subscription.data
    

    # 更新或新增 `stock_code`
    data[stock_code] = data.get(stock_code, {})
    data[stock_code]["parameters"] = parameters
    data[stock_code]["signals"] = data[stock_code].get("signals", {})

    # 更新資料庫
    user_subscription.data = data
    user_subscription.save()
    print(f"Updated parameters for stock code {stock_code}.")

def add_signal(user_subscription, stock_code, date, signal):
    data = user_subscription.data

    if stock_code not in data:
        raise ValueError(f"Stock code {stock_code} does not exist in the user's subscriptions.")

    # 新增信號
    data[stock_code]["signals"][date]=signal

    # 更新資料庫
    user_subscription.data = data
    user_subscription.save()
    print(f"Added signal for stock code {stock_code}.")


def get_signals(user_subscription, stock_code, date=None):
    data = user_subscription.data


    if stock_code not in data:
        raise ValueError(f"Stock code {stock_code} does not exist in the user's subscriptions.")

    signals = data[stock_code].get("signals", {})
    if date:
        signals = signals[date]

    return signals