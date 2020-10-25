import time
import json
from tqdm import tqdm
from bs4 import BeautifulSoup
import re
import requests
from pyquery import PyQuery as pq
import os
import time


def get_url_response(url, params=None, proxies=None):
    """
    获取 URL 内容
    :param url:
    :param params:
    :param proxies:
    :return:
    """
    rsp = requests.get(url, params=params, proxies=proxies)
    rsp.raise_for_status()
    return rsp.text


def get_table_body_data(table_body_dom):
    """
    读取 Table Body DOM 的表格数据
    :param table_body_dom: 
    :return: 
    """
    data = []
    for tr in table_body_dom.children().items():
        row = []
        for td in tr.children().items():
            td = td.clone()
            td.find('span[class*="tips"]').remove()
            row.append(td.text())
        data.append(row)

    irow = {}

    for i, a in enumerate(data):
        irow[a[0]] = i

    icol = {}

    for i, a in enumerate(data[0]):
        icol[a] = i

    return {
        'irow': irow,
        'icol': icol,
        'data': data
    }


def get_fund_dom(code):
    url = 'https://www.howbuy.com/fund/{0}/'.format(code)
    doc = pq(url)
    return doc


def get_fund_trend(code, line_per_page=10, date_begin='', date_end='', proxies=None):
    """
    获取基金走势数据
    :param code: 基金代码
    :param line_per_page:
    :param date_begin:
    :param date_end:
    :param proxies:
    :return:
    """
    url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx'
    params = {'type': 'lsjz', 'code': code, 'page': 1, 'per': line_per_page, 'sdate': date_begin, 'edate': date_end}
    html = get_url_response(url, params, proxies)
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
        html = get_url_response(url, params, proxies)
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
    """
    获取基金涨幅数据
    :param doc:
    :return:
    """
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
        rise[rise_type[table_id]] = get_table_body_data(table_doc)
    return rise


def get_fund_risk(doc):
    """
    获取基金风险
    :param doc:
    :return:
    """
    risk_doc = doc(
        '''h3:contains("基金风险")'''
    ).parent().parent()

    risk_table_doc = risk_doc('tbody')

    risk_data = get_table_body_data(risk_table_doc)

    return risk_data


def get_fund_config(dom):
    config_dom = dom(
        '''h3:contains("行业配置")'''
    ).parent().parent()

    a = config_dom.html()

    config_concentration = config_dom(
        '''b:contains("行业集中度")'''
    ).text()

    config_industry = [a.text() for a in config_dom.children('''tspan''').items()]

    return {
        '集中度': config_concentration,
        '配置': config_industry
    }



def get_fund_manager(doc):
    """
    获取基金经理
    :param doc:
    :return:
    """

    def get_a_fun_manager(manager_doc):

        manager_name = manager_doc(
            '''span:contains("综合评分")'''
        ).parent().parent().children().eq(0).text()

        manager_admin_num = manager_doc(
            '''li:contains('当前管理基金')'''
        ).children().text()

        manager_admin_time = manager_doc(
            '''span:contains('从业时间')'''
        ).text().split('：')[-1]

        manager_roi = manager_doc(
            '''p:contains('从业年均回报')'''
        ).parent().children('''p[class="b2"]''').text()

        manager_max_gain = manager_doc(
            '''p:contains('最大盈利')'''
        ).parent().children('''p[class="b2"]''').text()

        manager_max_drop = manager_doc(
            '''p:contains('最大回撤')'''
        ).parent().children('''p[class="b2"]''').text()

        return {
            '名字': manager_name,
            '管理数量': manager_admin_num,
            '从业时间': manager_admin_time,
            '从业年均回报': manager_roi,
            '从业最大盈利': manager_max_gain,
            '从业最大跌幅': manager_max_drop,
        }

    managers_doc = doc(
        '''div[class~="manager_box"]'''
    )

    managers_info = []
    for a_manager_doc in managers_doc.items():
        managers_info.append(get_a_fun_manager(a_manager_doc))

    return managers_info


def get_fund_all(code):

    try:

        doc = get_fund_dom(code)

        name = doc(
            """body > div.main > div.file_top_box > div > div.file_t_righ.rt > div > 
            div.gmfund_title > div > div.lt > h1""") \
            .clone().children().remove().end().text()

        code = doc(
            """body > div.main > div.file_top_box > div > div.file_t_righ.rt > div > 
            div.gmfund_title > div > div.lt > h1""") \
            .children().text()
        code = code.replace('(', '').replace(')', '')

        label = doc(
            '''p[class="risk"]'''
        ).text()

        scale = doc(
            '''li:contains('最新规模')'''
        ).children().text()

        risk_info = get_fund_risk(doc)

        manager_info = get_fund_manager(doc)

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

        rise_info = get_fund_rise(doc)

        config_info = get_fund_config(doc)

        return {
            '名称': name,
            '代码': code,
            '类型': label,
            '规模': scale,
            '风险': risk_info,
            '经理': manager_info,
            '风格': {
                '类型': investment_style_type,
                '描述': investment_style_desc,
                '建议': investment_style_suggest,
            },
            '涨幅': rise_info,
            '配置': config_info,
        }

    except Exception as e:
        return {
            '代码': code
        }


def get_fund_all_from_list(list_path):

    fund_code_list = set()
    with open(list_path, 'r', encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.strip()
            if len(line) != 0:
                fund_code_list.add(line)

    for fund_code in tqdm(fund_code_list):
        fund_detail = get_fund_all(fund_code)
        with open(os.path.join('data', 'fund_info', 'fund_' + fund_code + '.json'), 'w', encoding='utf-8') as fp:
            json.dump(fund_detail, fp, indent=2, ensure_ascii=False)
        time.sleep(0.05)


if __name__ == '__main__':

    fund_detail = get_fund_all('000126')
    print(json.dumps(fund_detail, indent=2, ensure_ascii=False))
    # get_fund_all_from_list(os.path.join('data', 'fund_list.txt'))

