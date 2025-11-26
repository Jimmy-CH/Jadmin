
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class CustomPagePagination(PageNumberPagination):
    page_query_param = 'pageNum'      # 前端传 pageNum=1
    page_size_query_param = 'pageSize'  # 前端传 pageSize=10
    max_page_size = 100               # 最大每页数量
    page_size = 10                    # 默认每页数量（可被 pageSize 覆盖）

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('code', '200'),
            ('data', {
                'list': data,
                'total': self.page.paginator.count
            }),
            ('msg', 'OK')
        ]))
