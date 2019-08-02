from functools import wraps
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from pychara.exceptions import (PyCharaException,
                                LoginFailureException)
from pychara.session import Session

from charaViewer.app_chara.aggregater import (aggregate_apply_list,
                                              filter_apply_list)


def require_login(func):
    @wraps(func)
    def _require_login(request, *args, **kwargs):
        username = request.session.get("username", None)
        if username is None:
            return redirect('login')
        return func(request, *args, **kwargs)
    return _require_login


@require_login
@require_http_methods(['GET', 'POST'])
def top_view(request):
    context = {}
    if request.method == 'GET':
        apply_list = request.session['apply_list']
        data = aggregate_apply_list(apply_list)
        context['data'] = data
        return render(request, 'top.html', context)
    else:  # POST
        postdata = request.POST
        filter_dict = get_filter_dict(postdata)
        apply_list = request.session['apply_list']
        _apply_list = filter_apply_list(apply_list, filter_dict)
        data = aggregate_apply_list(_apply_list)
        context['data'] = data
        return render(request, 'top.html', context)


def login_view(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'login.html', context)
    else:  # POST
        postdata = request.POST
        username = postdata['username']
        password = postdata['password']
        pages = int(postdata['page'])
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
            return render(request, 'login.html', context)
        except PyCharaException as err:
            context['error'] = '情報の取得に失敗しました...'
            return render(request, 'login.html', context)
        request.session['username'] = username
        return redirect('top')


def get_filter_dict(postdata):
    filter_dict = {}
    filter_dict['status_code'] = postdata.getlist('status_code')
    return filter_dict
