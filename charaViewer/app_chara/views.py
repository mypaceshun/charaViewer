import datetime
from django.shortcuts import render, redirect
from pychara.exceptions import (PyCharaException,
                                LoginFailureException)
from pychara.session import Session

from charaViewer.aggregater import apply_from_type


def top_view(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'top.html', context)
    else:  # POST
        postdata = request.POST
        username = postdata['username']
        password = postdata['password']
        pages = 5
        s = Session()
        try:
            s.login(username, password)
            apply_list = []
            for i in range(1, pages + 1):
                _apply_list = s.fetch_apply_list(page=i)
                # datetimeのままだとセッションに保存できないのでstrに変換する
                for d in _apply_list:
                    d['date'] = d['date'].strftime('%Y%m%d')
                    apply_list.append(d)
            request.session['apply_list'] = apply_list
        except LoginFailureException as err:
            context['error'] = 'ログインに失敗しました...'
            return render(request, 'top.html', context)
        except PyCharaException as err:
            context['error'] = '情報の取得に失敗しました...'
            return render(request, 'top.html', context)
        return redirect('result')


def result_view(request):
    context = {}
    apply_list = request.session['apply_list']
    _apply_list = apply_from_type(apply_list)
    print(_apply_list)
    data = [_apply_list[key] for key in _apply_list]
    context['data'] = data
    print(data)
    return render(request, 'result.html', context)
