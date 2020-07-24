# coding=gbk

import requests
"""�������� ��pip install requests"""
from handler.LogHandler import log
from handler.ConfigHandler import config


class HttpSessionHandler:
    """�Զ���¼cookies"""
    def __init__(self):
        self.session = requests.Session()

    def get(self, url, params=None, **kwargs):
        """get����"""
        try:
            response = self.session.get(url=url, params=params, **kwargs)
        except Exception as e:
            log.error(e)
        else:
            return response

    def post(self, url, data=None, json=None, **kwargs):
        """post����"""
        try:
            response = self.session.post(url=url, data=data, json=json, **kwargs)
        except Exception as e:
            log.error(e)
        else:
            return response

    def request(self, method, url, **kwargs):
        """�������󷽷�"""
        try:
            response = self.session.request(method=method, url=url, **kwargs)
        except Exception as e:
            log.error(e)
        else:
            return response

    def get_json(self, method, url, **kwargs):
        """���ʽӿڣ���ȡjson���ݣ� content-type: application/json"""
        try:
            res = self.request(method, url, **kwargs)
            json_dic = res.json()
        except Exception as e:
            log.error(e)
        else:
            return json_dic

    # def get_text(self, method, url, **kwargs):
    #     """��ȡ�ı����ݣ� text/html, text/xml, text/plain��"""
    #     try:
    #         res = self.request(method, url, **kwargs)
    #     except Exception as e:
    #         log.error(e)
    #     else:
    #         return res.text
    #
    # def get_content(self, method, url, **kwargs):
    #     """��ȡ�����Ƹ�ʽ���ݣ� image/gif, image/jpeg, image/png��"""
    #     try:
    #         res = self.request(method, url, **kwargs)
    #     except Exception as e:
    #         log.error(e)
    #     else:
    #         return res.content


class HttpRequestsHandler:
    """�����¼cookies������"""

    def get(self, url, params=None, **kwargs):
        """get����"""
        try:
            response = requests.get(url=url, params=params, **kwargs)
        except Exception as e:
            log.error(e)
        else:
            return response

    def post(self, url, data=None, json=None, **kwargs):
        """post����"""
        try:
            response = requests.post(url=url, data=data, json=json, **kwargs)
        except Exception as e:
            log.error(e)
        else:
            return response

    def request(self, method, url, **kwargs):
        """��������"""
        try:
            response = requests.request(method=method, url=url, **kwargs)
        except Exception as e:
            log.error(e)
        else:
            return response

    def get_json(self, method, url, **kwargs):
        """���ʽӿڣ���ȡjson����"""
        try:
            res = self.request(method, url, **kwargs)
            json_dic = res.json()
        except Exception as e:
            log.error(e)
        else:
            return json_dic


"""��ʼ��requests��session"""
session = HttpSessionHandler()
request = HttpRequestsHandler()


if __name__ == "__main__":
    api_url = config.get('api', 'base_url') + config.get('api', 'register_url')
    json_data = {"mobile_phone": "13655864554", "pwd": "12345678", "type": None, "reg_name": ""}
    headers = eval(config.get('api', 'headers'))
    rs = request.get_json(method='post', url=api_url, json=json_data, headers=headers)
    print(rs)
