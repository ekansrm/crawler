import re
import time
import os
import json
import requests
from tqdm import tqdm
from pyquery import PyQuery as pq

header = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'Accept-Encoding': 'gzip, deflate',
    # 'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Cache-Control': 'max-age=0',
    # 'Connection': 'keep-alive',
    # 'DNT': '1',
    # 'Host': 'www.bhcvs.com',
    # 'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
}


def get_cookies():
    f = open(r'cookies', 'r')  # 打开所保存的cookies内容文件
    cookies = {}  # 初始化cookies字典变量
    for line in f.read().split(';'):  # 按照字符：进行划分读取
        # 其设置为1就会把字符串拆分成2份
        name, value = line.strip().split('=', 1)
        cookies[name] = value
    return cookies


def get_fund_info_url(code):
    url = 'https://www.howbuy.com/fund/{0}/'.format(code)
    return url


def get_fund_dom_by_pyquery(code):
    url = get_fund_info_url(code)
    doc = pq(url)
    return doc


_db = {}
_db_name = ''


def create_db_session(dbname):
    global _db_name
    global _db
    _db_name = dbname
    if os.path.exists(dbname):
        with open(dbname, 'r', encoding='utf-8') as fp:
            lines = fp.readlines()
            db_json = '\n'.join(lines)
            if db_json.strip() == '':
                _db = {}
            else:
                _db = json.loads(db_json)


def commit_db_session():
    a = _db_name
    with open(_db_name, 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(_db, indent=2, ensure_ascii=False))


def select_from_db(tid):
    global _db
    if tid not in _db:
        return {}
    else:
        return _db[tid]


def select_all_from_db():
    global _db
    return _db


def upsert_to_db(tid, row):
    global _db
    if tid not in _db:
        _db[tid] = row
    else:
        _db[tid].update(row)


def get_qm_tid_by_href(href):
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


header_login = {
    'Referer': 'http://www.bhcvs.com/member.php?mod=logging&action=login&referer=http://www.bhcvs.com/forum.php',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
}


def get_session_by_login():
    url = 'http://www.bhcvs.com/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=LXA4M&inajax=1'

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


def upsert_qm_list_by_url(session, url):
    r = session.get(url, headers=header)
    page_html = r.text
    page_dom = pq(page_html)
    qm_href_list = page_dom(
        '''h3>a[href*="thread"]'''
    )
    for e in qm_href_list.items():
        title = e.attr('title')
        href = e.attr('href')
        tid = get_qm_tid_by_href(href)
        row = {
            'tid': tid,
            'title': title,
        }
        upsert_to_db(tid, row)


def upsert_qm_list_by_url_iter(session, url_tpl, page_num, interval=0.5):
    pbar = tqdm(range(1, page_num + 1))
    for page in pbar:
        pbar.set_description('抓取列表信息 ' + str(page))
        url = url_tpl.format(page)
        upsert_qm_list_by_url(session, url)
        time.sleep(interval)
    commit_db_session()


def get_qm_base_url():
    return 'http://www.bhcvs.com/'


def get_qm_info_url(tid):
    return 'http://www.bhcvs.com/thread-{0}-1-2.html'.format(tid)


def upsert_qm_info_by_list(session, tid_list, interval=0.2):
    pbar = tqdm(tid_list)
    i = 0
    u = 10
    for tid in pbar:
        pbar.set_description('抓取详情 ' + tid)
        info_url = get_qm_info_url(tid)
        row = get_qm_info_by_url(session, info_url)
        upsert_to_db(tid, row)
        time.sleep(interval)
        i += 1
        if i >= u:
            i = 0
            commit_db_session()
    commit_db_session()


def get_qm_info_by_url(session, url):
    r = session.get(url, headers=header)
    return get_qm_info_by_dom(pq(r.text))


def get_qm_info_by_dom(dom):
    post_dom = dom('div[id="postlist"]>div[id*="post"]:first')
    post_txt_dom = post_dom('td[id*="postmessage"]')
    post_txt = post_txt_dom.text()
    post_img_dom = post_dom('div[class*="savephotop"]>img')
    post_img = [get_qm_base_url() + e.attr('file') for e in post_img_dom.items()]

    return {
        'txt': post_txt,
        'img': post_img,
    }


if __name__ == '__main__':
    # url_tpl = 'http://www.bhcvs.com/forum.php?mod=forumdisplay&fid=2&page={0}'
    url_tpl = 'http://www.bhcvs.com/forum.php?mod=forumdisplay&fid=2&orderby=lastpost&typeid=2&filter=lastpost&orderby=lastpost&typeid=2&page={0}'

    session = get_session_by_login()

    create_db_session('天河.json')
    upsert_qm_list_by_url_iter(session, url_tpl, 20)

    qm_list = select_all_from_db()
    qm_tid_list = qm_list.keys()

    upsert_qm_info_by_list(session, qm_tid_list)




    # base = 'http://www.bhcvs.com/forum.php?mod=forumdisplay&fid=2&page=1'
    # qm_list, nxt_url = get_qm_list_dom(base)
    # login()
    # href = 'forum.php?mod=viewthread&amp;tid=7251&amp;extra=page%3D1%26filter%3Dauthor%26orderby%3Ddateline'
    # print(get_qm_tid_by_href(href))
    # href2 = 'thread-7251-1-1.html'
    # print(get_qm_tid_by_href(href2))
    #
    # tid = '123'
    # row = {'a': 1}
    #
    # open_db_session('test')
    # print(select_from_db(tid))
    # upsert_to_db(tid, row)
    # print(select_from_db(tid))
    # row = {'a': 1, 'b': 2}
    # upsert_to_db(tid, row)
    # print(select_from_db(tid))
    # close_db_session()
    # open_db_session('test')
    # row = {'c': 3, 'b': 3}
    # upsert_to_db(tid, row)
    # print(select_from_db(tid))
    # close_db_session()
