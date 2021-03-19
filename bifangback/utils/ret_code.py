import json
from django.http import HttpResponse


OP_SUCCESS = 0
THROW_EXP = 1000
OP_DB_FAILED = 1001
CHECK_PARAM_FAILED = 1002
FILE_FORMAT_ERR = 1003
NOT_POST = 1004
NOT_GET = 1005
NOT_PERMISSION = 2000

ERR_CODE = {
    0: '操作成功',
    1000: "抛出异常",
    1001: "数据库操作失败",
    1002: "参数检查失败",
    1003: "文件格式有误",
    1004: "非post请求",
    1005: "非get请求",
    2000: "无权限"
}


def build_ret_data(ret_code, data=''):
    return {'code': ret_code, 'message': ERR_CODE[ret_code], 'data': data}


def render_json(dictionary={}):
    response = HttpResponse(json.dumps(dictionary), content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    response["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type"
    response["Access-Control-Allow-Methods"] = "GET, POST, PUT, OPTIONS"
    return response

