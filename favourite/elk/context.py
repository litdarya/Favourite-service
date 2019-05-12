from typing import Dict, Any

from tornado.web import RequestHandler

_REQUIRED_COOKIE_KEYS = ['yandexuid', 'cycada']


class Context:
    @staticmethod
    def _get_user_identificators(request_handler: RequestHandler) -> Dict[str, Any]:
        return {
            f'custom_{key}': request_handler.get_cookie(key) for key in _REQUIRED_COOKIE_KEYS
        }

    @staticmethod
    def _get_ua(request_handler: RequestHandler) -> Dict[str, Any]:
        return {
            'User-Agent': request_handler.request.headers['User-Agent'],
        }

    @staticmethod
    def get(request_handler: RequestHandler) -> Dict[str, Any]:
        d1 = Context._get_user_identificators(request_handler)
        d2 = Context._get_ua(request_handler)
        d1.update(d2)
        return d2
