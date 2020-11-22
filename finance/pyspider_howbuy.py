#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-11-09 20:41:47
# Project: Howbuy

from pyspider.libs.base_handler import *
from pyquery import PyQuery as pq

import os
import json

from finance.howbuy import get_fund_info,get_fund_info_url
from finance.howbuy import get_fund_list
from finance.database import DBSession, Fund, FundInfoJson, FundProc
from finance.database import get_today_dt, get_pending_info_fund



class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):

        pengding_list = get_pending_info_fund()

        session = DBSession()

        for fund_detail in pengding_list:
            if fund_detail['info_obsolete']:
                self.crawl(
                    get_fund_info_url(fund_detail['code']),
                    callback=self.crawl_info,
                    fetch_type='js',
                    age=24*60*60*3,
                    auto_recrawl=True,
                    retries = 1,

                )



    def crawl_info(self, response):

        info = get_fund_info(pq(response.text))

        if not info['_success']:
            return {'_success': False}

        session = DBSession()

        session.merge(FundInfoJson(code=info['代码'], type='20201111', json=json.dumps(info)))
        session.merge(FundProc(code=info['代码'], info_status=0, info_retry=0, info_mdf=get_today_dt()))

        session.commit()
        session.close()

        return {'_success': True}





