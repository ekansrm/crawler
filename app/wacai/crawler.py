import re
import os
import time
import json
import traceback
import requests


class Crawler(object):
    _header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    }

    url = 'https://www.wacai.com/activity/bkk-frontier/api/v2/flow/save?___t=1693928140108'

    body = {
        "flows": [
            {
                "amount": 1,
                "tradetgt": {},
                "account": {
                    "key": "432305E56ED946D48DA0973940A3A73E",
                    "label": "忻忻-现金（CNY）"
                },
                "member": {
                    "key": "1",
                    "label": "KAMIWei"
                },
                "comment": "",
                "reimburse": 0,
                "tradetgtId": None,
                "tradetgtName": None,
                "accountId": "432305E56ED946D48DA0973940A3A73E",
                "bizTime": "2023-09-05T15:35:17.607Z",
                "address": "",
                "bkId": 113509541,
                "bookId": "A1BFB7D05F6C9C201225C5FDAC2F6A69",
                "categoryId": "1210",
                "edited": 0,
                "deleted": 0,
                "id": 0,
                "members": [
                    {
                        "memberId": "1",
                        "amount": 1
                    }
                ],
                "recType": 1,
                "type": None,
                "sourceSystem": 201,
                "bizId": "DDBDB73F5EEC018453BE54DB1FB810A7"
            }
        ]
    }

    def run(self):
        r = requests.post(self.url, data=self.body, headers=self._header)
        print(r.content.decode())



if __name__ == '__main__':
    crawler = Crawler()
    crawler.run()
