import re
import requests
from pyquery import PyQuery as pq

headers_pinglun = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Host': 'www.dianping.com',
    'Referer': 'http://www.dianping.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/535.19',
    'Accept-Encoding': 'gzip',
    'cookie':'_lxsdk_cuid=16d62ea6ca027-0a4910b28fb0df-67e1b3f-100200-16d62ea6ca1c8; _lxsdk=16d62ea6ca027-0a4910b28fb0df-67e1b3f-100200-16d62ea6ca1c8; _hc.v=c882456c-1f19-3cb7-e5a0-1121d5489bdd.1569322594; dper=59ce2667699ea89fbc4655c1e760911f6051307027e8a99460b3570c646358deb627eb975f642a5ecbc0e1b74b3de0882d44ccedf3dc4fdc7ea8611ccf9a482454c63f6b7f22e15bf3220de0ccf496424c9735957c231c6d1b6c9fa1065c1c04; ua=%E7%99%BD%E5%99%AA%E9%9F%B3; ctu=41c1fd0e93c86ea7559dba081079ee30592d2ef5e0aeb74b35665e82babbf339; cityInfo=%7B%22cityId%22%3A1%2C%22cityName%22%3A%22%E4%B8%8A%E6%B5%B7%22%2C%22provinceId%22%3A0%2C%22parentCityId%22%3A0%2C%22cityOrderId%22%3A0%2C%22isActiveCity%22%3Afalse%2C%22cityEnName%22%3A%22shanghai%22%2C%22cityPyName%22%3Anull%2C%22cityAreaCode%22%3Anull%2C%22cityAbbrCode%22%3Anull%2C%22isOverseasCity%22%3Afalse%2C%22isScenery%22%3Afalse%2C%22TuanGouFlag%22%3A0%2C%22cityLevel%22%3A0%2C%22appHotLevel%22%3A0%2C%22gLat%22%3A0%2C%22gLng%22%3A0%2C%22directURL%22%3Anull%2C%22standardEnName%22%3Anull%7D; cy=1; cye=shanghai; s_ViewType=10; ll=7fd06e815b796be3df069dec7836c3df; _lx_utm=utm_source%3Dwww.sogou%26utm_medium%3Dorganic; _lxsdk_s=16d8614746a-be0-d32-1ce%7C1769308312%7C785'
}

# proxyHost = "http-cla.abuyun.com"
# proxyPort = "9030"
#
# # 代理隧道验证信息
# proxyUser = "HCI2P91C99SE8C4C"
# proxyPass = "0FC22654BFC6944A"
#
# proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
#       "host" : proxyHost,
#       "port" : proxyPort,
#       "user" : proxyUser,
#       "pass" : proxyPass,
#     }
#
# proxies = {
#         "http"  : proxyMeta,
#         "https" : proxyMeta,
#    }

requests.adapters.DEFAULT_RETRIES = 5

def get_message():
    url_first = "http://www.dianping.com/shop/"
    shop_id = "500332"
    page = 4
    for i in range(page):
        url = url_first + shop_id + "/review_all/p" + str(i+1)
        headers_pinglun['Referer']=headers_pinglun['Referer'] + '/shop/review_all/p' + str(i+1)
        get_content(url,headers_pinglun)

def get_content(url,headers_pinglun):

    html = requests.get(url,headers = headers_pinglun,timeout = 5)
    doc = pq(html.text)
    middle_list,svg_dict,css_dict = get_dict(doc)

    pinglunli = doc("div.reviews-items>ul>li").items()
    for li in pinglunli:
        # name = li('div.main-review>div.dper-info>a').text()
        # userid = "http://www.dianping.com" + li("div.main-review>div.dper-info>a").attr('href')
        # star = li("div.main-review>div.review-rank>span").attr('class')
        pinglun_html = li("div.main-review>div.review-words Hide").html()
        if not pinglun_html:
            pinglun_html = li("div.main-review>div.review-words").html()
        pinglun = pinglun_decode(middle_list,svg_dict,css_dict,pinglun_html)





def get_dict(doc):
    head = doc("head")
    pattern = re.compile(r'<link\srel="stylesheet"\stype="text/css"\shref="(.*?)"/>',re.S)
    css_link = re.findall(pattern,head.html())
    css_link = "http:" + css_link[1]
    #获得css链接
    css_content = requests.get(css_link).text
    re_svg_link = re.compile(r"svgmtsi.*?//([^\s]*);", re.S)
    svg_link = re.findall(re_svg_link, css_content)
    svg_link = "http://" + svg_link[0]
    svg_link = svg_link.replace(')', '')
    #获得svg链接

    middle_list,svg_dict = get_svg_dict(svg_link)
    #获得中间列表和svg字典

    re_css_dict = r".(.*?){background:-(.*?)px -(.*?)px;}"
    css_dict_num = re.findall(re_css_dict, css_content, re.S)
    css_dict = {}
    for data in css_dict_num:
        css_dict[data[0]] = (data[1], data[2])
    #构造css字典

    return middle_list,svg_dict,css_dict



def get_svg_dict(svg_link):
    svg_html = requests.get(svg_link)
    re_svg_num = re.compile(r'<path id="(.*?)" d="(.*?) (.*?) (.*?)"/>', re.S)
    svg_y = re.findall(re_svg_num, svg_html.text)
    middle_list = []
    middle_list_ = []
    svg_dict = {}
    for data in svg_y:
        middle_list_.append(data[0])
        middle_list_.append(data[2])
        middle_list.append(middle_list_)
        middle_list_ = []
    re_svg_list = re.compile(r'<textPath xlink:href="(.*?)" textLength="(.*?)">(.*?)</textPath>', re.S)
    svg_dict_re = re.findall(re_svg_list, svg_html.text)
    for data in svg_dict_re:
        svg_dict[data[0].replace('#', '')] = list(data[2])
    return middle_list,svg_dict




def pinglun_decode(middle_list,svg_dict,css_dict,pinglun_html):
    pinglun_text = pinglun_html.replace('<svgmtsi class="',',').replace('"/>',',').replace('\n','').replace(' ','')
    pinglun_text = re.sub('<imgclass=.*?alt="','',pinglun_text)
    pinglun_text = re.sub('<divclass=.*?</a></div>','',pinglun_text)
    pinglun_list = [x for x in pinglun_text.split(",") if x != '']
    pinglun_str = []
    for msg in pinglun_list:
        if msg in css_dict.keys():
            x = int(int(float(css_dict[msg][0])) / 14)
            y = int(float(css_dict[msg][1]))
            for mid_y in middle_list:
                if y <= int(mid_y[1]) :
                    svg_y = str(mid_y[0])
                    pinglun_str.append(svg_dict[svg_y][x])
                    break
        else:
            pinglun_str.append(msg)
    str_pinglun = ''.join(pinglun_str)
    return str_pinglun




get_message()
