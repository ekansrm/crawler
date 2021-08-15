import re
import os
import time
import json
import requests
from tqdm import tqdm
from pyquery import PyQuery as pq
from utils.fs import FsRowDict
from utils.img import download_img


class Crawler(object):
    _header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    }

    _base_dir = ''
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
        if area == '海珠':
            url_tpl = 'http://www.bhcvs.com/forum.php?mod=forumdisplay&fid=2&typeid=3&filter=typeid&typeid=3&page={0}'
            return url_tpl.format(page)
        if area == '番禺':
            url_tpl = 'http://www.bhcvs.com/forum.php?mod=forumdisplay&fid=2&typeid=7&filter=typeid&typeid=7&page={0}'
            return url_tpl.format(page)
        if area == '越秀':
            url_tpl = 'http://www.bhcvs.com/forum.php?mod=forumdisplay&fid=2&typeid=5&filter=typeid&typeid=5&page={0}'
            return url_tpl.format(page)
        if area == '全部':
            url_tpl = 'http://www.bhcvs.com/forum.php?mod=forumdisplay&fid=2&orderby=lastpost&filter=lastpost&orderby=lastpost&page={0}'
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
        post_img_dom = post_dom('img[file*="data/attachment/forum"]')
        post_img = [Crawler.base_url() + e.attr('file') for e in post_img_dom.items()]
        post_area_dom = dom('h1[class="ts"]>a')
        post_area = post_area_dom.text().replace('[', '').replace(']', '')
        post_time_dom = post_dom('em:contains(发表于)>span')
        post_time = post_time_dom.attr('title')

        if post_time is None:
            post_time_dom = post_dom('em:contains(发表于)')
            post_time = post_time_dom.text().replace('发表于', '').strip()
        try:
            post_time = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(post_time, "%Y-%m-%d %H:%M:%S"))
        except:
            try:
                post_time = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(post_time, "%Y-%m-%d %H:%M"))
            except:
                pass

        return {
            'txt': post_txt,
            'img': post_img,
            'area': post_area,
            'time': post_time,
        }

    @property
    def session(self):
        if self._session is None:
            self._session = Crawler.get_session_by_login()
        return self._session

    def _get_qm_list_by_url(self, url):
        r = self.session.get(url, headers=self._header)
        return Crawler.parse_qm_list_from_dom(pq(r.text))

    def _get_qm_info_by_url(self, url):
        r = self.session.get(url, headers=self._header)
        return Crawler.parse_qm_info_from_dom(pq(r.text))


    def __init__(self, base_dir):
        self._base_dir = base_dir
        # self._session = Crawler.get_session_by_login()
        self._row_dict = FsRowDict(os.path.join(base_dir, 'all.json'))

    def __del__(self):
        # self._session.close()
        pass

    def upsert_qm_list_by_area(self, area, page_num, interval=0.5):
        pbar = tqdm(range(1, page_num + 1))
        rv = {}
        for page in pbar:
            try:
                pbar.set_description('抓取列表信息 ' + str(page))
                url = Crawler.list_url(page, area)
                page_rv = self._get_qm_list_by_url(url)
                for e in page_rv:
                    self._row_dict.upsert(page_rv[e]['tid'], page_rv[e])
                    rv[e] = self._row_dict.select(page_rv[e]['tid'])
                time.sleep(interval)
            except Exception as e:
                print('发生异常, 停止翻页, error=' + e)
                break
        self._row_dict.commit()
        return rv

    def upsert_qm_info_by_list(self, tid_list, refresh=True, interval=0.5):
        if len(tid_list) == 0:
            return {}
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
                _row = self._get_qm_info_by_url(info_url)
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

    def upsert_qm_info_missing(self, interval=0.5):
        tid_list = self._row_dict.select_all().keys()
        pbar = tqdm(tid_list)
        i = 0
        u = 10
        rv = {}
        for tid in pbar:
            pbar.set_description('抓取详情 ' + tid)
            row = self._row_dict.select(tid)
            row_empty = 'txt' not in row or row['txt'] is None or row['txt'].strip() == ''
            if row_empty:
                info_url = Crawler.info_url(tid)
                _row = self._get_qm_info_by_url(info_url)
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

    def select_qm_info_missing_img(self):
        infos = self._row_dict.select_all()
        return {e: infos[e] for e in infos if 'img' not in infos[e] or len(infos[e]['img']) == 0}

    def clean_qm_txt(self):
        for tid, row in self._row_dict.select_all().items():
            lines = row.get('txt', '暂无介绍').split('\n')
            lines = [line for line in lines
                     if '本帖最后由' not in line
                     and '下载附件' not in line
                     and '下载次数' not in line
                     and '上传' not in line
                     and len(line.strip()) > 0]
            txt = '\n'.join(lines)
            row['txt'] = txt

        self._row_dict.commit()



    def download_qm_info_img(self, interval=0.5):
        tid_list = self._row_dict.select_all().keys()
        pbar = tqdm(tid_list)
        i = 0
        u = 10
        rv = {}
        for tid in pbar:
            pbar.set_description('抓取图片 ' + tid)
            img_dir = os.path.join(self._base_dir, tid)

            row = self._row_dict.select(tid)
            img = row.get('img', [])
            img_done = row.get('img_done', [])
            for a_img in img:
                if a_img in img_done:
                    continue
                try:
                    download_img(a_img, img_dir)
                    img_done.append(a_img)
                except Exception as e:
                    print('下载错误: ' + a_img)
                time.sleep(interval)

            row['img_done'] = img_done
            self._row_dict.upsert(tid, row)
            row = self._row_dict.select(tid)
            rv[tid] = row

            i += 1
            if i >= u:
                i = 0
                self._row_dict.commit()

        self._row_dict.commit()

        return rv


base_dir = os.path.join('.', '_rst', 'bhc')
crawler = Crawler(base_dir)

if __name__ == '__main__':
    # missing_img_qm = crawler.select_qm_info_missing_img()
    # print(json.dumps(missing_img_qm, indent=2))
    qm_list = crawler.upsert_qm_list_by_area('越秀', 10, interval=1)
    # qm_info = crawler.upsert_qm_info_by_list(qm_list.keys(), refresh=True)
    crawler.upsert_qm_info_missing()
    crawler.download_qm_info_img()
    crawler.clean_qm_txt()
    # qm_info = crawler.upsert_qm_info_by_list(qm_list.keys(), refresh=False)
    pass
