'''
pycharaのfetch_apply_list()やfetch_purchase_list()で取得してきたリストを
それぞれ任意のルールで集計する
'''


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
    return r


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
