# 对新浪微博用户进行情感分析
本爬虫可以一次性爬取用户的所有原创微博, 并计算每一条微博的情绪值, 由此得到样本的均值 MEAN, 方差 SD, [MEAN - SD, MEAN + SD] 即可看作该用户的正常情绪波动范围

再定期(默认间隔五分钟, 可在 app.py 中设置)爬取最新微博, 对其内容计算情绪值, 若该值没有落在上述范围内, 则可看作用户出现极端情绪, 表明该用户正处在极度兴奋或极度悲伤的状态, 会自动向预设手机号发送短信通知

## 文件结构

### weiboSpider/
爬虫类继承自[dataabc/weiboSpider](https://github.com/dataabc/weiboSpider)
所以在克隆本项目时, 要执行`git clone --recursive [address]`, 将子模块里的代码也克隆下来
子模块中将数据写入了txt里, 这会对数据分析造成困难,因此要在spider.py中将微博内容写入数据库
### spider.py
本项目使用的爬虫主要逻辑都在这里, 继承自 weiboSpider/weiboSpider.py 里的 Weibo 类, 重写了里面的一些方法, 并新增了方法
### analyser.py
分析器, 用来对微博内容进行情感分析
### db.py
所有对数据库的操作放在这里, 默认使用 sqlite3 数据库
### sms.py
使用 twilio 发送短信
### app.py
主要代码, 在这里设置 user_id, filter, cookie 等值

## 使用方法
### 1. 克隆代码
`git clone --recursive [address]`
### 2. 创建环境
`cd sheepdog`

`pipenv install`
### 3. 在 app.py 中设置 user_id, filter, my_cookie

获得这三个值的方法, 可以去看 `weiboSpider/`中的 README

```python
"""
user_id: 用户ID, 查询方法看weiboSpider里的README
filter: 值为1时,爬取所有原创微博
my_cookie: 设置cookie值
"""
```
### 4. 配置 sms.py
先去[twilio官网](www.twilio.com)注册试用账号, 进入控制台, 然后选择一个 phone number, 再找到自己的 ACCOUNT SID, AUTH TOKEN, 填入 `sms.py`
这里的 `from_` 填的是你从 twilio 里获得的电话号码, 带区号, +1 是美国, +86 是中国, `from_='+152011112222'`, `to` 填入你用来接收短信的手机号.

### 5. 运行
`python app.py`

### 6. (可选)在云服务器上运行
#### 1). **nohup + & 这种后台运行的方式并不适用**
因为 python 的 print 会向 buffer 里写数据, 这些数据并不会被输出到 nohup.out 文件中

#### 2). 用 screen 的方式:
`cd sheepdog`

`screen`

`python app.py`

`[ctrl] + [A] + [D]`返回
