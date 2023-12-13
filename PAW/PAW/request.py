from urllib.parse import urlparse, parse_qs

class Request:
    def __init__(self, http_handler, session_id):
        self.handler = http_handler
        self.path = self.handler.path
        self.method = self.handler.command
        self.headers = self.handler.headers
        self.query_params = self._parse_query_params()
        self.body = self._parse_body()

    def _parse_query_params(self):
        query_params = urlparse(self.path).query
        return parse_qs(query_params)

    def _parse_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.handler.rfile.read(content_length).decode('utf-8')
        return body

    # Add any other methods or properties you need

    def get_cookie(self, cookie_name):
        cookies = self.headers.get('Cookie', '')
        cookie_dict = {item.split('=')[0].strip(): item.split('=')[1].strip() for item in cookies.split(';')}
        return cookie_dict.get(cookie_name, None)
