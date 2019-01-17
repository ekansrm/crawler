import time
import json
from tqdm import tqdm
from pyquery import PyQuery as pq


def parse_detail(course_url: str) -> map:

    doc = pq(url=course_url)

    course_name = doc("""label[class="course-name"]""").text()
    course_price = doc("""em[class="price-num"]""").text()
    course_time = doc("""p[class="time"]""").text()
    course_fit = doc("""p[class="fit"]""").text()

    teacher_infos = doc("""div[class="teacher-credentials"]""")
    teacher_name = teacher_infos.children("""p[class="name"]""").text()

    teacher_credential = []
    teacher_span = teacher_infos.children("""p[class="credentials"]""")
    for i in range(0, teacher_span.length):
        teacher_credential.append(teacher_span.eq(i).text())
    teacher_credential = "|".join(teacher_credential)

    return {
        'course_url': course_url,
        'course_name': course_name,
        'course_time': course_time,
        'course_fit': course_fit,
        'course_price': course_price,
        'teacher_name': teacher_name,
        'teacher_credential': teacher_credential,
    }


if __name__ == '__main__':

    with open('course_urls.json', 'r') as fp:
        course_urls = json.load(fp)

    course_details = []
    for url in tqdm(course_urls):
        # noinspection PyBroadException
        try:
            course_details.append(parse_detail(url))
            time.sleep(0.1)
        except Exception as e:
            print("error occurs!")

    json.dump(course_details, open("course_details.json", 'w'), indent=2, ensure_ascii=False)





