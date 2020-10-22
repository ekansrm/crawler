import time
import json
from tqdm import tqdm
import requests
from pyquery import PyQuery as pq
import os

def get_fund_doc(code):
    url = 'https://www.howbuy.com/fund/{0}/'.format(code)
    doc = pq(url)
    return doc


def get_fund_info(code):
    doc = get_fund_doc(code)
    name = doc(
        """body > div.main > div.file_top_box > div > div.file_t_righ.rt > div > 
        div.gmfund_title > div > div.lt > h1""")\
        .clone().children().remove().end().text()
    code = doc(
        """body > div.main > div.file_top_box > div > div.file_t_righ.rt > div > 
        div.gmfund_title > div > div.lt > h1""")\
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

    return {
        'name': name,
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
    print(doc)
