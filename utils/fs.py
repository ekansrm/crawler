import re
import time
import os
import json
import requests
from tqdm import tqdm
from pyquery import PyQuery as pq


class FsRowDict(object):
    _data = {}
    _path = ''

    def __init__(self, path):
        self._path = path
        if not os.path.exists(path):
            return
        with open(path, 'r', encoding='utf-8') as fp:
            lines = fp.readlines()
            db_json = '\n'.join(lines)
            if db_json.strip() == '':
                self._data = {}
            else:
                self._data = json.loads(db_json)

    def select(self, tid):
        if tid not in self._data:
            return {}
        else:
            return self._data[tid]

    def select_all(self, ):
        return self._data

    def upsert(self, tid, row):
        if tid not in self._data:
            self._data[tid] = row
        else:
            self._data[tid].update(row)

    def commit(self):
        if not os.path.exists(os.path.dirname(self._path)):
            os.mkdir(os.path.dirname(self._path))
        with open(self._path, 'w', encoding='utf-8') as fp:
            fp.write(json.dumps(self._data, indent=2, ensure_ascii=False))
