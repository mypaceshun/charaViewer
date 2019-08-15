from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.http.response import JsonResponse
import requests
from bs4 import BeautifulSoup
from pychara.session import Session


RESERVE_URL = 'https://akb48.chara-ani.com/hall1/akbreserve.aspx'


@require_http_methods(['GET'])
def date_view(request):

    res = requests.get(RESERVE_URL)

    if res.status_code != 200:
        data = {'status_code': res.status_code,
                'error_message': res.text}
        return JsonResponse(data)

    soup = BeautifulSoup(res.text, 'html.parser')
    event_els = soup.find(attrs={'id': 'ddlEvents'})
    option_els = event_els.findAll('option')
    data = []
    for option in option_els:
        value = option.get('value')
        text = option.text
        data.append({'text': text, 'value': value})

    return JsonResponse({'data': data})


@require_http_methods(['GET'])
def date_items_view(request, value):
    res = requests.get(RESERVE_URL)

    if res.status_code != 200:
        data = {'status_code': res.status_code,
                'error_message': res.text}
        return JsonResponse(data)

    # valueのページへ遷移
    cookies = res.cookies
    postdata = find_hidden(res.text)
    postdata['ddlEvents'] = str(value)
    postdata['btnDisp.x'] = str(114)
    postdata['btnDisp.y'] = str(18)
    res = requests.post(RESERVE_URL, cookies=cookies, data=postdata)
    
    if res.status_code != 200:
        data = {'status_code': res.status_code,
                'error_message': res.text}
        return JsonResponse(data)

    soup = BeautifulSoup(res.text, 'html.parser')
    even_els = soup.findAll(attrs={'class': 'even'})
    data = []
    for even in even_els:
        text = even.findAll('span')[0].text
        options = [i.text for i in even.findAll('option')]
        num = 0
        if len(options) != 0:
            num = max(options)
        select_el = even.find('select')
        if select_el is None:
            data.append({'text': text, 'name': None, 'num': num, 'soldout': True})
        else:
            name = select_el.get('name')
            data.append({'text': text, 'name': name, 'num': num, 'soldout': False})

    return JsonResponse({'data': data})


def find_hidden(html):
    soup = BeautifulSoup(html, 'html.parser')
    input_els = soup.find_all('input')
    hidden_data = {}
    for input_el in input_els:
        _type = input_el.get('type')
        if _type in "hidden":
            hidden_data[input_el.get("name")] = input_el.get("value")

    return hidden_data
