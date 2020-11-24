from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import or_, and_
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
import json
from typing import List, Dict

Base = declarative_base()


class Fund(Base):
    __tablename__ = 'fund'
    code = Column('code', String(128), primary_key=True)


class FundProc(Base):
    __tablename__ = 'fund_zproc'
    code = Column('code', String(128), primary_key=True)
    info_status = Column('info_status', Integer())
    info_retry = Column('info_retry', Integer(), default=0)
    info_mdf = Column('info_mdf', Integer())
    trend_status = Column('trend_status', Integer())
    trend_newest = Column('trend_newest', Integer())
    trend_oldest = Column('trend_oldest', Integer())
    trend_retry = Column('trend_retry', Integer(), default=0)


class FundInfoJson(Base):
    __tablename__ = 'fund_info_json'
    code = Column('code', String(128), primary_key=True)
    type = Column('type', String(128), default='standard')
    json = Column('json', LONGTEXT(), default='{}')


class FundTrendJson(Base):
    __tablename__ = 'fund_trend_json'
    code = Column('code', String(128), primary_key=True)
    date = Column('date', Integer(), primary_key=True)
    json = Column('json', LONGTEXT(), default='{}')


# noinspection NonAsciiCharacters
class FundTrend(Base):
    __tablename__ = 'fund_trend'
    基金代码 = Column('基金代码', String(128), primary_key=True)
    净值日期 = Column('净值日期', Integer(), primary_key=True)
    单位净值 = Column('单位净值', Float())
    累计净值 = Column('累计净值', Float())
    日增长率 = Column('日增长率', String(128))
    申购状态 = Column('申购状态', String(128))
    赎回状态 = Column('赎回状态', String(128))
    分红送配 = Column('分红送配', String(128))


engine = create_engine(
    'mysql+pymysql://crawler:1234567Aa!@rm-wz9m5478sy8814agy1o.mysql.rds.aliyuncs.com:3306/invest',
    max_overflow=5)

DBSession = sessionmaker(bind=engine)


def init_db():
    """
    DB 初始化
    """
    Base.metadata.create_all(engine)


# 初始化爬取进度
def init_fund_proc():
    session = DBSession()
    fund_code_list = session.query(Fund.code).all()
    fund_code_list = [r[0] for r in fund_code_list]

    fund_proc_list = session.query(FundProc).all()
    fund_proc_code_list = [r.code for r in fund_proc_list]

    new_fund_proc_list = []
    for code in fund_code_list:
        if code not in fund_proc_code_list:
            new_fund_proc_list.append(
                FundProc(
                    code=code,
                    info_status=-1, info_retry=0, info_mdf=-1,
                    trend_status=-1, trend_retry=0, trend_newest=-1, trend_oldest=-1
                )
            )
    session.bulk_save_objects(new_fund_proc_list)
    session.commit()
    session.close()


def get_today_dt():
    return int(datetime.date.today().strftime('%Y%m%d'))


def get_pending_info_fund() -> List[Dict]:
    """
    获取需要爬取的基金
    """
    today = datetime.date.today()
    info_obsolete_date = today - datetime.timedelta(days=7)
    info_obsolete_dt = int(info_obsolete_date.strftime('%Y%m%d'))

    session = DBSession()
    query_info_stm = session \
        .query(FundProc) \
        .filter(
        or_(
            FundProc.info_status < 0, FundProc.info_mdf < info_obsolete_dt,
        ),
        FundProc.info_retry < 3
    ).limit(128)

    fund_pending_list = query_info_stm.all()

    fund_pending_detail = [
        {
            'code': r.code,
            'info_obsolete': r.info_status < 0 or r.info_mdf < info_obsolete_dt,
            'info_last_dt': r.info_mdf,
        }
        for r in fund_pending_list
    ]

    update = [
        {
            'code': r.code,
            'info_retry': r.info_retry + 1 if r.info_status < 0 or r.info_mdf < info_obsolete_dt else r.info_retry,
        }
        for r in fund_pending_list
    ]
    session.bulk_update_mappings(FundProc, update)
    session.commit()
    session.close()

    return fund_pending_detail


def get_pending_trend_fund() -> List[Dict]:
    """
    获取需要爬取的基金
    """

    today = datetime.date.today()
    trend_obsolete_date = today - datetime.timedelta(days=5)
    trend_obsolete_dt = int(trend_obsolete_date.strftime('%Y%m%d'))

    session = DBSession()

    query_trend_stm = session \
        .query(FundProc) \
        .filter(
        FundProc.trend_status < 0,
        FundProc.trend_retry < 3
    ).limit(512)

    fund_pending_list = query_trend_stm.all()

    fund_pending_detail = [
        {
            'code': r.code,
            'trend_obsolete': r.trend_status < 0,
            'trend_newest': r.trend_newest,
            'trend_oldest': r.trend_oldest,
        }
        for r in fund_pending_list
    ]

    update = [
        {
            'code': r.code,
            'trend_retry': r.trend_retry + 1 if r.trend_status < 0 else r.trend_retry,
        }
        for r in fund_pending_list
    ]
    session.bulk_update_mappings(FundProc, update)
    session.commit()
    session.close()

    return fund_pending_detail


def update_trend_proc_success(session, code, oldest, newest):

    fundProc = session.query(FundProc).filter(FundProc.code == code).first()

    if fundProc.trend_newest != -1 and fundProc.trend_newest > newest:
        newest = fundProc.trend_newest

    if fundProc.trend_oldest != -1 and fundProc.trend_oldest < oldest:
        oldest = fundProc.trend_oldest

    session.merge(FundProc(
        code=code, trend_status=0, trend_retry=0, trend_newest=newest, trend_oldest=oldest
    ))


def update_trend_json(session, code, date, json):
    session.merge(FundTrendJson(
        code=code, date=date, json=json
    ))


def print_fund_info_json_db():
    session = DBSession()
    r = session.query(FundInfoJson).first()
    session.close()

    print(json.dumps(json.loads(r.json), indent=2, ensure_ascii=False))


def update_trend_ob(response):
    url = response.orig_url
    page = url.split('page=')[1]
    page = int(page[0:page.find('&')])
    code = url.split('code=')[1]
    code = code[0:code.find('&')]

    total_page, data = (None, None, None)

    session = DBSession()

    for row in data:
        session.merge(FundTrend(
            基金代码=code,
            净值日期=row['净值日期'],
            单位净值=row['单位净值'],
            累计净值=row['累计净值'],
            日增长率=row['日增长率'],
            申购状态=row['申购状态'],
            赎回状态=row['赎回状态'],
            分红送配=row['分红送配'],

        ))

    max_dt = max([a['净值日期'] for a in data])

    session.merge(FundProc(code=code, trend_status=0, trend_retry=0, trend_mdf=max_dt))

    session.commit()
    session.close()

    if page < total_page:
        old_page = 'page={}'.format(page)
        new_page = 'page={}'.format(page + 1)
        new_url = url.replace(old_page, new_page)
    return {'_success': True}


if __name__ == '__main__':

    # init_db()
    init_fund_proc()
    # print(get_pending_fund())
    # print_fund_info_json_db()

    # session = DBSession()
    # update_trend_json(session, '000001', 20201230, '{}')
    # update_trend_proc_success(session, '000001', 19990101, 20201230)
    # session.commit()
