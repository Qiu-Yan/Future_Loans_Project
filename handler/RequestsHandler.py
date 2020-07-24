# coding=gbk

import requests
"""第三方库 需pip install requests"""
from handler.LogHandler import log
from handler.ConfigHandler import config


class HttpSessionHandler:
    """自动记录cookies"""
    def __init__(self):
        self.session = requests.Session()

    def get(self, url, params=None, **kwargs):
        """get请求"""
        try:
            response = self.session.get(url=url, params=params, **kwargs)
        except Exception as e:
            log.error(e)
        else:
            return response

    def post(self, url, data=None, json=None, **kwargs):
        """post请求"""
        try:
            response = self.session.post(url=url, data=data, json=json, **kwargs)
        except Exception as e:
            log.error(e)
        else:
            return response

    def request(self, method, url, **kwargs):
        """其他请求方法"""
        try:
            response = self.session.request(method=method, url=url, **kwargs)
        except Exception as e:
            log.error(e)
        else:
            return response

    def get_json(self, method, url, **kwargs):
        """访问接口，获取json内容， content-type: application/json"""
        try:
            res = self.request(method, url, **kwargs)
            json_dic = res.json()
        except Exception as e:
            log.error(e)
        else:
            return json_dic

    # def get_text(self, method, url, **kwargs):
    #     """获取文本内容， text/html, text/xml, text/plain等"""
    #     try:
    #         res = self.request(method, url, **kwargs)
    #     except Exception as e:
    #         log.error(e)
    #     else:
    #         return res.text
    #
    # def get_content(self, method, url, **kwargs):
    #     """获取二进制格式内容， image/gif, image/jpeg, image/png等"""
    #     try:
    #         res = self.request(method, url, **kwargs)
    #     except Exception as e:
    #         log.error(e)
    #     else:
    #         return res.content


class HttpRequestsHandler:
    """无需记录cookies的请求"""

    def get(self, url, params=None, **kwargs):
        """get请求"""
        try:
            response = requests.get(url=url, params=params, **kwargs)
        except Exception as e:
            log.error(e)
        else:
            return response

    def post(self, url, data=None, json=None, **kwargs):
        """post请求"""
        try:
            response = requests.post(url=url, data=data, json=json, **kwargs)
        except Exception as e:
            log.error(e)
        else:
            return response

    def request(self, method, url, **kwargs):
        """其他请求"""
        try:
            response = requests.request(method=method, url=url, **kwargs)
        except Exception as e:
            log.error(e)
        else:
            return response

    def get_json(self, method, url, **kwargs):
        """访问接口，获取json内容"""
        try:
            res = self.request(method, url, **kwargs)
            json_dic = res.json()
        except Exception as e:
            log.error(e)
        else:
            return json_dic


"""初始化requests、session"""
session = HttpSessionHandler()
request = HttpRequestsHandler()


if __name__ == "__main__":
    api_url = config.get('api', 'base_url') + config.get('api', 'register_url')
    json_data = {"mobile_phone": "13655864554", "pwd": "12345678", "type": None, "reg_name": ""}
    headers = eval(config.get('api', 'headers'))
    rs = request.get_json(method='post', url=api_url, json=json_data, headers=headers)
    print(rs)
