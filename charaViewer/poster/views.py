from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.http.response import JsonResponse
from pychara.exceptions import (PyCharaException,
                                LoginFailureException)
from pychara.session import Session
from charaViewer.poster import APPTITLE
from charaViewer.api.views import find_hidden
import requests
from bs4 import BeautifulSoup

MAX_ITEMS = 10


@require_http_methods(['GET', 'POST'])
def top_view(request):
    context = {'title': APPTITLE,
                'maxItems': range(MAX_ITEMS)}
    if request.method == 'GET':
        date_api_url = request.build_absolute_uri(reverse('api_date'))
        res = requests.get(date_api_url)
        context['data'] = res.json()['data']
        return render(request, 'poster/top.html', context)
    else:
        postdata = request.POST
        num = postdata['num']
        username = postdata['username']
        password = postdata['password']
        items = [{'date': postdata['date-{}'.format(i)],
                  'name': postdata['name-{}'.format(i)],
                  'num': postdata['num-{}'.format(i)]} for i in range(MAX_ITEMS) if 'num-{}'.format(i) in postdata.keys()]
        try:
            result = do_reserve(username, password, items)
        except Exception as error:
            print(error)
            context['error'] = "申込みに失敗しました..."
        return render(request, 'poster/result.html', context)


def do_reserve(username, password, items):
    reserve_url = 'https://akb48.chara-ani.com/hall1/akbreserve.aspx'
    res = requests.get(reserve_url)
    cookies = res.cookies

    # 同じ日付のものはまとめて申し込む
    reserve_data = {}
    for item in items:
        if item['date'] in reserve_data.keys():
            reserve_data[item['date']].append({'name': item['name'], 'num': item['num']})
        else:
            reserve_data[item['date']] = [{'name': item['name'], 'num': item['num']}]
    print(reserve_data)

    postdata = find_hidden(res.text)

    date_history = 0
    for date in reserve_data:
        if date == '0':
            continue
        print(date)
        # 最初に対象の日付のページに移動
        date_history = date
        postdata['ddlEvents'] = str(date)
        postdata['btnDisp.x'] = str(114)
        postdata['btnDisp.y'] = str(18)
        res = requests.post(reserve_url, cookies=cookies, data=postdata)
        cookies = res.cookies
        postdata = find_hidden(res.text)
        
        # 指定のアイテムを選択する(postdataに追加)
        soup = BeautifulSoup(res.text, 'html.parser')
        select_els = soup.find_all('select')
        for select_el in select_els:
            name = select_el.get('name')
            postdata[name] = ""

        for item in reserve_data[date]:
            postdata[item['name']] = str(item['num'])

    # 最後に確認ボタンを押す
    postdata['ddlEvents'] = str(1)
    postdata['ibtnConfirm.x'] = str(27)
    postdata['ibtnConfirm.y'] = str(16)
    res = requests.post(reserve_url, cookies=cookies, data=postdata)
    cookies = res.cookies

    # ログイン
    postdata = find_hidden(res.text)
    postdata['txID'] = password
    # postdata['TboxAksMemberID'] = password
    postdata['txPASSWORD'] = username
    # postdata['TboxAksPass'] = username
    postdata['btnLogin.x'] = str(125)
    postdata['btnLogin.y'] = str(6)
    res = requests.post(reserve_url, cookies=cookies, data=postdata)
    print(res.text)
