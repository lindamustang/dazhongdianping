# 关于大众点评的爬虫

## 1.dianpingsrapy（使用scrapy框架）
    用于爬取大众点评店铺分类页面的一些内容，仅作本人测试使用。经测试，随着爬取次数的增加，scrapy框架会渐渐失效，原因不明。之前
    的爬取结果都在csv文件里。在控制台输入scrapy crawl dianpingsrapy  便可执行。
## 2.dianpinglun1和dianpinglun2
    用于爬取某店铺的所有评论信息，店铺名（shop_id），页码(page)可自行设置（后续考虑自动获取）。经观察，大众点评点评评论有两种页
    面写法，所以两个代码互为替换。两个代码的区别是是否存在middle_list
## 3.dish_list
    用于爬取店铺招牌菜信息，只需替换str()中的shop_id即可
## 4.user_reviews
     用于爬取某个用户所有评论信息，暂无翻页设置
## 5.cookie
     cookie自行登录替换，替换完之后每个代码即可直接运行
   
  


