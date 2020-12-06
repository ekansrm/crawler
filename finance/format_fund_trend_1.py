import os
import re
import traceback
import json
from tqdm import tqdm
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

from finance.database import Base
from finance.database import DBSession
from finance.database import init_db
from finance.database import FundTrendJson, Fund

header = ['基金代码', '净值日期', '单位净值', '累计净值', '日增长率', '申购状态', '赎回状态', '分红送配']


# noinspection NonAsciiCharacters
class FundTrend(Base):
    __tablename__ = 'fund_trend'
    基金代码 = Column('基金代码', String(128), primary_key=True)
    净值日期 = Column('净值日期', Integer(), primary_key=True)
    单位净值 = Column('单位净值', String(128))
    累计净值 = Column('累计净值', String(128))
    日增长率 = Column('日增长率', String(128))
    申购状态 = Column('申购状态', String(128))
    赎回状态 = Column('赎回状态', String(128))
    分红送配 = Column('分红送配', String(128))


def read_json_from_database(session: DBSession, code):
    return [
        json.loads(r.json)
        for r in session.query(FundTrendJson).filter(FundTrendJson.code == code).all()
    ]


def write_info_to_database(session: DBSession, rows):
    obj_list = []
    for row in rows:
        try:
            row['基金代码'] = row['code']
            row['净值日期'] = row['date']
            # row['单位净值'] = float(row['单位净值'])
            # row['累计净值'] = float(row['累计净值'])
            del row['code']
            del row['date']

            obj_list.append(FundTrend(**row))
        except Exception as e:
            print(e)
    session.bulk_save_objects(obj_list)
    session.commit()


if __name__ == '__main__':
    session = DBSession()
    init_db()
    fund_list = session.query(Fund).all()
    for fund in tqdm(fund_list):
        try:
            fund_trends = read_json_from_database(session, code=fund.code)
            write_info_to_database(session, fund_trends)
        except Exception as e:
            print(e)

