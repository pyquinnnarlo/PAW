class Router:
    routes = {}

    @classmethod
    def route(cls, path):
        def wrapper(func):
            cls.routes[path] = func
            return func
        return wrapper

    @classmethod
    def get_handler(cls, path):
        return cls.routes.get(path, cls.default_handler)

    @staticmethod
    def default_handler(*args, **kwargs):
        response = "404 Not Found"
        status_code = 404
        return response, status_code
