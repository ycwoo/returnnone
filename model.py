#!/usr/bin/env python
# coding=utf-8

import requests
from bs4 import BeautifulSoup
from app import app
from utils.langconv import *


def get_google_result(keyword, pn):
    params = {'q': keyword,
              "start": (pn - 1) * 10,
              'gws_rd': "ssl"}
    html = requests.get(app.config['GOOGLE_SEARCH_URL'],
                        params=params,
                        timeout=10,
                        headers=app.config['USER_AGENT']).content.decode('utf-8', 'ignore')
    soup = BeautifulSoup(html, "lxml")
    find_result_sum_re = re.compile(r'<div\s*id="resultStats">\D*([\d,]*).*<nobr>')
    find_result_time_re = re.compile(r'<nobr>\D*([\d.]*)\D*</nobr>')
    result_info = soup.find("div", id="resultStats")
    result_sum = find_result_sum_re.findall(str(result_info))[0]
    result_time = find_result_time_re.findall(str(result_info))[0]
    f = soup.find_all("div", class_="rc")
    find_abstract_re = re.compile(r'<span\s+class="st">(.+?)</span></?div')
    find_cite_re = re.compile(r'<cite\s+class="_Rm.*">(.+?)</cite>')
    l = [{'title': Converter('zh-hans').convert(b.h3.get_text()),
          'link': b.h3.a.get('href'),
          'cite': find_cite_re.findall(str(b))[0].decode('utf-8', 'ignore'),
          'abstract': Converter('zh-hans').convert(find_abstract_re.findall(str(b))[0].decode('utf-8', 'ignore'))} for b
         in f if
         find_abstract_re.findall(str(b))]
    return {
        'total': result_sum,
        'took': result_time,
        'item': l
    }


def get_zhihu_result(keyword):
    zhihu_result = []
    p = {
        'query': keyword,
        'ie': 'utf-8'
    }
    try:
        html = requests.get(app.config['ZHIHU_SEARCH_URL'],
                            params=p,
                            timeout=5,
                            headers=app.config['USER_AGENT']).content.decode('utf-8', 'ignore')
        r = BeautifulSoup(html, "lxml").find_all('div', class_='result-about-list')[:6]
        zhihu_result = [{'title': x.a.text,
                         'link': x.h4.a.get('href'),
                         'thumb': x.find('span', class_='about-img').img.get('src')
                         if x.find('span', class_='about-img') is not None
                         else app.config['ZHIHU_DEFAULT_THUMBNAIL'],
                         'author': u'知乎用户' if x.p.a is None else x.p.a.text,
                         'like': x.find('span', class_='count').text} for x in r]
    except requests.ConnectionError, requests.ConnectTimeout:
        pass
    return zhihu_result
