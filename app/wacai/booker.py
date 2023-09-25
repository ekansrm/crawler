import re
import os
import time
import json
import traceback
import datetime
import requests
import copy
import hashlib
import pymongo


class Booker(object):
    _token = 'WCeO2k48mBOd2o2PYLKsjDhJcnakUPGvXg9ew'

    _header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'X-Access-Token': 'WCeO2k48mBOd2o2PYLKsjDhJcnakUPGvXg9ew',
    }

    _dict_account = {
        "忻忻-现金": {
            "uuid": "432305E56ED946D48DA0973940A3A73E",
            "name": "忻忻-现金（CNY）",
            "moneyTypeId": "0",
            "moneyTypeShortName": "CNY"
        },
        "燕红-现金": {
            "uuid": "ed2d5a104e7d4ec4892226827e80613d",
            "name": "燕红-现金（CNY）",
            "moneyTypeId": "0",
            "moneyTypeShortName": "CNY"
        },
        "韦铭-现金": {
            "uuid": "92a0daaef69e462fb47b170bc85c4727",
            "name": "韦铭-现金（CNY）",
            "moneyTypeId": "0",
            "moneyTypeShortName": "CNY"
        },
        "燕红-增额寿教育金": {
            "uuid": "d05553cb29bf453395bc0bb856472394",
            "name": "燕红-增额寿教育金（0374，CNY）",
            "moneyTypeId": "0",
            "moneyTypeShortName": "CNY"
        },
        "韦铭-投资本金": {
            "uuid": "f3308f91139a4873912a5124d81b2c11",
            "name": "韦铭-投资本金（0603，CNY）",
            "moneyTypeId": "0",
            "moneyTypeShortName": "CNY"
        },
        "现金": {
            "uuid": "ff3d984451f94fe3987202102eae7858",
            "name": "现金（CNY）",
            "moneyTypeId": "0",
            "moneyTypeShortName": "CNY"
        }

    }

    _dict_book = {
        "日常账本": {
            "id": 113509541,
            "uuid": "A1BFB7D05F6C9C201225C5FDAC2F6A69",
            "name": "日常账本",
            "startDay": 1,
            "type": "NOTMP",
            "createdTime": 1482728328513,
            "bookMembers": {
                "KAMIWei": {
                    "uuid": "1",
                    "name": "KAMIWei"
                },
                "家庭公用": {
                    "uuid": "6",
                    "name": "家庭公用"
                },
                "配偶": {
                    "uuid": "2",
                    "name": "配偶"
                },
                "孩子": {
                    "uuid": "3",
                    "name": "孩子"
                },
                "父母": {
                    "uuid": "4",
                    "name": "父母"
                },
                "朋友": {
                    "uuid": "5",
                    "name": "朋友"
                },
                "Christine": {
                    "uuid": "0bfeedf7f51e469c92379bb83b4f321a",
                    "name": "Christine"
                }
            }
        },
        "大宗账本": {
            "id": 201692472,
            "uuid": "201692472",
            "name": "大宗账本",
            "startDay": 1,
            "type": "MP",
            "createdTime": 1584334531423
        },
        "项目支出": {
            "id": 206098875,
            "uuid": "63A76015EAE649FD85DB5F28EEFED91F",
            "name": "项目支出",
            "startDay": 1,
            "type": "NOTMP",
            "createdTime": 1688345463365
        }

    }

    _dict_category = {
        "日常支出": [
            {
                "categoryId": "e9417ad520cd48408667fb23bd6c1e48",
                "name": "家居家纺",
                "parentId": None,
                "categoryType": 3,
                "outgoSubTypes": None
            },
            {
                "categoryId": "10",
                "name": "餐饮",
                "parentId": None,
                "categoryType": 3,
                "outgoSubTypes": [
                    {
                        "categoryId": "352C3562BF82475F814FC0B9909C9F76",
                        "name": "下午茶",
                        "parentId": "10",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1001",
                        "name": "早餐",
                        "parentId": "10",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1002",
                        "name": "午餐",
                        "parentId": "10",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1003",
                        "name": "晚餐",
                        "parentId": "10",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1004",
                        "name": "夜宵",
                        "parentId": "10",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1008",
                        "name": "零食",
                        "parentId": "10",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1005",
                        "name": "饮料水果",
                        "parentId": "10",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1006",
                        "name": "买菜原料",
                        "parentId": "10",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1009",
                        "name": "油盐酱醋",
                        "parentId": "10",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1007",
                        "name": "餐饮其他",
                        "parentId": "10",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    }
                ]
            },
            {
                "categoryId": "11",
                "name": "交通",
                "parentId": None,
                "categoryType": 3,
                "outgoSubTypes": [
                    {
                        "categoryId": "1101",
                        "name": "打车",
                        "parentId": "11",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1102",
                        "name": "公交",
                        "parentId": "11",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1104",
                        "name": "加油",
                        "parentId": "11",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1105",
                        "name": "停车费",
                        "parentId": "11",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1103",
                        "name": "地铁",
                        "parentId": "11",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1109",
                        "name": "火车",
                        "parentId": "11",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1117",
                        "name": "长途汽车",
                        "parentId": "11",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1111",
                        "name": "飞机",
                        "parentId": "11",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1113",
                        "name": "自行车",
                        "parentId": "11",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1112",
                        "name": "船舶",
                        "parentId": "11",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1108",
                        "name": "保养维修",
                        "parentId": "11",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1106",
                        "name": "过路过桥",
                        "parentId": "11",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1107",
                        "name": "罚款赔偿",
                        "parentId": "11",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1110",
                        "name": "车款车贷",
                        "parentId": "11",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1115",
                        "name": "车险",
                        "parentId": "11",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1116",
                        "name": "驾照费用",
                        "parentId": "11",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1114",
                        "name": "交通其他",
                        "parentId": "11",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    }
                ]
            },
            {
                "categoryId": "12",
                "name": "购物",
                "parentId": None,
                "categoryType": 3,
                "outgoSubTypes": [
                    {
                        "categoryId": "1201",
                        "name": "服饰鞋包",
                        "parentId": "12",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1202",
                        "name": "家居百货",
                        "parentId": "12",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1212",
                        "name": "宝宝用品",
                        "parentId": "12",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1204",
                        "name": "化妆护肤",
                        "parentId": "12",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1211",
                        "name": "烟酒",
                        "parentId": "12",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1203",
                        "name": "电子数码",
                        "parentId": "12",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1209",
                        "name": "文具玩具",
                        "parentId": "12",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1208",
                        "name": "报刊书籍",
                        "parentId": "12",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1205",
                        "name": "珠宝首饰",
                        "parentId": "12",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1207",
                        "name": "家具家纺",
                        "parentId": "12",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1213",
                        "name": "保健用品",
                        "parentId": "12",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1206",
                        "name": "电器",
                        "parentId": "12",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1214",
                        "name": "摄影文印",
                        "parentId": "12",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1210",
                        "name": "购物其他",
                        "parentId": "12",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    }
                ]
            },
            {
                "categoryId": "13",
                "name": "娱乐",
                "parentId": None,
                "categoryType": 3,
                "outgoSubTypes": [
                    {
                        "categoryId": "1308",
                        "name": "旅游度假",
                        "parentId": "13",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1302",
                        "name": "电影",
                        "parentId": "13",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1304",
                        "name": "网游电玩",
                        "parentId": "13",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1312",
                        "name": "麻将棋牌",
                        "parentId": "13",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1306",
                        "name": "洗浴足浴",
                        "parentId": "13",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1305",
                        "name": "运动健身",
                        "parentId": "13",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1311",
                        "name": "花鸟宠物",
                        "parentId": "13",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1313",
                        "name": "聚会玩乐",
                        "parentId": "13",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1307",
                        "name": "茶酒咖啡",
                        "parentId": "13",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1301",
                        "name": "卡拉OK",
                        "parentId": "13",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1309",
                        "name": "歌舞演出",
                        "parentId": "13",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1303",
                        "name": "电视",
                        "parentId": "13",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1310",
                        "name": "娱乐其他",
                        "parentId": "13",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    }
                ]
            },
            {
                "categoryId": "14",
                "name": "医教",
                "parentId": None,
                "categoryType": 3,
                "outgoSubTypes": [
                    {
                        "categoryId": "1401",
                        "name": "医疗药品",
                        "parentId": "14",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1407",
                        "name": "挂号门诊",
                        "parentId": "14",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1408",
                        "name": "养生保健",
                        "parentId": "14",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1409",
                        "name": "住院费",
                        "parentId": "14",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1410",
                        "name": "养老院",
                        "parentId": "14",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1403",
                        "name": "学杂教材",
                        "parentId": "14",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1402",
                        "name": "培训考试",
                        "parentId": "14",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1412",
                        "name": "幼儿教育",
                        "parentId": "14",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1411",
                        "name": "学费",
                        "parentId": "14",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1406",
                        "name": "家教补习",
                        "parentId": "14",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1413",
                        "name": "出国留学",
                        "parentId": "14",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1405",
                        "name": "助学贷款",
                        "parentId": "14",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1404",
                        "name": "医教其他",
                        "parentId": "14",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    }
                ]
            },
            {
                "categoryId": "15",
                "name": "居家",
                "parentId": None,
                "categoryType": 3,
                "outgoSubTypes": [
                    {
                        "categoryId": "1a0bcbfc2f504269976294e2c7eaef62",
                        "name": "应用包月",
                        "parentId": "15",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1501",
                        "name": "手机电话",
                        "parentId": "15",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1504",
                        "name": "水电燃气",
                        "parentId": "15",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1517",
                        "name": "生活费",
                        "parentId": "15",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1511",
                        "name": "美发美容",
                        "parentId": "15",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1506",
                        "name": "住宿房租",
                        "parentId": "15",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1507",
                        "name": "材料建材",
                        "parentId": "15",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1503",
                        "name": "房款房贷",
                        "parentId": "15",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1509",
                        "name": "快递邮政",
                        "parentId": "15",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1502",
                        "name": "电脑宽带",
                        "parentId": "15",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1508",
                        "name": "家政服务",
                        "parentId": "15",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1505",
                        "name": "物业",
                        "parentId": "15",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1514",
                        "name": "税费手续费",
                        "parentId": "15",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1512",
                        "name": "保险费",
                        "parentId": "15",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1513",
                        "name": "消费贷款",
                        "parentId": "15",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1516",
                        "name": "婚庆摄影",
                        "parentId": "15",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1515",
                        "name": "漏记款",
                        "parentId": "15",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1510",
                        "name": "生活其他",
                        "parentId": "15",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    }
                ]
            },
            {
                "categoryId": "16",
                "name": "投资",
                "parentId": None,
                "categoryType": 3,
                "outgoSubTypes": [
                    {
                        "categoryId": "1610",
                        "name": "利息支出",
                        "parentId": "16",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1602",
                        "name": "保险",
                        "parentId": "16",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1603",
                        "name": "出资",
                        "parentId": "16",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1611",
                        "name": "基金",
                        "parentId": "16",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1616",
                        "name": "股票",
                        "parentId": "16",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1612",
                        "name": "P2P",
                        "parentId": "16",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1615",
                        "name": "余额宝",
                        "parentId": "16",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1614",
                        "name": "理财产品",
                        "parentId": "16",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1606",
                        "name": "投资贷款",
                        "parentId": "16",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1613",
                        "name": "银行存款",
                        "parentId": "16",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1601",
                        "name": "证券期货",
                        "parentId": "16",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1607",
                        "name": "外汇",
                        "parentId": "16",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1604",
                        "name": "贵金属",
                        "parentId": "16",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1608",
                        "name": "收藏品",
                        "parentId": "16",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1605",
                        "name": "投资其他",
                        "parentId": "16",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    }
                ]
            },
            {
                "categoryId": "17",
                "name": "人情",
                "parentId": None,
                "categoryType": 3,
                "outgoSubTypes": [
                    {
                        "categoryId": "1701",
                        "name": "礼金红包",
                        "parentId": "17",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1702",
                        "name": "物品",
                        "parentId": "17",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1708",
                        "name": "孝敬",
                        "parentId": "17",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1707",
                        "name": "请客",
                        "parentId": "17",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1709",
                        "name": "给予",
                        "parentId": "17",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1704",
                        "name": "代付款",
                        "parentId": "17",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1703",
                        "name": "慈善捐款",
                        "parentId": "17",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1705",
                        "name": "人情其他",
                        "parentId": "17",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    }
                ]
            },
            {
                "categoryId": "18",
                "name": "生意",
                "parentId": None,
                "categoryType": 3,
                "outgoSubTypes": [
                    {
                        "categoryId": "1801",
                        "name": "进货采购",
                        "parentId": "18",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1802",
                        "name": "人工支出",
                        "parentId": "18",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1803",
                        "name": "材料辅料",
                        "parentId": "18",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1808",
                        "name": "办公费用",
                        "parentId": "18",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1805",
                        "name": "交通运输",
                        "parentId": "18",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1804",
                        "name": "工程付款",
                        "parentId": "18",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1806",
                        "name": "运营费",
                        "parentId": "18",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1807",
                        "name": "会务费",
                        "parentId": "18",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1809",
                        "name": "营销广告",
                        "parentId": "18",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1810",
                        "name": "店面租金",
                        "parentId": "18",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1811",
                        "name": "注册登记",
                        "parentId": "18",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    },
                    {
                        "categoryId": "1812",
                        "name": "生意其他",
                        "parentId": "18",
                        "categoryType": 1,
                        "outgoSubTypes": None
                    }
                ]
            }
        ],
        "日常收入": [
            {
                "categoryId": "1",
                "name": "工资薪水",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "6",
                "name": "利息",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "2",
                "name": "兼职外快",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "22",
                "name": "营业收入",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "19",
                "name": "红包",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "12",
                "name": "销售款",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "18",
                "name": "退款返款",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "14",
                "name": "报销款",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "8",
                "name": "福利补贴",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "21",
                "name": "余额宝",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "11",
                "name": "应收款",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "16",
                "name": "生活费",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "7",
                "name": "奖金",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "4",
                "name": "基金",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "9",
                "name": "礼金",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "5",
                "name": "分红",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "10",
                "name": "租金",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "3",
                "name": "股票",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "17",
                "name": "公积金",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "23",
                "name": "工程款",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "20",
                "name": "赔付款",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "15",
                "name": "漏记款",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            },
            {
                "categoryId": "13",
                "name": "其他",
                "parentId": None,
                "categoryType": 2,
                "outgoSubTypes": None
            }
        ]
    }

    _dict_category_by_name = {}

    _body_expense = {
        "flows": [
            {
                "amount": 1,
                "tradetgt": {},
                "account": {
                    "key": "432305E56ED946D48DA0973940A3A73E",
                    "label": "忻忻-现金（CNY）"
                },
                "member": {
                    "key": "1",
                    "label": "KAMIWei"
                },
                "comment": "",
                "reimburse": 0,
                "tradetgtId": None,
                "tradetgtName": None,
                "accountId": "432305E56ED946D48DA0973940A3A73E",
                "bizTime": "2023-09-05T15:32:18.607Z",
                "address": "",
                "bkId": 113509541,
                "bookId": "A1BFB7D05F6C9C201225C5FDAC2F6A69",
                "categoryId": "1210",
                "edited": 0,
                "deleted": 0,
                "id": 0,
                "members": [
                    {
                        "memberId": "1",
                        "amount": 1
                    }
                ],
                "recType": 1,
                "type": None,
                "sourceSystem": 201,
                "bizId": "DDBDB73F5EEC018453BE54DB1FB810A9"
            }
        ]
    }

    _body_income = {
        "flows": [{
            "amount": 33,
            "category": {"key": "18", "label": "退款返款"},
            "tradetgt": {},
            "account": {"key": "432305E56ED946D48DA0973940A3A73E", "label": "忻忻-现金（CNY）"},
            "member": {"key": "1", "label": "KAMIWei"},
            "comment": "",
            "reimburse": 0,
            "categoryId": "18",
            "tradetgtId": None,
            "accountId": "432305E56ED946D48DA0973940A3A73E",
            "bizTime": "2023-09-11T15:32:25.579Z",
            "address": "",
            "bkId": 113509541,
            "bookId": "A1BFB7D05F6C9C201225C5FDAC2F6A69",
            "edited": 0,
            "deleted": 0,
            "id": 0,
            "members": [{"memberId": "1", "amount": 33}],
            "recType": 2,
            "type": None,
            "sourceSystem": 201,
            "bizId": "EE439684D830761E57AC3EAC9E1FCF48"
        }]}

    def __init__(self):
        self._map_category_by_name()

    def set_token(self, token):
        self._token = token

    def _time_convert(self, t_time):
        # 定义东八区的时区

        dt = datetime.datetime.strptime(t_time, '%Y-%m-%d %H:%M:%S')
        dt = dt - datetime.timedelta(hours=8)
        formatted_dt = dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')

        return formatted_dt

    def _map_category_by_name(self):
        def _map_node(node):
            self._dict_category_by_name[node['name']] = node
            if 'outgoSubTypes' in node and node['outgoSubTypes'] is not None and len(node['outgoSubTypes']) > 0:
                for s_node in node['outgoSubTypes']:
                    _map_node(s_node)

        for k, v in self._dict_category.items():
            for e in v:
                _map_node(e)

    def _build_body(self, template, book_name, member_name, category_name, account_name, amount, t_time, comment):
        account = self._dict_account[account_name]
        book = self._dict_book[book_name]
        member = self._dict_book[book_name]['bookMembers'][member_name]
        category = self._dict_category_by_name[category_name]

        token = str(account) + '#' + t_time + '#' + comment

        body = copy.deepcopy(template)

        flow = body['flows'][0]

        flow['bkId'] = book['id']
        flow['bookId'] = book['uuid']

        flow['members'] = [{
            "memberId": member['uuid'],
            "amount": amount
        }]
        flow['member'] = {
            "key": member['uuid'],
            "label": member['name']
        }

        flow['accountId'] = account['uuid']
        flow['account'] = {
            "key": account['uuid'],
            "label": account['name']
        }

        flow['amount'] = amount

        flow['categoryId'] = category['categoryId']

        flow['bizTime'] = self._time_convert(t_time)

        flow['comment'] = comment

        flow['bizId'] = hashlib.md5(token.encode()).hexdigest()

        return body

    def _commit(self, body):
        ts = str(int(datetime.datetime.now().timestamp() * 1000))
        url = 'https://www.wacai.com/activity/bkk-frontier/api/v2/flow/save?___t={0}'.format(ts)
        header = copy.deepcopy(self._header)
        header['X-Access-Token'] = self._token
        try:
            r = requests.post(url, json=body, headers=header)
            if r.status_code == 200:
                r_data = json.loads(r.text)
                if 'code' in r_data:
                    if r_data['code'] == 0:
                        return 0, 'SUCCESS'
                    else:
                        return -1, '接口返回异常, error=' + r_data['error']
                else:
                    return -1, '结果解析异常, r.text=' + str(r.text)
            else:
                return -1, '接口调用异常, status_code=' + str(r.status_code)
        except Exception as e:
            return -1, '未知异常, e=' + json.dumps(e)

    def book_income(self, book_name, member_name, category_name, account_name, amount, t_time, comment):
        body = self._build_body(self._body_income,
                                book_name, member_name, category_name, account_name, amount, t_time, comment)
        return self._commit(body)

    def book_expense(self, book_name, member_name, category_name, account_name, amount, t_time, comment):
        body = self._build_body(self._body_expense,
                                book_name, member_name, category_name, account_name, amount, t_time, comment)
        return self._commit(body)


class Fetcher(object):


    def fetch_one(self):
        record_id = 'dfdfafaf'

        record_time = 'dadfadfaf'

        record_content = '1112132312'

        return record_id, record_time, record_content


class Database(object):

    _client = None
    _db = None
    _collection_record_sms = None

    def __init__(self):
        self._client = pymongo.MongoClient(host="192.168.1.11", port=27017)
        self._db = self._client['booking']
        self._collection_record_sms = self._db['record_sms']

    def upsert_record(self, record_id, record):
        self._collection_record_sms.update_one({'_id': record_id}, {'$set': record}, upsert=True)

    def remove_record(self, record_id):
        self._collection_record_sms.delete_many({'_id': record_id})

    def find_success_record(self, n):
        cursor = self._collection_record_sms.find({'code': 0}).sort([('time', pymongo.DESCENDING)]).limit(n)
        return [r for r in cursor]

    def find_failure_record(self, n):
        cursor = self._collection_record_sms.find({'code': {'$ne': 0}}).sort([('time', pymongo.DESCENDING)]).limit(n)
        return [r for r in cursor]


class Service(object):

    _database: Database = None

    _booker: Booker = None

    _fetcher: Fetcher = None

    _book_name = '日常账本'

    _member_name = 'KAMIWei'

    _account_name = '现金'

    def __init__(self):
        self._booker = Booker()

        self._fetcher = Fetcher()

        self._database = Database()

    def set_token(self, token):
        self._booker.set_token(token)

    def parse(self, content):
        t_time = '2023-09-22 09:11:22'
        amount = 123
        record_type = 'income'
        comment = '中文测试'
        return {
            'type': record_type,

            'category_name': '退款返款',
            't_time': t_time,
            'amount': amount,
            'comment': comment
        }

    def handle(self, record):

        record_id = record['uid']
        record_time = record['time']
        record_content = record['content']

        try:
            result = self.parse(record_content)
            record.update(result)
            
        except Exception as e:
            record['code'] = -1
            record['message'] = 'parse 异常'
            self._database.upsert_record(record_id, record)
            return

        if record['type'] == 'income':
            code, message = self._booker.book_income(
                book_name=self._book_name,
                member_name=self._member_name,
                account_name=self._account_name,
                category_name=record['category_name'],
                amount=record['amount'],
                t_time=record['t_time'],
                comment=record['comment'],
            )

            if code != 0:
                record['code'] = code
                record['message'] = message
            else:
                record['code'] = 0
                record['message'] = 'SUCCESS'

            self._database.upsert_record(record_id, record)

    def collect_next(self):

        record_id, record_time, record_content = self._fetcher.fetch_one()

        record = {
            'uid': record_id,
            'time': record_time,
            'content': record_content,
        }

        self.handle(record)


if __name__ == '__main__':
    # crawler = Booker()
    #
    # crawler.set_token('WCeO2k48mBOd2o2PYLKsjDhJcnakUPGvXg9ew')
    #
    # crawler.book_expense(book_name='日常账本',
    #                      member_name='KAMIWei',
    #                      account_name='现金',
    #                      category_name='宝宝用品',
    #                      amount=123,
    #                      t_time='2023-09-22 09:11:22',
    #                      comment='中文测试')
    #
    # crawler.book_income(book_name='日常账本',
    #                     member_name='KAMIWei',
    #                     account_name='现金',
    #                     category_name='退款返款',
    #                     amount=123,
    #                     t_time='2023-09-11 18:11:22',
    #                     comment='中文测试, 这是退款')

    service = Service()

    service.set_token('WCeO2k48mBOd2o2PYLKsjDhJcnakUPGvXg9ew')

    service.collect_next()
