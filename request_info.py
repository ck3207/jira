import requests

from login import valid_cookie
from dingding import Dingding

from loading_config import config_obj_of_authority
from public import logging

class Request:
    def __init__(self):
        self.headers = {}

    def set_headers_of_cookie(self, valid_cookie):
        self.headers = {"Cookie": valid_cookie}

    def attachment(self):
        self.headers.update({"Content-Type": "image/png"})
        url = "https://se.hundsun.com/rest/internal/2/AttachTemporaryFile?filename=2.png&size=504541&atl_token=AP09-DAGE-Z2LT-THGZ%7C3c69a80fd2a363ceeebec076e540d6d34a900822%7Clin&formToken=cc87857b5880a8bee32b7d462deead6a28203e60&projectId=2017112101"
        data = {"filename": open(file=r"C:\Users\hspcadmin\Desktop\2.png", mode="rb"),
                "atl_token": self.headers.get("Cookie").split(";")[0].split("=")[1],
                "formToken": "cc87857b5880a8bee32b7d462deead6a28203e60",
                "projectId": "2017112101",
                "size": "504541"
                }
        r = requests.post(url=url, data=data, headers=self.headers)
        print(r.text)

    def send_dingding_msg(self, msg="", url="https://oapi.dingtalk.com/robot/send"):
        timestamp, sign = Dingding.get_sign()
        headers = { "Content-Type": "application/json; charset=utf-8",
                    "timestamp": "{}".format(timestamp),
                    "sign":"{}".format(sign)}
        at_mobiles = config_obj_of_authority['dingding']['at_mobiles'].strip().split(",")
        body_data = {
     "msgtype": "text",
     "text": {
         "content": msg.format("@".join(at_mobiles))
     },
     "at": {
         "atMobiles": at_mobiles,
         "isAtAll": False
     }
 }
        url = url + "?access_token={0}&timestamp={1}&sign={2}".format(
            config_obj_of_authority['dingding']['access_token'], timestamp, sign)
        r = requests.post(url=url, json=body_data, headers=headers)
        logging.info(r.json())


r = requests.post(url="https://se.hundsun.com/secure/QuickCreateIssue!default.jspa?decorator=none",
              headers={"Cookie": valid_cookie})
r_json = r.json()


if __name__ == "__main__":
    request = Request()
    request.set_headers_of_cookie(valid_cookie)
    request.send_dingding_msg(msg="我就是我, @{} 是不一样的烟火")
    # request.attachment()
