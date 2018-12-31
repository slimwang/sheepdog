import traceback
from weiboSpider.weiboSpider import Weibo
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
