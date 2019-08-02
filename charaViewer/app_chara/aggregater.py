# apply_listをこねくり回す関数たち

import re
import datetime


def aggregate_apply_list(apply_list):
    '''
    apply_list = [{'date': datetime,
                  'id': id,
                  'name': 1/1(月)XX XXXX 第2部【XXXX】,
                  'one_money': 1028,
                  'num': 3,
                  'total_money': 3084,
                  'status': 当選
                  'status_code': 0,
                  }, ...]
    apply_list をstatus_codeごとに集計
    '''

    r = {}

    for d in apply_list:
        key = '{}{}'.format(str(d['id']), str(d['status_code']))
        if key in r.keys():
            r[key]['num'] = int(r[key]['num']) + int(d['num'])
            r[key]['total_money'] = int(
                r[key]['one_money']) * int(r[key]['num'])
        else:
            r[key] = d
    # リストに直す
    r = [r[key] for key in r]
    r = genarate_bu(r)
    r = replace_date(r)
    r = sort_apply_list(r)
    return r


def genarate_bu(apply_list):
    '''
    apply_listのname属性から部数を判別する
    '''
    pattern = '.*第(\d)部.*'
    repattern = re.compile(pattern)
    new_apply_list = []
    for d in apply_list:
        result = repattern.match(d['name'])
        if result is None:
            print('{} is not found bu'.format(d['name']))
        else:
            d['bu'] = int(result.group(1))
            new_apply_list.append(d)
    return new_apply_list


def replace_date(apply_list):
    '''
    apply_listに含まれているdateの値は申込み日時になっているが、
    開催日時が入っていたほうが嬉しいので置き換える。

    nameの値の先頭から数字かスラッシュのみを抽出したものを日付とする
    開催日は申込み日時以降であると仮定し、開催年を判別する
    '''

    pattern = '[\d/]*'
    repattern = re.compile(pattern)

    format = '%m/%d'

    new_apply_list = []
    for d in apply_list:
        result = repattern.match(d['name'])
        if result is None:
            print('{} is not found bu'.format(d['name']))
        else:
            apply_date = datetime.datetime.strptime(d['date'], "%Y%m%d")  # yyyymmdd
            date_str = result.group()
            date = datetime.datetime.strptime(date_str, format)
            date = date.replace(year=apply_date.year)
            if date < apply_date:
                date = date.replace(year=apply_date.year+1)

            d['date'] = date
            d['apply_date'] = apply_date
            new_apply_list.append(d)
    return new_apply_list


def sort_apply_list(apply_list):
    '''
    apply_listをdateとbuをキーにソートする
    '''
    def key(d):
        format = "%Y%m%d"
        date_str = d['date'].strftime(format)
        bu_str = str(d['bu'])
        return '{}{}'.format(date_str, bu_str)

    sorted_list = sorted(apply_list, key=key)
    return sorted_list


def filter_apply_list(apply_list, filter_dict):
    status_code = filter_dict.get("status_code", None)
    if status_code is None \
       or len(status_code) == 0:
        return apply_list

    status_code = [int(s) for s in status_code]

    r = []
    for d in apply_list:
        if d['status_code'] in status_code:
            r.append(d)
    return r
