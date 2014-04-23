# -*- coding: utf-8 -*-

from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException


def QnAExceptionHandler(exc):
    # REST framework's default exception handler
    response = exception_handler(exc)

    if response is not None:
        response.data['status_code'] = response.status_code

    return response


class NotFound(APIException):

    status_code = 404
    default_detail = 'Not found.'

    def __init__(self, detail):
        self.detail = detail
