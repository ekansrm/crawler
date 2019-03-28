import json
import requests
from pyquery import PyQuery as pq
import os


def _get_img_url(doc):
    img_url = doc("""img[class="img-fluid"][src^="/ccbaike"]""").attr('src')
    return img_url


def _save_img(vol_dir, img_url):
    filename = img_url.split('/')[-1]
    filepath = os.path.join(vol_dir, filename)
    if os.path.exists(filepath):
        return
    loop = 0
    while True:
        try:
            with open(filepath, 'wb') as fp:
                r = requests.get(img_url, timeout=10)
                fp.write(r.content)
                break
        except Exception as e:
            print(e)
            loop = loop + 1
        if loop >= 3:
            raise RuntimeError("can not download " + img_url)


def _get_vol_name(doc):
    vol_name = doc("""h2[class~="text-center"]""").text()
    return vol_name


def _get_next_page_url(doc):
    next_url = doc("""a[id="right"]""").attr('href')

    # 这一章已经完成
    if 'goNumPage' in next_url:
        next_url = None
    return next_url


def get_book_details(base_dir, base_url, book_url):
    doc = pq(url=base_url + book_url)

    vol_name = _get_vol_name(doc)
    vol_dir = os.path.join(os.getcwd(), base_dir, vol_name)
    if not os.path.exists(vol_dir):
        os.mkdir(vol_dir)

    total_pages = []
    fail_pages = []

    while True:
        img_url = _get_img_url(doc)
        print("processing " + img_url)
        try:
            total_pages.append(img_url)
            _save_img(vol_dir, base_url + img_url)
            next_url = _get_next_page_url(doc)
            if next_url is None:
                break
            doc = pq(url=base_url + next_url)
        except Exception as e:
            fail_pages.append(img_url)

    with open(os.path.join(vol_dir, "total.json"), 'w') as fp:
        json.dump(total_pages, fp, indent=2)

    with open(os.path.join(vol_dir, "fail.json"), 'w') as fp:
        json.dump(fail_pages, fp, indent=2)


if __name__ == '__main__':
    with open("铳梦.json", 'r') as fp:
        infos = json.load(fp)

    base_dir = '铳梦'
    base_url = 'https://www.manhuadb.com'
    fail_url = []
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    for info in infos:
        title = info['title']
        book_urls = info['list']
        book_urls.reverse()
        book_base_dir = os.path.join(base_dir, title)
        if not os.path.exists(book_base_dir):
            os.mkdir(book_base_dir)
        for book_url in book_urls:
            print("processing " + title + " " + book_url)
            try:
                get_book_details(os.path.join(base_dir, title), base_url, book_url)
            except Exception as e:
                print(e)
                fail_url.append(book_url)

    print("fail url= " + json.dumps(fail_url, indent=2))
