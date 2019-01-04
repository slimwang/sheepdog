import traceback
import requests
import sys
import re
from weiboSpider.weiboSpider import Weibo
from lxml import etree
from db import DB


class Spider(Weibo):
    def __init__(self, user_id, filter):
        super(Spider, self).__init__(user_id, filter)
        self.db = DB()

    def write_to_db(self):
        try:
            if self.filter:
                self.is_original = True
            else:
                self.is_original = False

            # 写入用户信息
            self.db.store_person(
                username=self.username,
                user_id=self.user_id,
                weibo_num=self.weibo_num,
                following=self.following,
                followers=self.followers,
            )

            # 写入微博信息
            for i in range(1, self.weibo_num2 + 1):
                self.db.store_weibo(
                    weibo_content=self.weibo_content[i-1],
                    weibo_place=self.weibo_place[i-1],
                    publish_time=self.publish_time[i-1],
                    up_num=self.up_num[i-1],
                    retweet_num=self.retweet_num[i-1],
                    comment_num=self.comment_num[i-1],
                    publish_tool=self.publish_tool[i-1],
                    is_original=self.is_original,
                )
            print(u"微博写入数据库完毕")
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 爬取最新微博
    def get_newest_weibo(self):
        # 初始化
        self.weibo_content = []
        self.weibo_place = []
        self.publish_time = []
        self.publish_tool = []
        self.up_num = []
        self.retweet_num = []
        self.comment_num = []

        page = 1
        url2 = "https://weibo.cn/u/%d?filter=%d&page=%d" % (
            self.user_id, self.filter, page)
        html2 = requests.get(url2, cookies=self.cookie).content
        selector2 = etree.HTML(html2)
        info = selector2.xpath("//div[@class='c']")
        self.get_weibo_content(info[0])
        # 微博位置
        self.get_weibo_place(info[0])

        # 微博发布时间
        self.get_publish_time(info[0])

        # 微博发布工具
        self.get_publish_tool(info[0])

        str_footer = info[0].xpath("div")[-1]
        str_footer = str_footer.xpath("string(.)").encode(
            sys.stdout.encoding, "ignore").decode(sys.stdout.encoding)
        str_footer = str_footer[str_footer.rfind(u'赞'):]
        pattern = r"\d+\.?\d*"
        guid = re.findall(pattern, str_footer, re.M)

        # 点赞数
        up_num = int(guid[0])
        self.up_num.append(up_num)
        print(u"点赞数: " + str(up_num))

        # 转发数
        retweet_num = int(guid[1])
        self.retweet_num.append(retweet_num)
        print(u"转发数: " + str(retweet_num))

        # 评论数
        comment_num = int(guid[2])
        self.comment_num.append(comment_num)
        new_weibo = {
            "weibo_content": self.weibo_content[0],
            "weibo_place": self.weibo_place[0],
            "publish_time": self.publish_time[0],
            "publish_tool": self.publish_tool[0],
            "up_num": self.up_num[0],
            "retweet_num": self.retweet_num[0],
            "comment_num": self.comment_num[0],
            "is_original": self.filter,
        }
        return new_weibo

    # 运行爬虫
    def start(self):
        try:
            self.get_username()
            self.get_user_info()
            self.get_weibo_info()
            self.write_to_db()
            print(u"信息抓取完毕")
        except Exception as e:
            print("Error: ", e)
