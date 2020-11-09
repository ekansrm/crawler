from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Fund(Base):
    __tablename__ = 'fund'
    code = Column('code', String(128), primary_key=True)


class FundCrawlerProc(Base):
    __tablename__ = 'fund_crawler_proc'
    code = Column('code', String(128), primary_key=True)
    info_status = Column('info_status', Integer())
    info_mdf = Column('info_mdf', Integer())
    trend_status = Column('trend_status', Integer())
    trend_mdf = Column('trend_mdf', Integer())


engine = create_engine(
    'mysql+pymysql://crawler:1234567Aa!@rm-wz9m5478sy8814agy1o.mysql.rds.aliyuncs.com:3306/invest',
    max_overflow=5)

DBSession = sessionmaker(bind=engine)

if __name__ == '__main__':
    session = DBSession()

    Base.metadata.create_all(engine)

    fund_prod = FundCrawlerProc(code='111111', info_status=0, info_mdf=20201109)
    fund = Fund(code='1234567')
    session.merge(fund)
    session.merge(fund_prod)
    # 添加到session
    # 提交
    session.commit()
    # 关闭session
    session.close()
