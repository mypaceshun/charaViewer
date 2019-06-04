import datetime
import pytest
from . import get_apply_list
from aggregater import apply_from_type

class TestAggregateRecordsFromType():
    def test_aggregate_records_from_type(self):
        apply_list = get_apply_list()
        result_dict = apply_from_type(apply_list)
        expect_dict = {'A123456780': {
                           'date': datetime.datetime(2019, 5, 28, 0, 0),
                           'id': 'A12345678',
                           'name': '1/1(月)XX XXXX 第1部【XXXX】',
                           'one_money': 1028,
                           'num': 9,
                           'total_money': 1028 * 9,
                           'status': '当選',
                           'status_code': 0 },
                       'A123456781': {
                           'date': datetime.datetime(2019, 5, 28, 0, 0),
                           'id': 'A12345678',
                           'name': '1/1(月)XX XXXX 第1部【XXXX】',
                           'one_money': 1028,
                           'num': 3,
                           'total_money': 3084,
                           'status': '落選',
                           'status_code': 1 },
                       'A123456782': {
                           'date': datetime.datetime(2019, 5, 28, 0, 0),
                           'id': 'A12345678',
                           'name': '1/1(月)XX XXXX 第1部【XXXX】',
                           'one_money': 1028,
                           'num': 3,
                           'total_money': 3084,
                           'status': '抽選中',
                           'status_code': 2 },
                       'A123456790': {
                           'date': datetime.datetime(2019, 5, 28, 0, 0),
                           'id': 'A12345679',
                           'name': '1/1(月)XX XXXX 第2部【XXXX】',
                           'one_money': 1028,
                           'num': 3,
                           'total_money': 3084,
                           'status': '当選',
                           'status_code': 0 },
                       'A123456800': {
                           'date': datetime.datetime(2019, 5, 28, 0, 0),
                           'id': 'A12345680',
                           'name': '想定と異なるテキスト',
                           'one_money': 1028,
                           'num': 3,
                           'total_money': 3084,
                           'status': '当選',
                           'status_code': 0 },}
                           
        assert isinstance(result_dict, dict)
        assert result_dict == expect_dict
