
from rest_framework.response import Response


def custom_response(code: str, message: str = "success", data=None, http_status=200):
    """
    统一 API 响应格式
    :param code: 业务状态码（字符串），如 "200", "40001"
    :param message: 提示信息
    :param data: 返回数据，默认为 {}
    :param http_status: HTTP 状态码（用于 Response status）
    :return: DRF Response
    """
    if data is None:
        data = {}

    return Response(
        data={
            "code": str(code),
            "msg": message,
            "data": data
        },
        status=http_status
    )

