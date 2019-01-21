import os
import time
from spider import Spider
from analyser import Analyser
from db import DB
from db import Person
from db import Weibo
from sms import send_sms


def main():
    """
    user_id: 用户ID, 查询方法看weiboSpider里的README
    filter: 值为1时,爬取所有原创微博
    my_cookie: 设置cookie值
    """
    user_id = int(os.environ.get('USER_ID')) or 00000000
    filter = 1
    my_cookie = os.environ.get('COOKIE') or "your_cookie"  # noqa: ignore=E501

    # 爬取数据
    if not os.path.isfile('weibo.db'):
        spider = Spider(user_id, filter)
        spider.set_cookie(my_cookie)
        spider.start()
    # 分析数据
    person = Person.get(Person.user_id == user_id)
    if not person.mean:
        analyser = Analyser(user_id)
        analyser.start()

    # 初始化
    spider = Spider(user_id, filter)
    spider.set_cookie(my_cookie)

    # 处理新微博
    def process_newest_weibo():
        """
        设置定时器: 每隔一段时间调用自身
        获取新微博: 先爬取 person 的最新一条微博, 若其已存在与数据库中, 则等待下次执行.
                                             若不存在, 则分析其情绪值, 并存入数据库中, 同时更新数据库中的统计数据
        分析情绪值: 若情绪正常, 则等待, 否则, 发送短信
        """

        # 获取新微博
        new_weibo = spider.get_newest_weibo()
        query = Weibo.select().where(Weibo.weibo_content ==
                                     new_weibo["weibo_content"])
        # 对新发出的微博进行处理
        if not query.exists():
            print('======发现新微博======')
            analyser = Analyser(user_id)
            sentiment_value = analyser.get_sentiment_value(
                new_weibo["weibo_content"])
            # 数据库操作
            db = DB()
            db.person = person
            weibo = db.store_weibo(**new_weibo)
            db.store_sentiment(weibo, sentiment_value)
            analyser.calculate()
            # 更新数据库后, 均值和方差变了, 需要再次更新
            MEAN = Person.get(Person.user_id == user_id).mean
            SD = Person.get(Person.user_id == user_id).std
            if sentiment_value not in range(MEAN - SD // 2, MEAN + SD // 2):
                message = '[{person_name}]发了一条[情绪值]为 {sentiment_value} 的微博, 内容为: {content}'.format(
                    person_name=person.username,
                    sentiment_value=sentiment_value,
                    content=new_weibo['weibo_content'],
                )
                print(message)
                print('============')
                # 发送短信
                send_sms(message)
        else:
            # 更新点赞数 转发数 和 评论数
            weibo = query[0]
            if (
                weibo.up_num != new_weibo['up_num'] or
                weibo.retweet_num != new_weibo['retweet_num'] or
                weibo.comment_num != new_weibo['comment_num']
            ):
                print('微博状态发生变化, 正在更新数据库...')
                db = DB()
                db.person = person
                weibo.up_num = new_weibo['up_num']
                weibo.retweet_num = new_weibo['retweet_num']
                weibo.comment_num = new_weibo['comment_num']
                weibo.save()
                print('数据库更新完毕')

            print('======无新微博, 当前输出的是最后一条微博======')

    # 循环爬取最新微博, 并处理
    while True:
        process_newest_weibo()
        time.sleep(300)


if __name__ == '__main__':
    main()
