import re
from fontTools.ttLib import TTFont
import requests
from pyquery import PyQuery as pq
import os


headers_user={
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Host': 'www.dianping.com',
    'Referer': 'http://www.dianping.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/535.19',
    'Accept-Encoding': 'gzip',
    'cookie': '_lxsdk_cuid=16d62ea6ca027-0a4910b28fb0df-67e1b3f-100200-16d62ea6ca1c8; _lxsdk=16d62ea6ca027-0a4910b28fb0df-67e1b3f-100200-16d62ea6ca1c8; _hc.v=c882456c-1f19-3cb7-e5a0-1121d5489bdd.1569322594; dper=59ce2667699ea89fbc4655c1e760911f6051307027e8a99460b3570c646358deb627eb975f642a5ecbc0e1b74b3de0882d44ccedf3dc4fdc7ea8611ccf9a482454c63f6b7f22e15bf3220de0ccf496424c9735957c231c6d1b6c9fa1065c1c04; ua=%E7%99%BD%E5%99%AA%E9%9F%B3; ctu=41c1fd0e93c86ea7559dba081079ee30592d2ef5e0aeb74b35665e82babbf339; cy=1; cye=shanghai; s_ViewType=10; aburl=1; ll=7fd06e815b796be3df069dec7836c3df; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; _lxsdk_s=16dd3240dda-ed1-22d-687%7C%7C1'
}

character = [
        '','','1','2','3','4','5','6','7','8',
        '9','0','店','中','美','家','馆','小','车','大',
        '市','公','酒','行','国','品','发','电','金','心',
        '业','商','司','超','生','装','园','场','食','有',
        '新','限','天','面','工','服','海','华','水','房',
        '饰','城','乐','汽','香','部','利','子','老','艺',
        '花','专','东','肉','菜','学','福','饭','人','百',
        '餐','茶','务','通','味','所','山','区','门','药',
        '银','农','龙','停','尚','安','广','鑫','一','容',
        '动','南','具','源','兴','鲜','记','时','机','烤',
        '文','康','信','果','阳','理','锅','宝','达','地',
        '儿','衣','特','产','西','批','坊','州','牛','佳',
        '化','五','米','修','爱','北','养','卖','建','材',
        '三','会','鸡','室','红','站','德','王','光','名',
        '丽','油','院','堂','烧','江','社','合','星','货',
        '型','村','自','科','快','便','日','民','营','和',
        '活','童','明','器','烟','育','宾','精','屋','经',
        '居','庄','石','顺','林','尔','县','手','厅','销',
        '用','好','客','火','雅','盛','体','旅','之','鞋',
        '辣','作','粉','包','楼','校','鱼','平','彩','上',
        '吧','保','永','万','物','教','吃','设','医','正',
        '造','丰','健','点','汤','网','庆','技','斯','洗',
        '料','配','汇','木','缘','加','麻','联','卫','川',
        '泰','色','世','方','寓','风','幼','羊','烫','来',
        '高','厂','兰','阿','贝','皮','全','女','拉','成',
        '云','维','贸','道','术','运','都','口','博','河',
        '瑞','宏','京','际','路','祥','青','镇','厨','培',
        '力','惠','连','马','鸿','钢','训','影','甲','助',
        '窗','布','富','牌','头','四','多','妆','吉','苑',
        '沙','恒','隆','春','干','饼','氏','里','二','管',
        '诚','制','售','嘉','长','轩','杂','副','清','计',
        '黄','讯','太','鸭','号','街','交','与','叉','附',
        '近','层','旁','对','巷','栋','环','省','桥','湖',
        '段','乡','厦','府','铺','内','侧','元','购','前',
        '幢','滨','处','向','座','下','県','凤','港','开',
        '关','景','泉','塘','放','昌','线','湾','政','步',
        '宁','解','白','田','町','溪','十','八','古','双',
        '胜','本','单','同','九','迎','第','台','玉','锦',
        '底','后','七','斜','期','武','岭','松','角','纪',
        '朝','峰','六','振','珠','局','岗','洲','横','边',
        '济','井','办','汉','代','临','弄','团','外','塔',
        '杨','铁','浦','字','年','岛','陵','原','梅','进',
        '荣','友','虹','央','桂','沿','事','津','凯','莲',
        '丁','秀','柳','集','紫','旗','张','谷','的','是',
        '不','了','很','还','个','也','这','我','就','在',
        '以','可','到','错','没','去','过','感','次','要',
        '比','觉','看','得','说','常','真','们','但','最',
        '喜','哈','么','别','位','能','较','境','非','为',
        '欢','然','他','挺','着','价','那','意','种','想',
        '出','员','两','推','做','排','实','分','间','甜',
        '度','起','满','给','热','完','格','荐','喝','等',
        '其','再','几','只','现','朋','候','样','直','而',
        '买','于','般','豆','量','选','奶','打','每','评',
        '少','算','又','因','情','找','些','份','置','适',
        '什','蛋','师','气','你','姐','棒','试','总','定',
        '啊','足','级','整','带','虾','如','态','且','尝',
        '主','话','强','当','更','板','知','己','无','酸',
        '让','入','啦','式','笑','赞','片','酱','差','像',
        '提','队','走','嫩','才','刚','午','接','重','串',
        '回','晚','微','周','值','费','性','桌','拍','跟',
        '块','调','糕'
    ]

def get_review():
    url = 'http://www.dianping.com/member/68702/reviews'
    response = requests.get(url = url, headers = headers_user)
    text = response.content.decode('utf-8')
    pinglun_list = get_pinglun_list(text)
    re_url = r'<link rel="stylesheet" type="text/css" href="(.*?)">'
    css_url = 'http:' + re.findall(re_url,text,re.S)[1]
    ttf_list,name = get_ttf_list(css_url)
    uni_dict = dict(zip(ttf_list,character))
    print(uni_dict)
    for item in pinglun_list:
        pinglun_item = []
        for item1 in item:
            if item1 in uni_dict.keys():
                item1 = uni_dict[item1]
                pinglun_item.append(item1)
            else:
                pinglun_item.append(item1)
        str_pinglun = ''.join(pinglun_item)
        print(str_pinglun)



def get_pinglun_list(text):
    re_result_1 = r'<div class="pic-txt">(.*?)</ul>'
    result_1 = re.search(re_result_1,text,re.S).group(1)
    re_result_2 = r'<div class="mode-tc comm-entry">(.*?)</div>'
    result_2 = re.findall(re_result_2,result_1,re.S)
    result_list = []
    for result in result_2:
        result = re.sub('<svgmtsi class="reviewText">',',',result)
        result = re.sub('<br/>','',result)
        result = re.sub('</svgmtsi>',',',result)
        result_list_1 = [x for x in result.split(',') if x !='']
        result_list_2 =[]
        for item in result_list_1:
            item = item.replace('&#x','uni').replace(';','')
            result_list_2.append(item)
        result_list.append(result_list_2)
    return result_list



def get_ttf_list(css_url):
    css_text = requests.get(url=css_url).text
    re_url = r'reviewText.*?,url(.*?);}'
    woff_url =  re.search(re_url,css_text,re.S).group(1).replace('("','').replace('")','')
    name = woff_url[woff_url.rfind('/')+1:-5]
    woff_url = 'http:' + woff_url
    with open(name + '.woff','wb+') as f :
        f.write(requests.get(url=woff_url).content)
        f.close()
    font = TTFont(name + '.woff')
    uni_list = font['cmap'].tables[0].ttFont.getGlyphOrder()
    print(uni_list)
    return uni_list,name




get_review()








