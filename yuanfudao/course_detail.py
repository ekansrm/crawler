import time
import json
import traceback
import trace
from tqdm import tqdm
from pyquery import PyQuery as pq

base_url = 'https://www.yuanfudao.com'

def parse_detail(course_url: str) -> map:

    doc = pq(url=course_url)

    course_name = doc("""h3[class="name"]""").text()

    course_price = doc("""em[id="J_Price"]""").text()
    if not course_price.isdigit():
        course_price = doc("""div[class="price"] strong""").text()

    course_time = doc("""p[class="sub-name"]""").text()
    course_fit = doc("""p[class="features"]""").text()
    course_quota = doc("""p[id="J_QuotaDesc"]""").text()
    teacher_name = doc("""a[href^="/teachers"] p""").text()
    teacher_url = doc("""a[href^="/teachers"]""").attr('href')
    if teacher_url is not None:
        teacher_url = base_url + teacher_url
    else:
        teacher_url = "null"

    return {
        'course_url': course_url,
        'course_name': course_name,
        'course_time': course_time,
        'course_fit': course_fit,
        'course_price': course_price,
        'course_quota': course_quota,
        'teacher_name': teacher_name,
        'teacher_url': teacher_url,
        # 'teacher_credential': teacher_credential,
    }


if __name__ == '__main__':

    # course_urls = [
    #     'https://www.yuanfudao.com/lessons/3080946.html',
    #     'https://www.yuanfudao.com/lessons/3079554.html',
    #     'https://www.yuanfudao.com/lessons/3092234.html',
    # ]

    with open('course_urls.json', 'r') as fp:
        course_urls = json.load(fp)

    course_details = []
    i = 0
    for url in tqdm(course_urls):
        # noinspection PyBroadException
        try:
            course_details.append(parse_detail(url))
            i += 1
            if i % 20 == 0:
                json.dump(course_details, open("course_details.json", 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
            time.sleep(0.02)
        except Exception as e:
            traceback.print_tb(e)
            print("error occurs!")

    # print(json.dumps(course_details, indent=2, ensure_ascii=False))
    json.dump(course_details, open("course_details.json", 'w', encoding='utf-8'), indent=2, ensure_ascii=False)





