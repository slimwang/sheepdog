import pandas as pd
from snownlp import SnowNLP
from db import DB
from db import Weibo


class Analyser:
    """
    用于情绪值的分析和计算

    需要接收一个 user_id 参数来确定是对哪个 Person 进行分析
    且默认是对所有原创微博进行分析
    """

    def __init__(self, user_id):
        self.db = DB()
        self.person = self.db.get_person(user_id)

    def get_sentiment_value(self, content):
        sentiment = SnowNLP(content).sentiments
        sentiment_value = round(sentiment * 100)
        return sentiment_value

    def analyse_sentiment_value(self):
        """ 情绪值的计算方法

        sentiment: 该内容为正极性的概率
        sentiment_value: 取概率的前两位小数作为情绪值,百分制
        """
        query = Weibo.select().where(Weibo.person == self.person and Weibo.is_original)
        for weibo in query:
            sentiment_value = self.get_sentiment_value(weibo.weibo_content)
            self.db.store_sentiment(weibo, sentiment_value)

    def calculate(self):
        query = Weibo.select().where(Weibo.person == self.person and Weibo.is_original)
        sentiments = [w.sentiment for w in query]
        Q1 = int(pd.Series(sentiments).quantile(.25))
        Q2 = int(pd.Series(sentiments).quantile(.5))
        Q3 = int(pd.Series(sentiments).quantile(.75))
        mean = pd.Series(sentiments).mean()
        std = pd.Series(sentiments).std()
        self.db.store_Q1_Q2_Q3(self.person, Q1, Q2, Q3)
        self.db.store_mean_and_std(self.person, mean, std)

    def start(self):
        self.analyse_sentiment_value()
        self.calculate()
        print('分析完毕')
