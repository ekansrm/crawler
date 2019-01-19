import time
import json
from tqdm import tqdm
from pyquery import PyQuery as pq
import requests
from utils.utils import load_cookies

headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 "
                  "Safari/537.36",
    "Host": "www.yuanfudao.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
}

base_url = 'https://www.yuanfudao.com'

if __name__ == '__main__':

    with open('course_details.json', 'r') as fp:
        course_details = json.load(fp)


    cookies = load_cookies('cookies.txt')[0]


    # with open('course_urls.json', 'r') as fp:
    #     course_urls = json.load(fp)

    for course in tqdm(course_details):

        url = course['teacher_url'].split('/lesson')[0]
        response = requests.post('https://www.yuanfudao.com/teachers/39413413/lessonList', headers=headers, cookies=cookies)

        doc = pq(url='https://www.yuanfudao.com/teachers/39413413/lesson', headers=headers)

        courses_docs = []

        course_doc = doc("""a[href$="html"]""")
        courses_docs.append(course_doc)
        #
        # group_doc = doc("""a[href^="/lessons/group"]""")
        # for i in range(0, group_doc.length):
        #     sub_url = group_doc.eq(i).attr("href")
        #     group_urls.add(sub_url)
        #
        # for sub_url in group_urls:
        #     group_doc = pq(url=base_url + sub_url)
        #     course_doc = group_doc("""a[href^="/lessons/"]""")
        #     courses_docs.append(course_doc)
        #     time.sleep(0.1)
        #
        # for course_doc in courses_docs:
        #     for i in range(0, course_doc.length):
        #         sub_url = course_doc.eq(i).attr("href")
        #         course_urls.add(sub_url)

        time.sleep(0.1)
        break

    course_urls = list([base_url + sub_url for sub_url in course_urls])

    print(json.dumps(course_urls, indent=2))

    # json.dump(course_urls, open("course_urls.json", 'w'), indent=2)

