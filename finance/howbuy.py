import time
import json
from tqdm import tqdm
from bs4 import BeautifulSoup
import re
import requests
from pyquery import PyQuery as pq
import os


# 抓取网页
def get_url(url, params=None, proxies=None):
    rsp = requests.get(url, params=params, proxies=proxies)
    rsp.raise_for_status()
    return rsp.text


def get_table(table_doc):
    rv = []
    table_body_doc = table_doc
    for tr in table_body_doc.children().items():
        row = []
        for td in tr.children().items():
            td = td.clone()
            td.find('span[class*="tips"]').remove()
            row.append(td.text())
        rv.append(row)

    return rv


# 从网页抓取数据
def get_fund_data(code, per=10, sdate='', edate='', proxies=None):
    url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx'
    params = {'type': 'lsjz', 'code': code, 'page': 1, 'per': per, 'sdate': sdate, 'edate': edate}
    html = get_url(url, params, proxies)
    soup = BeautifulSoup(html, 'html.parser')

    # 获取总页数
    pattern = re.compile(r'pages:(.*),')
    result = re.search(pattern, html).group(1)
    pages = int(result)

    # 获取表头
    heads = []
    for head in soup.findAll("th"):
        heads.append(head.contents[0])

    # 数据存取列表
    records = []

    # 从第1页开始抓取所有页面数据
    page = 1
    while page <= pages:
        params = {'type': 'lsjz', 'code': code, 'page': page, 'per': per, 'sdate': sdate, 'edate': edate}
        html = get_url(url, params, proxies)
        soup = BeautifulSoup(html, 'html.parser')

        # 获取数据
        for row in soup.findAll("tbody")[0].findAll("tr"):
            row_records = []
            for record in row.findAll('td'):
                val = record.contents

                # 处理空值
                if not val:
                    row_records.append('--')
                else:
                    row_records.append(val[0])

            # 记录数据
            records.append(row_records)

        # 下一页
        page = page + 1

    # 数据整理到dataframe
    return records


def get_fund_doc(code):
    url = 'https://www.howbuy.com/fund/{0}/'.format(code)
    doc = pq(url)
    return doc


def get_fund_info(code):
    doc = get_fund_doc(code)

    fund_name = doc(
        """body > div.main > div.file_top_box > div > div.file_t_righ.rt > div > 
        div.gmfund_title > div > div.lt > h1""") \
        .clone().children().remove().end().text()

    code = doc(
        """body > div.main > div.file_top_box > div > div.file_t_righ.rt > div > 
        div.gmfund_title > div > div.lt > h1""") \
        .children().text()
    code = code.replace('(', '').replace(')', '')

    sharp_doc = doc(
        """#nTab2_0 > div:nth-child(5) > div.con-container-right.file_zcpz.clearfix > 
        div.chart > div > div.fxzb > table > tbody > tr.bottom"""
    )
    sharp = [sharp_doc.children('''td[class="tdl"]''').text()]
    for a in sharp_doc.children('''td[class!="tdl"]''').items():
        sharp.append(a.text())

    manager_name = doc(
        '''
        #nTab3_0 > div.manager_b_l.lt > div > div.manager_b_r > div > ul.item_4 > li:nth-child(1)
        '''
    ).text()

    manager_reward = doc(
        '''p:contains('从业年均回报')'''
    ).parent().children('''p[class="b2"]''').text()

    manager_max_rise = doc(
        '''p:contains('最大盈利')'''
    ).parent().children('''p[class="b2"]''').text()

    manager_max_redraw = doc(
        '''p:contains('最大回撤')'''
    ).parent().children('''p[class="b2"]''').text()

    style_doc = doc(
        '''div:contains('当前投资风格')'''
    ).parent().children('''div[class="right_content"]''')

    style_type = style_doc.children(
        '''p[class="right_p1"]'''
    ).text()

    style_desc = style_doc.children(
        '''div[class="right_text"]'''
    ).text()

    style_suggest = style_doc.children(
        '''div[class="suggest_text"]'''
    ).text()

    fund_up_doc = doc(
        '''div[class="file_jjzf"]'''
    )

    fund_up_tab = fund_up_doc('''div[class="title"]''')
    fund_up_title = {}
    for fund_up_title_doc in fund_up_tab('li').items():
        fund_up_title[str(fund_up_title_doc.attr('id'))[-1]] = fund_up_title_doc.text()

    fund_up_data_doc = fund_up_doc('''div[class~="jjzf_content"]''')
    func_up = {}
    for div in fund_up_data_doc.items():
        table_id = str(div.attr('id'))[-1]
        table_doc = div.children()
        func_up[fund_up_title[table_id]] = get_table(table_doc)

    return {
        '基金名称': fund_name,
        'code': code,
        'sharp': sharp,
        'manager': manager_name,
        'manager_reward': manager_reward,
        'manager_max_rise': manager_max_rise,
        'manager_max_redraw': manager_max_redraw,
        'style_type': style_type,
        'style_desc': style_desc,
        'style_suggest': style_suggest,
    }

    pass


if __name__ == '__main__':
    doc = get_fund_info('001790')
    print(json.dumps(doc,indent=2,ensure_ascii=False))
    # data = get_fund_data('001790', per=200, sdate='1900-01-01', edate='2099-12-31')
    # print(data)
