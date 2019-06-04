'''
pycharaのfetch_apply_list()やfetch_purchase_list()で取得してきたリストを
それぞれ任意のルールで集計する
'''


def apply_from_type(apply_list):
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
    apply_list をstatus_codeごとに分類
    '''

    r = {}

    for d in apply_list:
        key = '{}{}'.format(d['id'], d['status_code'])
        if key in r.keys():
            r[key]['num'] = int(r[key]['num']) + int(d['num'])
            r[key]['total_money'] = int(r[key]['one_money']) * int(r[key]['num'])
        else:
            r[key] = d
    return r
