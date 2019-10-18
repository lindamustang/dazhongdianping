from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
import json

base_url = 'http://www.dianping.com/ajax/json/shopDynamic/allReview?'
headers_dish={
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Host': 'www.dianping.com',
    'Referer': 'http://www.dianping.com/shop/72351070',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/535.19',
    'Accept-Encoding': 'gzip',
    'X-Requested-With': 'XMLHttpRequest',
    'cookie': '_lxsdk_cuid=16d62ea6ca027-0a4910b28fb0df-67e1b3f-100200-16d62ea6ca1c8; _lxsdk=16d62ea6ca027-0a4910b28fb0df-67e1b3f-100200-16d62ea6ca1c8; _hc.v=c882456c-1f19-3cb7-e5a0-1121d5489bdd.1569322594; dper=59ce2667699ea89fbc4655c1e760911f6051307027e8a99460b3570c646358deb627eb975f642a5ecbc0e1b74b3de0882d44ccedf3dc4fdc7ea8611ccf9a482454c63f6b7f22e15bf3220de0ccf496424c9735957c231c6d1b6c9fa1065c1c04; ua=%E7%99%BD%E5%99%AA%E9%9F%B3; ctu=41c1fd0e93c86ea7559dba081079ee30592d2ef5e0aeb74b35665e82babbf339; cy=1; cye=shanghai; s_ViewType=10; aburl=1; ll=7fd06e815b796be3df069dec7836c3df; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; _lxsdk_s=16dd28e3f8f-bde-430-102%7C%7C2'
}


def get_dish():

   url = base_url + 'shopId='+str(72351070)+'&cityId=1&shopType=10&tcv=51'
   text = requests.get(url = url,headers = headers_dish)
   result = text.json()
   dish_str = get_dish_list(result)
   print(dish_str)


def get_dish_list(result):
    if result:
        dish_list = result.get('dishTagStrList')
        if dish_list:
            dish_str = ','.join(dish_list)

    return dish_str




get_dish()


