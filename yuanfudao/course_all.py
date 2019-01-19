# 导入模块
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

# 定义主域名
domain = 'https://www.yuanfudao.com'

# 定义主info表
info = {'grade': [], 'channelid': [], 'lessonid': [], 'lessonurl': [], 'lessonname': []}

# 定义主页面筛选表
gradeList = range(1, 13)
urlList = {
    1: [3],
    2: [3],
    3: [3],
    4: [3, 201],
    5: [3, 201],
    6: [3, 201],
    7: [1, 2, 3, 7, 8],
    8: [1, 2, 3, 4, 5, 7, 8],
    9: [1, 2, 3, 4, 5, 7, 8, 14],
    10: [1, 2, 3, 4, 5, 6, 7, 8, 9],
    11: [1, 2, 3, 4, 5, 6, 7, 8, 9],
    12: [1, 2, 3, 4, 5, 6, 7, 8, 9]
}

# 获取每个主页面系统课的info：
for grade in gradeList:
    for channelid in urlList[grade]:
        main_url = 'https://www.yuanfudao.com/?grade=%i&channelId=%i&count=80' % (grade, channelid)
        res1 = requests.get(main_url)
        soup1 = BeautifulSoup(res1.text, 'html.parser')
        # 循环取出group相关的信息
        for Class in soup1.select('.group h3'):
            groupurl = domain + Class.select('a')[0]['href']
            res2 = requests.get(groupurl)
            soup2 = BeautifulSoup(res2.text, 'html.parser')
            # 循环取出每个groupurl，即课程下面的课程信息
            for classlist in soup2.select('li h3'):
                info['lessonid'].append(classlist.select('a')[0]['href'][9:16])
                info['lessonurl'].append(domain + classlist.select('a')[0]['href'])
                info['lessonname'].append(classlist.select('a span')[0].text)
                info['grade'].append(grade)
                info['channelid'].append(channelid)
# 利用有序字典导入DataFrame
infoOrderDict = OrderedDict(info)
infoDf = pd.DataFrame(infoOrderDict)
infoDf.head()

# 获取每个主页面专题/讲座/无groupid的系统班的info：
for grade in gradeList:
    for channelid in urlList[grade]:
        main_url = 'https://www.yuanfudao.com/?grade=%i&channelId=%i&count=80' % (grade, channelid)
        res1 = requests.get(main_url)
        soup1 = BeautifulSoup(res1.text, 'html.parser')
        # 循环取数据
        for Class in soup1.select('.lesson-box'):
            # 判断是否为讲座类
            if Class.select('h2')[0].text == '讲座':
                for seminar in Class.select('h3'):
                    info['lessonname'].append(seminar.select('span')[0].text)
                    info['lessonurl'].append(domain + seminar.select('a')[0]['href'])
                    info['lessonid'].append(seminar.select('a')[0]['href'][9:16])
                    info['grade'].append(grade)
                    info['channelid'].append(channelid)
                # 判断是否为专题类
            elif Class.select('h2')[0].text == '专题课':
                for subject in Class.select('h3'):
                    info['lessonname'].append(subject.select('span')[0].text)
                    info['lessonurl'].append(domain + subject.select('a')[0]['href'])
                    info['lessonid'].append(subject.select('a')[0]['href'][9:16])
                    info['grade'].append(grade)
                    info['channelid'].append(channelid)
            elif Class.select('h2')[0].text == '系统班':
                for subject in Class.select('h3'):
                    info['lessonname'].append(subject.select('span')[0].text)
                    info['lessonurl'].append(domain + subject.select('a')[0]['href'])
                    info['lessonid'].append(subject.select('a')[0]['href'][9:16])
                    info['grade'].append(grade)
                    info['channelid'].append(channelid)
# 利用有序字典导入DataFrame
infoOrderDict = OrderedDict(info)
infoDf = pd.DataFrame(infoOrderDict)
infoDf.head()

# 导出数据至xls
infoDf.to_excel('all_lesson.xls')

# 定义课程表
info_class = {'lesson_id': [], 'price': [], 'signup_number': []}

# 爬取所有课的课程表
for url in info['lessonurl']:
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    # 对课程里的“已报满”课程进行单独处理
    if soup.select('.price em')[0].text == '已报满':
        info_class['lesson_id'].append(url[-12:-5])
        info_class['price'].append(soup.select('.price')[0].text[: soup.select('.price')[0].text.index('已')])
        info_class['signup_number'].append(soup.select('.common-num')[0].text)
    else:
        info_class['lesson_id'].append(url[-12:-5])
        info_class['price'].append(soup.select('.price em')[0].text)
        info_class['signup_number'].append(soup.select('.common-num')[0].text)

# 利用有序字典导入DataFrame
infoOrderDict = OrderedDict(info_class)
infoclassDf = pd.DataFrame(infoOrderDict)
infoclassDf.head()

# 导出课程表
infoclassDf.to_excel('lesson_detail.xls')

# 定义教师表
info_teacher = {'lesson_id': [], 'teacher_id': [], 'teacher_name': []}

# 爬取所有课程的教师表
for url in info['lessonurl']:
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    for teacher in soup.select('.horizontal li'):
        info_teacher['teacher_name'].append(teacher.select('a')[0].text)
        begin = teacher.select('a')[0]['href'].index('/', 2)
        end = teacher.select('a')[0]['href'].index('/', 12)
        info_teacher['teacher_id'].append(teacher.select('a')[0]['href'][begin + 1:end])
        info_teacher['lesson_id'].append(url[-12:-5])
# 利用有序字典导入DataFrame
infoOrderDict = OrderedDict(info_teacher)
infoteacherDf = pd.DataFrame(infoOrderDict)
infoteacherDf.head()

# 导出教师表
infoteacherDf.to_excel('teacher_detail.xls')
