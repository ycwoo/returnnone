#!/usr/bin/env python
# coding=utf-8


class Config(object):
    USER_AGENT = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Accept-Encoding': "gzip,deflate,sdch",
        'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
    ZHIHU_DEFAULT_THUMBNAIL = 'http://img02.sogoucdn.com/v2/thumb/resize/w/100/h/100/ir/3/zi/on/iw/75/ih/75/crop/x/0/y/0/w/100/h/100?t=2&appid=200648&url=http%3A%2F%2Fpic1.zhimg.com%2Fe82bab09c_l.jpg&referer=http://www.zhihu.com/topic/19836490'
    GOOGLE_SEARCH_URL = 'https://www.google.com.hk/search'
    ZHIHU_SEARCH_URL = 'http://zhihu.sogou.com/zhihu'
    SECRET_KEY = 'asdghtyu'


class OnlineConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'online': OnlineConfig,
    'development': DevelopmentConfig
}
