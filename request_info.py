import requests

from login import valid_cookie


class Request:
    def __init__(self, config_obj_of_authority):
        self.headers = {"Cookie": config_obj_of_authority['default']['cookie']}

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

r = requests.post(url="https://se.hundsun.com/secure/QuickCreateIssue!default.jspa?decorator=none",
              headers={"Cookie": valid_cookie})
r_json = r.json()


if __name__ == "__main__":
    request = Request(valid_cookie)
    request.attachment()