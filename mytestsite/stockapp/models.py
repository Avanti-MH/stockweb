from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 每個用戶對應一條記錄
    data = models.JSONField()  # 存儲所有訂閱資料
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Subscriptions for {self.user.username}"

'''
userSubscription: 
負責創建
user 1 
    |- created_at  
    |- stock_code 1
        |- parameters
        |- signal
addSignal:
給定user、stock_code，負責新增
|- date, price, (sell, buy)

Case 1: 
    使用者沒建立過Subscription，則須建立。
    |- created_at  
    |- stock_code 1
        |- parameters
        |- signal

Case 2:
    使用者想新增訊號date, price, (sell, buy)，在
    |- created_at  
    |- stock_code 1
        |- parameters
        |- signal
    如果沒有新增過訊號，則底下新增
    |- signal
            |- date, price, (sell, buy)
    若有
    |- signal
            |- date, price, (sell, buy)
            .
            .
            |- date, price, (sell, buy)
database的資料結構:
user 1 
    |- created_at  
    |- stock_code 1
        |- parameters = models.JSONField()  # 使用通用的 JSONField
        |- signal
            |- date, price, (sell, buy)
            |- date, price, (sell, buy)
        ...
    |- stock_code n
        |- parameters = models.JSONField()  # 使用通用的 JSONField
        |- signal
            |- date, price, (sell, buy)
            |- date, price, (sell, buy)
...
user n 
    |- created_at  
    |- stock_code 1
        |- parameters = models.JSONField()  # 使用通用的 JSONField
        |- signal
            |- date, price, (sell, buy)
            |- date, price, (sell, buy)
        ...
    |- stock_code n
        |- parameters = models.JSONField()  # 使用通用的 JSONField
        |- signal
            |- date, price, (sell, buy)
            |- date, price, (sell, buy)
'''