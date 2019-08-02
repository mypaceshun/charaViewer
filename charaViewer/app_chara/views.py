from functools import wraps
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from pychara.exceptions import (PyCharaException,
                                LoginFailureException)
from pychara.session import Session

from charaViewer.app_chara.aggregater import (aggregate_apply_list,
                                              filter_apply_list,
                                              get_titles)


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
    status_codes = [
            {'id': 'status_code0','value': '0', 'name': '当選', 'checked': False},
            {'id': 'status_code1','value': '1', 'name': '落選', 'checked': False},
            {'id': 'status_code2','value': '-1', 'name': '抽選待ち', 'checked': False},
            ]
    titles = [ ]
    context = {
            'status_codes': status_codes,
            'titles': titles,
            }
    if request.method == 'GET':
        apply_list = request.session['apply_list']
        title_list = get_titles(apply_list)
        data = aggregate_apply_list(apply_list)
        context['data'] = data
        context['titles'] = title_list_convert_titles(title_list)
        return render(request, 'top.html', context)
    else:  # POST
        postdata = request.POST
        print(postdata)
        filter_dict = get_filter_dict(postdata)

        apply_list = request.session['apply_list']
        title_list = get_titles(apply_list)
        _apply_list = filter_apply_list(apply_list, filter_dict)
        data = aggregate_apply_list(_apply_list, filter_dict)
        context['data'] = data
        context['titles'] = title_list_convert_titles(title_list)
        context = filter_dict_convert_context(filter_dict, context)
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

    filter_dict['reverse'] = False
    if 'reverse' in postdata.keys():
        filter_dict['reverse'] = True

    filter_dict['titles'] = postdata.getlist('titles')

    return filter_dict

def filter_dict_convert_context(filter_dict, context):
    '''
    前回の検索条件をcontextに保存する
    '''
    status_codes = context['status_codes']
    for i in range(len(status_codes)):
        if status_codes[i]['value'] in filter_dict['status_code']:
            status_codes[i]['checked'] = True
    context['status_codes'] = status_codes

    context['reverse'] = filter_dict['reverse']

    title_list = filter_dict['titles']
    titles = context['titles']
    for i in range(len(titles)):
        if titles[i]['value'] in title_list:
            titles[i]['checked'] = True
    context['titles'] = titles

    return context


def title_list_convert_titles(title_list):
    '''
    title(idの上位4桁)が列挙されただけのリストを、
    contextに利用出来る形に整形する
    '''
    titles = []
    for i in range(len(title_list)):
        d = {
                'id': 'title{}'.format(i),
                'value': title_list[i],
                'display': title_list[i],
                'checked': False,
            }
        titles.append(d)
    return titles
