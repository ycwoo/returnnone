#!/usr/bin/env python
# coding=utf-8

from flask import url_for, render_template, request, redirect

from app import app
from form import TextQueryInput
from model import get_google_result, get_zhihu_result


@app.route('/', methods=['GET', 'POST'])
def index():
    index_form = TextQueryInput(request.form)
    if index_form.validate_on_submit():
        return redirect(url_for('search_result', keyword=index_form.keyword.data, page_num=1))
    return render_template('index.html', form=index_form)


@app.route('/s/<keyword>/<int:page_num>', methods=['GET', 'POST'])
def search_result(keyword, page_num):
    g = get_google_result(keyword, page_num)
    query_form = TextQueryInput(request.form)
    if query_form.validate_on_submit():
        return redirect(url_for('search_result', keyword=query_form.keyword.data, page_num=1))
    query_form.keyword.data = keyword
    return render_template('result.html',
                           keyword=keyword,
                           result_num=g.get('total'),
                           result_time=g.get('took'),
                           google_results=g.get('item'),
                           zhihu_results=get_zhihu_result(keyword),
                           current_page=page_num,
                           query_form=query_form)


@app.route('/killIE')
def kill_ie():
    return render_template('killIE.html')
