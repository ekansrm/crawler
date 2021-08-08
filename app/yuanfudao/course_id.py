import xlrd
import json

base_url = 'https://www.yuanfudao.com'

if __name__ == '__main__':
    data = xlrd.open_workbook('all_lesson.xls')
    table = data.sheets()[0]

    course_urls = set()
    for c in table.col([i.value for i in table.row(0)].index('lessonid')):
        c = str(c.value)
        if not c.isdigit():
            continue
        url = base_url + '/lessons/' + c + '.html'
        course_urls.add(url)
    course_urls = list(course_urls)

    json.dump(course_urls, open("course_urls.json", 'w'), indent=2)
