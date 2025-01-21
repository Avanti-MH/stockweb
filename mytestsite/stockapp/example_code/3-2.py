import requests
from bs4 import BeautifulSoup

# 取得reponse
req=requests.get('https://fubon-ebrokerdj.fbs.com.tw/z/zg/zg_A_0_5.djhtm')
# 取得網頁原始碼文字
html=req.text
# 將網頁原始碼轉為Beautiful Soup
soup=BeautifulSoup(html,'html.parser')
# 取出所有的商品欄位
product=[ i.text.strip() for i in soup.find_all('td',class_='t3t1')]
# 顯示
print(product)


