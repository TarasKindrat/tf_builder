"""Module contains common utils for microservice"""
from functools import wraps

from flask import make_response

from core.application.helpers.exceptions import APIExceptionHandler


def make_error_response(message: str, code: int):
    """
    Generates error json
    Args:
        message: str: error message
        code: int: http error code

    Returns: flask response object

    """
    resp = make_response(message, code)
    resp.headers['Content-Type'] = "application/json"
    return resp


def make_api_response(*args):
    def wrapper_func(fn):
        @wraps(fn)
        def wrapped_func(*args, **kwargs):
            error_catcher = APIExceptionHandler()
            with error_catcher:
                res = fn(*args, **kwargs)
            if error_catcher.error:
                err_msg = error_catcher.error[0].format(error_catcher.error[3])
                return make_error_response(err_msg, error_catcher.error[1])
            else:
                return res
        return wrapped_func
    return wrapper_func
