import requests
from src.multi_agent.Logger import Logger

logger = Logger("HttpRequest", "console", "INFO").get_logger()


class HttpRequest:
    def __init__(self, request_url, method, headers=None, body=None):
        self.url = request_url
        self.method = method.upper()  # 确保方法为大写
        self.headers = headers or {}
        self.body = body
        self.resp = None
        self.resp_string = None
        self.status_code = None

    def send(self):
        try:
            if self.method == "GET":
                resp = requests.get(self.url, headers=self.headers)
            elif self.method == "POST":
                resp = requests.post(self.url, headers=self.headers, json=self.body)
            elif self.method == "PUT":
                resp = requests.put(self.url, headers=self.headers, json=self.body)
            elif self.method == "DELETE":
                resp = requests.delete(self.url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {self.method}")
            resp.raise_for_status()
            self.resp = resp
            self.status_code = resp.status_code
            self.resp_string = resp.text
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            logger.error(f"Response status code: {http_err.response.status_code}")
            logger.error(f"Response body: {http_err.response.text}")
            raise
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(f"Connection error occurred: {conn_err}")
            raise
        except requests.exceptions.Timeout as timeout_err:
            logger.error(f"Timeout error occurred: {timeout_err}")
            raise
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Request error occurred: {req_err}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise

    def is_ok(self):
        return self.status_code == 200


class HttpRequestBuilder:
    def __init__(self):
        self.req_url = None
        self.req_method = None
        self.req_headers = {}
        self.req_body = None

    def url(self, url):
        """设置请求 URL"""
        self.req_url = url
        return self

    def method(self, method):
        """设置请求方法"""
        self.req_method = method.upper()
        return self

    def header(self, key, value):
        """设置请求头"""
        self.req_headers[key] = value
        return self

    def headers(self, header):
        """设置请求头"""
        self.req_headers = header
        return self

    def body(self, body):
        """设置请求体"""
        self.req_body = body
        return self

    def build(self):
        """生成 HttpRequest 对象"""
        if not self.method:
            raise ValueError("HTTP method must be set")
        return HttpRequest(self.req_url, self.req_method, self.req_headers, self.req_body)

    def toString(self):
        return f"url: {self.req_url}, method: {self.req_method}, headers: {self.req_headers}, body: {self.req_body}"

