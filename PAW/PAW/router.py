# router.py
class Router:
    routes_get = {}
    routes_post = {}

    @classmethod
    def route(cls, path, methods=None):
        def wrapper(func):
            if methods is None or 'GET' in methods:
                cls.routes_get[path] = func
            if methods is None or 'POST' in methods:
                cls.routes_post[path] = func
            return func
        return wrapper

    @classmethod
    def get_handler(cls, path):
        return cls.routes_get.get(path, cls.default_handler)

    @classmethod
    def post_handler(cls, path):
        return cls.routes_post.get(path, cls.default_handler)

    @staticmethod
    def default_handler(*args, **kwargs):
        response = "404 Not Found"
        status_code = 404
        return response, status_code
    
