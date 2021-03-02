# -*- coding: utf-8 -*-
# @Time    : 2021/3/2 12:25
# @Author  : chenkang19736
# @File    : get_dingding_sign.py
# @Software: PyCharm

#python 3.8
import time
import hmac
import hashlib
import base64
import urllib.parse

from public import logging
from loading_config import config_obj_of_authority


class Dingding:
    def __init__(self):
        pass

    @staticmethod
    def get_sign(secret=""):
        if not secret:
            secret = config_obj_of_authority['dingding']['secret'].strip()
        timestamp = str(round(time.time() * 1000))
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        logging.info("Timestamp is [{0}]. Sign is [{1}].".format(timestamp, sign))
        return timestamp, sign

if __name__ == "__main__":
    Dingding.get_sign()