from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
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
    trend_mdf = Column('trend_mdf', Integer())
    trend_retry = Column('trend_retry', Integer(), default=0)


class FundInfoJson(Base):
    __tablename__ = 'fund_info_json'
    code = Column('code', String(128), primary_key=True)
    type = Column('type', String(128), default='standard')
    json = Column('json', LONGTEXT(), default='{}')


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
                FundProc(code=code, info_status=-1, info_retry=0, info_mdf=-1, trend_status=-1, trend_retry=0, trend_mdf=-1)
            )
    session.bulk_save_objects(new_fund_proc_list)
    session.commit()
    session.close()


def get_today_dt():
    return int(datetime.date.today().strftime('%Y%m%d'))


def get_pending_fund() -> List[Dict]:
    """
    获取需要爬取的基金
    """
    today = datetime.date.today()
    info_obsolete_date = today - datetime.timedelta(days=3)
    trend_obsolete_date = today - datetime.timedelta(days=5)
    info_obsolete_dt = int(info_obsolete_date.strftime('%Y%m%d'))
    trend_obsolete_dt = int(trend_obsolete_date.strftime('%Y%m%d'))

    session = DBSession()
    query_info_stm = session \
        .query(FundProc) \
        .filter(
            or_(
                    FundProc.info_status < 0, FundProc.info_mdf < info_obsolete_dt,
            ),
            FundProc.info_retry < 3
        ).limit(128)

    query_trend_stm = session \
        .query(FundProc) \
        .filter(
            or_(
                FundProc.trend_status < 0, FundProc.trend_mdf < trend_obsolete_dt,
            ),
            FundProc.trend_retry < 3
        ).limit(128)

    fund_pending_list = query_info_stm.all()

    fund_pending_detail = [
        {
            'code': r.code,
            'info_obsolete': r.info_status < 0 or r.info_mdf < info_obsolete_dt,
            'info_last_dt': r.info_mdf,
            'trend_obsolete': r.trend_status < 0 or r.trend_mdf < trend_obsolete_dt,
            'trend_last_dt': r.trend_mdf,
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


def print_fund_info_json_db():

    session = DBSession()
    r = session.query(FundInfoJson).first()
    session.close()

    print(json.dumps(json.loads(r.json), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    init_db()
    init_fund_proc()
    print(get_pending_fund())
    # print_fund_info_json_db()
