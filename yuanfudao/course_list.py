import time
import json
from tqdm import tqdm
from pyquery import PyQuery as pq

# cookies_str = "optimizelyEndUserId=oeu1532569713196r0.5975193584464786; optimizelyBuckets=%7B%7D; _omappvp=t5KWuZJmchi5h9UStyGxdHqWeZm7zoDxtj025iSFkbr15f9vksRxNFoAoqpIoW2NmbGtAYKhz0hNTMXNvfFDa9woAq4B3z7n; RETURNING_VISITOR=true; _ga=GA1.2.486250441.1532569759; mp_dd81b79ad7bab9bd2b685a3a0116b034_mixpanel=%7B%22distinct_id%22%3A%20%2216589c52526184-0b8d9341b66dbc-39614807-1fa400-16589c52527a9b%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; dzuuid=4b969672-a28e-42b3-98ce-a3f5af0e8d4d; optimizelySegments=%7B%221595101009%22%3A%22search%22%2C%221596781023%22%3A%22gc%22%2C%221600230999%22%3A%22false%22%7D; om-yxqxn52jp9zs07u4yiiz=1542331371387; om-v2ztbriq3nusgrkbecgs=1542935065090; om-swx8od5qaum1mtdbq7qe=1543195953567; om-opcsulqohj0tavq2h6jz=1543886759910; om-usqx9tg38wzb4ryhav4e=1544146221698; _gid=GA1.2.818963861.1544419202; om-qwze5lkdfy9n0i0ot95z=1544419212326; om-eyoq6nv3nk6ofwa3rhzz=1544506362734; om-ptk1txj64xvw4x4u9hug=1544664416098; omGlobalInteractionCookie=1544664416098; JSESSIONID=B538BB9E5D53295F16C16C5B42BC399E; TH_CSRF=3847428072419124801; SPRING_SECURITY_REMEMBER_ME_COOKIE=U3RzVEhDK0tWcGtTMmtWMGlHNU5sQT09OmFVNmM2bndyc01WQm5DSUFZNVVwL3c9PQ; AWSELB=2B23F73512874A984846CB61011FAE4304C7C410AC6D2BD8DA2DA380073EAD554E22B9735186545710CBA36F8982913695204F268C6CA1DCA47DC66D55D9FAB03E146CDB7B; SESSION_STARTED=true; _parsely_session={%22sid%22:66%2C%22surl%22:%22https://dzone.com/%22%2C%22sref%22:%22%22%2C%22sts%22:1544706726907%2C%22slts%22:1544664405949}; _parsely_visitor={%22id%22:%22d86d7bdb-a3f9-49d5-862c-120107c28d4c%22%2C%22session_count%22:66%2C%22last_session_ts%22:1544706726907}; __insp_wid=1999343779; __insp_nv=true; __insp_targlpu=aHR0cHM6Ly9kem9uZS5jb20v; __insp_targlpt=RFpvbmU6IFByb2dyYW1taW5nICYgRGV2T3BzIG5ld3MsIHR1dG9yaWFscyAmIHRvb2xz; __insp_norec_sess=true; mp_022d397c8f6bfc6c6b289f607d96fc84_mixpanel=%7B%22distinct_id%22%3A%20%22165a9739dc144e-02caad40b36c9c-39614807-1fa400-165a9739dc24cc%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22%24search_engine%22%3A%20%22google%22%7D; __insp_slim=1544706794125; _gali=ng-app"
# cookies = dict({key.strip(): val.strip() for key, val in [item.split("=") for item in cookies_str.split(";")]})

headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 "
                  "Safari/537.36",
    "Host": "www.yuanfudao.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
}

base_url = 'https://www.yuanfudao.com'
list_url = base_url + '/?keyfrom=apeOfficialWebsite&vendor=apeOfficialWebsite&grade={0}&channelId={1}&count=1000'

if __name__ == '__main__':

    group_grade_cata = [
        (100, 2),
        (1, 0),
        (2, 0),
        (3, 0),
        (4, 0),
        (5, 0),
        (6, 0),
        (7, 0),
        (8, 0),
        (9, 0),
        (10, 0),
        (11, 0),
        (12, 0),
    ]

    group_urls = set()
    course_urls = set()

    for g in tqdm(group_grade_cata):

        page_top = list_url.format(*g)

        doc = pq(url=page_top)

        courses_docs = []

        course_doc = doc("""a[href^="/lessons/"][href$="html"]""")
        courses_docs.append(course_doc)

        group_doc = doc("""a[href^="/lessons/group"]""")
        for i in range(0, group_doc.length):
            sub_url = group_doc.eq(i).attr("href")
            group_urls.add(sub_url)

        for sub_url in group_urls:
            group_doc = pq(url=base_url + sub_url)
            course_doc = group_doc("""a[href^="/lessons/"]""")
            courses_docs.append(course_doc)
            time.sleep(0.1)

        for course_doc in courses_docs:
            for i in range(0, course_doc.length):
                sub_url = course_doc.eq(i).attr("href")
                course_urls.add(sub_url)

        time.sleep(0.1)

    course_urls = list([base_url + sub_url for sub_url in course_urls])

    # print(json.dumps(course_urls, indent=2))

    json.dump(course_urls, open("course_urls.json", 'w'), indent=2)

