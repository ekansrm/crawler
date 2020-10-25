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


def get_fund_doc(code):
    url = 'https://www.howbuy.com/fund/{0}/'.format(code)
    doc = pq(url)
    return doc

# 从网页抓取数据
def get_fund_trend(code, line_per_page=10, date_begin='', date_end='', proxies=None):
    url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx'
    params = {'type': 'lsjz', 'code': code, 'page': 1, 'per': line_per_page, 'sdate': date_begin, 'edate': date_end}
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
        params = {
            'type': 'lsjz', 'code': code, 'page': page, 'per': line_per_page, 'sdate': date_begin, 'edate': date_end
        }
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

    return records


def get_fund_rise(doc):
    rise_doc = doc(
        '''div[class="file_jjzf"]'''
    )
    rise_type_doc = rise_doc('''div[class="title"]''')
    rise_type = {}
    for a_rise_type_doc in rise_type_doc('li').items():
        rise_type[str(a_rise_type_doc.attr('id'))[-1]] = a_rise_type_doc.text()
    rise_data_doc = rise_doc('''div[class~="jjzf_content"]''')
    rise = {}
    for div in rise_data_doc.items():
        table_id = str(div.attr('id'))[-1]
        table_doc = div.children()
        rise[rise_type[table_id]] = get_table(table_doc)
    return rise


def get_fund_info(code):
    doc = get_fund_doc(code)

    name = doc(
        """body > div.main > div.file_top_box > div > div.file_t_righ.rt > div > 
        div.gmfund_title > div > div.lt > h1""") \
        .clone().children().remove().end().text()

    code = doc(
        """body > div.main > div.file_top_box > div > div.file_t_righ.rt > div > 
        div.gmfund_title > div > div.lt > h1""") \
        .children().text()
    code = code.replace('(', '').replace(')', '')

    sharpe_ratio_doc = doc(
        """#nTab2_0 > div:nth-child(5) > div.con-container-right.file_zcpz.clearfix > 
        div.chart > div > div.fxzb > table > tbody > tr.bottom"""
    )
    sharpe_ratio = [sharpe_ratio_doc.children('''td[class="tdl"]''').text()]
    for a in sharpe_ratio_doc.children('''td[class!="tdl"]''').items():
        sharpe_ratio.append(a.text())

    manager_name = doc(
        '''
        #nTab3_0 > div.manager_b_l.lt > div > div.manager_b_r > div > ul.item_4 > li:nth-child(1)
        '''
    ).text()

    manager_admin_num = doc(
        '''li:contains('当前管理基金')'''
    ).children().text()

    manager_admin_time = doc(
        '''span:contains('从业时间')'''
    ).text().split('：')[-1]

    manager_roi = doc(
        '''p:contains('从业年均回报')'''
    ).parent().children('''p[class="b2"]''').text()

    manager_max_gain = doc(
        '''p:contains('最大盈利')'''
    ).parent().children('''p[class="b2"]''').text()

    manager_max_drop = doc(
        '''p:contains('最大回撤')'''
    ).parent().children('''p[class="b2"]''').text()

    investment_style_doc = doc(
        '''div:contains('当前投资风格')'''
    ).parent().children('''div[class="right_content"]''')

    investment_style_type = investment_style_doc.children(
        '''p[class="right_p1"]'''
    ).text()

    investment_style_desc = investment_style_doc.children(
        '''div[class="right_text"]'''
    ).text()

    investment_style_suggest = investment_style_doc.children(
        '''div[class="suggest_text"]'''
    ).text()

    rise = get_fund_rise(doc)

    return {
        '基金名称': name,
        '基金代码': code,
        '夏普比率': sharpe_ratio,
        '基金经理': {
            '名字': manager_name,
            '管理数量': manager_admin_num,
            '从业时间': manager_admin_time,
            '从业年均回报': manager_roi,
            '从业最大盈利': manager_max_gain,
            '从业最大跌幅': manager_max_drop,
        },
        '投资风格': {
            '类型': investment_style_type,
            '描述': investment_style_desc,
            '建议': investment_style_suggest,
        },
        '基金涨幅': rise
    }

    pass


if __name__ == '__main__':
    doc = get_fund_info('001790')
    print(json.dumps(doc, indent=2, ensure_ascii=False))
    # data = get_fund_data('001790', per=200, sdate='1900-01-01', edate='2099-12-31')
    # print(data)
