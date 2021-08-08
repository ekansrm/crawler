import re
import os
import time
import requests
from tqdm import tqdm
from pyquery import PyQuery as pq
from utils.fs import FsRowDict


class Crawler(object):
    _header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    }

    _session = None
    _row_dict = None


    @staticmethod
    def base_url():
        return 'http://www.bhcvs.com/'

    @staticmethod
    def list_url(page, area='天河'):
        if area == '天河':
            url_tpl = 'http://www.bhcvs.com/forum.php?mod=forumdisplay&fid=2&orderby=lastpost&typeid=2&filter=lastpost&orderby=lastpost&typeid=2&page={0}'
            return url_tpl.format(page)
        raise Exception('未知地区: ' + area)

    @staticmethod
    def info_url(tid):
        return 'http://www.bhcvs.com/thread-{0}-1-2.html'.format(tid)

    @staticmethod
    def get_session_by_login():
        url = 'http://www.bhcvs.com/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=LXA4M&inajax=1'

        header_login = {
            'Referer': 'http://www.bhcvs.com/member.php?mod=logging&action=login&referer=http://www.bhcvs.com/forum.php',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        }

        data = {
            'loginfield': 'username',
            'username': 'mrsnake',
            'password': '2271989wlsex',
            'questionid': 0,
            'answer': '',
        }

        session = requests.session()
        session.post(url, headers=header_login, data=data)
        return session

    @staticmethod
    def parse_qm_tid_from_href(href):
        """
        从 href 里解析出 tid
        :param href:
        """
        tid = None
        if 'thread-' in href:
            tid = href.split('-')[1]

        if 'tid=' in href:
            tid = re.search('(?<=tid=)[0-9]+', href).group()

        return tid

    @staticmethod
    def parse_qm_list_from_dom(dom):
        qm_href_list = dom(
            '''h3>a[href*="thread"]'''
        )
        rv = {}
        for e in qm_href_list.items():
            title = e.attr('title')
            href = e.attr('href')
            tid = Crawler.parse_qm_tid_from_href(href)
            row = {
                'tid': tid,
                'title': title,
            }
            rv[tid] = row
        return rv

    @staticmethod
    def parse_qm_info_from_dom(dom):
        post_dom = dom('div[id="postlist"]>div[id*="post"]:first')
        post_txt_dom = post_dom('td[id*="postmessage"]')
        post_txt = post_txt_dom.text()
        post_img_dom = post_dom('div[class*="savephotop"]>img')
        post_img = [Crawler.base_url() + e.attr('file') for e in post_img_dom.items()]

        return {
            'txt': post_txt,
            'img': post_img,
        }

    def get_qm_list_by_url(self, url):
        r = self._session.get(url, headers=self._header)
        return Crawler.parse_qm_list_from_dom(pq(r.text))

    def get_qm_info_by_url(self, url):
        r = self._session.get(url, headers=self._header)
        return Crawler.parse_qm_info_from_dom(pq(r.text))

    def __init__(self, row_dict):
        self._session = Crawler.get_session_by_login()
        self._row_dict = row_dict

    def __del__(self):
        self._session.close()

    def upsert_qm_list_by_area(self, area, page_num, interval=0.5):
        pbar = tqdm(range(1, page_num + 1))
        rv = {}
        for page in pbar:
            try:
                pbar.set_description('抓取列表信息 ' + str(page))
                url = Crawler.list_url(page, area)
                page_rv = self.get_qm_list_by_url(url)
                for e in page_rv:
                    page_rv[e]['area'] = area
                    self._row_dict.upsert(page_rv[e]['tid'], page_rv[e])
                    rv[e] = self._row_dict.select(page_rv[e]['tid'])
                time.sleep(interval)
            except Exception as e:
                print('发生异常, 停止翻页')
                break
        self._row_dict.commit()
        return rv

    def upsert_qm_info_by_list(self, tid_list, refresh=True, interval=0.2):
        pbar = tqdm(tid_list)
        i = 0
        u = 10
        rv = {}
        for tid in pbar:
            pbar.set_description('抓取详情 ' + tid)
            row = self._row_dict.select(tid)
            is_empty = 'txt' not in row or row['txt'] is None or row['txt'].strip() == ''
            if is_empty or refresh:
                info_url = Crawler.info_url(tid)
                _row = self.get_qm_info_by_url(info_url)
                self._row_dict.upsert(tid, _row)
                row = self._row_dict.select(tid)
                time.sleep(interval)
            rv[tid] = row

            i += 1
            if i >= u:
                i = 0
                self._row_dict.commit()

        self._row_dict.commit()

        return rv

    def upsert_qm_info_missing(self, interval=0.2):
        tid_list = self._row_dict.select_all().keys()
        pbar = tqdm(tid_list)
        i = 0
        u = 10
        rv = {}
        for tid in pbar:
            pbar.set_description('抓取详情 ' + tid)
            row = self._row_dict.select(tid)
            is_empty = 'txt' not in row or row['txt'] is None or row['txt'].strip() == ''
            if is_empty:
                info_url = Crawler.info_url(tid)
                _row = self.get_qm_info_by_url(info_url)
                self._row_dict.upsert(tid, _row)
                row = self._row_dict.select(tid)
                time.sleep(interval)
            rv[tid] = row

            i += 1
            if i >= u:
                i = 0
                self._row_dict.commit()

        self._row_dict.commit()

        return rv


if __name__ == '__main__':

    row_dict = FsRowDict(os.path.join('.', '_rst', 'bhc', 'all.json'))

    crawler = Crawler(row_dict)
    crawler.upsert_qm_info_missing()
    # qm_list = crawler.upsert_qm_list_by_area('天河', 30)
    # qm_info = crawler.upsert_qm_info_by_list(qm_list.keys(), refresh=False)


