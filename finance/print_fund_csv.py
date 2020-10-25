import os
import json


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


def print_row(data):
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

    return ','.join([
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

    ])


def print_fund_csv(fund_detail_path, fund_csv_path):
    fund_detail_list = []
    for path in os.listdir(fund_detail_path):
        fund_detail_list.append(os.path.join(fund_detail_path, path))

    fund_csv = [print_header()]
    for path in fund_detail_list:
        with open(path, 'r', encoding='utf-8') as fp:
            fund_detail = json.load(fp)
            fund_csv.append(print_row(fund_detail))

    with open(fund_csv_path, 'w', encoding='gbk') as fp:
        content = '\r'.join(fund_csv)
        fp.write(content)


if __name__ == '__main__':
    print_fund_csv(os.path.join('data', 'fund_info'), os.path.join('data', 'fund.csv'))
