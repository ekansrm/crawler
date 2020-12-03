import os
import json
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

from finance.database import Base
from finance.database import DBSession
from finance.database import init_db
from finance.database import FundInfoJson


# noinspection NonAsciiCharacters
class FundInfo1(Base):
    __tablename__ = 'fund_info_1'
    代码 = Column('代码', String(128), primary_key=True)
    名称 = Column('名称', String(128), primary_key=True)
    类型 = Column('类型', String(128))
    规模 = Column('规模', String(128))
    风格_类型 = Column('风格_类型', String(128))
    阶段涨幅_今年以来 = Column('阶段涨幅_今年以来', String(128))
    阶段涨幅_近1周 = Column('阶段涨幅_近1周', String(128))
    阶段涨幅_近1月 = Column('阶段涨幅_近1月', String(128))
    阶段涨幅_近3月 = Column('阶段涨幅_近3月', String(128))
    阶段涨幅_近6月 = Column('阶段涨幅_近6月', String(128))
    阶段涨幅_近1年 = Column('阶段涨幅_近1年', String(128))
    阶段涨幅_近2年 = Column('阶段涨幅_近2年', String(128))
    阶段涨幅_近3年 = Column('阶段涨幅_近3年', String(128))
    经理_个数 = Column('经理_个数', String(128))
    经理_1_名字 = Column('经理_1_名字', String(128))
    经理_1_管理数量 = Column('经理_1_管理数量', String(128))
    经理_1_从业时间 = Column('经理_1_从业时间', String(128))
    经理_1_从业年均回报 = Column('经理_1_从业年均回报', String(128))
    经理_1_从业最大盈利 = Column('经理_1_从业最大盈利', String(128))
    经理_1_从业最大跌幅 = Column('经理_1_从业最大跌幅', String(128))
    经理_2_名字 = Column('经理_2_名字', String(128))
    经理_2_管理数量 = Column('经理_2_管理数量', String(128))
    经理_2_从业时间 = Column('经理_2_从业时间', String(128))
    经理_2_从业年均回报 = Column('经理_2_从业年均回报', String(128))
    经理_2_从业最大盈利 = Column('经理_2_从业最大盈利', String(128))
    经理_2_从业最大跌幅 = Column('经理_2_从业最大跌幅', String(128))
    经理_3_名字 = Column('经理_3_名字', String(128))
    经理_3_管理数量 = Column('经理_3_管理数量', String(128))
    经理_3_从业时间 = Column('经理_3_从业时间', String(128))
    经理_3_从业年均回报 = Column('经理_3_从业年均回报', String(128))
    经理_3_从业最大盈利 = Column('经理_3_从业最大盈利', String(128))
    经理_3_从业最大跌幅 = Column('经理_3_从业最大跌幅', String(128))
    风险_年化夏普比率_1年 = Column('风险_年化夏普比率_1年', String(128))
    风险_年化夏普比率_2年 = Column('风险_年化夏普比率_2年', String(128))
    风险_年化夏普比率_3年 = Column('风险_年化夏普比率_3年', String(128))


def print_header():
    return ','.join([
        '名称', '代码', '类型', '规模',
        '风格-类型',
        '阶段涨幅-今年以来', '阶段涨幅-近1周', '阶段涨幅-近1月', '阶段涨幅-近3月', '阶段涨幅-近6月', '阶段涨幅-近1年', '阶段涨幅-近2年', '阶段涨幅-近3年',
        '经理-个数',
        '经理-1-名字', '经理-1-管理数量', '经理-1-从业时间', '经理-1-从业年均回报', '经理-1-从业最大盈利', '经理-1-从业最大跌幅',
        '经理-2-名字', '经理-2-管理数量', '经理-2-从业时间', '经理-2-从业年均回报', '经理-2-从业最大盈利', '经理-2-从业最大跌幅',
        '经理-3-名字', '经理-3-管理数量', '经理-3-从业时间', '经理-3-从业年均回报', '经理-3-从业最大盈利', '经理-3-从业最大跌幅',
        '风险-年化夏普比率-1年', '风险-年化夏普比率-2年', '风险-年化夏普比率-3年'
    ])


def header():
    return [
        '名称', '代码', '类型', '规模',
        '风格_类型',
        '阶段涨幅_今年以来', '阶段涨幅_近1周', '阶段涨幅_近1月', '阶段涨幅_近3月', '阶段涨幅_近6月', '阶段涨幅_近1年', '阶段涨幅_近2年', '阶段涨幅_近3年',
        '经理_个数',
        '经理_1_名字', '经理_1_管理数量', '经理_1_从业时间', '经理_1_从业年均回报', '经理_1_从业最大盈利', '经理_1_从业最大跌幅',
        '经理_2_名字', '经理_2_管理数量', '经理_2_从业时间', '经理_2_从业年均回报', '经理_2_从业最大盈利', '经理_2_从业最大跌幅',
        '经理_3_名字', '经理_3_管理数量', '经理_3_从业时间', '经理_3_从业年均回报', '经理_3_从业最大盈利', '经理_3_从业最大跌幅',
        '风险_年化夏普比率_1年', '风险_年化夏普比率_2年', '风险_年化夏普比率_3年'
    ]

def format_row(data):
    rise_data = data['涨幅']['阶段涨幅']
    rise_data_irow = rise_data['irow']
    rise_data_icol = rise_data['icol']

    def get_rise_data(row, col):
        return rise_data['data'][rise_data_irow[row]][rise_data_icol[col]]

    risk_data = data['风险']
    risk_data_irow = risk_data['irow']
    risk_data_icol = risk_data['icol']

    def get_risk_data(row, col):
        return risk_data['data'][risk_data_irow[row]][risk_data_icol[col]]

    return [
        data['名称'], data['代码'], data['类型'], data['规模'],

        data['风格']['类型'],

        get_rise_data('区间回报', '今年以来'), get_rise_data('区间回报', '近1周'), get_rise_data('区间回报', '近1月'),
        get_rise_data('区间回报', '近3月'), get_rise_data('区间回报', '近6月'), get_rise_data('区间回报', '近1年'),
        get_rise_data('区间回报', '近2年'), get_rise_data('区间回报', '近3年'),

        str(len(data['经理'])),
        data['经理'][0]['名字'], data['经理'][0]['管理数量'], data['经理'][0]['从业时间'],
        data['经理'][0]['从业年均回报'], data['经理'][0]['从业最大盈利'], data['经理'][0]['从业最大跌幅'],
        data['经理'][1]['名字'] if len(data['经理']) >= 2 else '--',
        data['经理'][1]['管理数量'] if len(data['经理']) >= 2 else '--',
        data['经理'][1]['从业时间'] if len(data['经理']) >= 2 else '--',
        data['经理'][1]['从业年均回报'] if len(data['经理']) >= 2 else '--',
        data['经理'][1]['从业最大盈利'] if len(data['经理']) >= 2 else '--',
        data['经理'][1]['从业最大跌幅'] if len(data['经理']) >= 2 else '--',
        data['经理'][2]['名字'] if len(data['经理']) >= 3 else '--',
        data['经理'][2]['管理数量'] if len(data['经理']) >= 3 else '--',
        data['经理'][2]['从业时间'] if len(data['经理']) >= 3 else '--',
        data['经理'][2]['从业年均回报'] if len(data['经理']) >= 3 else '--',
        data['经理'][2]['从业最大盈利'] if len(data['经理']) >= 3 else '--',
        data['经理'][2]['从业最大跌幅'] if len(data['经理']) >= 3 else '--',

        get_risk_data('年化夏普比率', '1年'), get_risk_data('年化夏普比率', '2年'), get_risk_data('年化夏普比率', '3年')

    ]


def read_json_from_database(session: DBSession, row=-1):
    if row > 0:
        return [
            json.loads(r.json) for r in session.query(FundInfoJson).limit(row).all()
        ]
    else:
        return [
            json.loads(r.json) for r in session.query(FundInfoJson).all()
        ]


def write_info_to_database(session: DBSession, rows):
    for row in rows:
        rowDict = zip(header(), row)
        rowDict = {a[0]:a[1] for a in rowDict}
        session.merge(FundInfo1(**rowDict))
    session.commit()


def print_fund_csv(fund_detail_path, fund_csv_path):
    fund_detail_list = []
    for path in os.listdir(fund_detail_path):
        fund_detail_list.append(os.path.join(fund_detail_path, path))

    fund_csv = [print_header()]
    for path in fund_detail_list:
        with open(path, 'r', encoding='utf-8') as fp:
            fund_detail = json.load(fp)
            fund_csv.append(','.join(format_row(fund_detail)))

    with open(fund_csv_path, 'w', encoding='gbk') as fp:
        content = '\r'.join(fund_csv)
        fp.write(content)


if __name__ == '__main__':
    session = DBSession()
    init_db()
    info_jsons = read_json_from_database(session)
    info_rows = [
        format_row(info_json) for info_json in info_jsons
    ]
    write_info_to_database(session, info_rows)

    session.close()

