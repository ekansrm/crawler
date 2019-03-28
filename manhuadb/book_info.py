import time
import json
from tqdm import tqdm
import requests
from pyquery import PyQuery as pq
import os


def get_book_info(doc):
    book_info_title_doc = doc("""h3[class~="comic_version_title"]""")
    book_info_list_doc = doc("""ol[class~="links-of-books"]""")

    book_info = []
    for i in range(0, book_info_list_doc.length):
        book_title = book_info_title_doc.eq(i).text()
        book_list_doc = book_info_list_doc.eq(i).children()
        book_list = []
        for j in range(0, book_list_doc.length):
            book_url = book_list_doc.eq(j).children().attr('href')
            book_list.append(book_url)
        book_info.append({'title': book_title, 'list': book_list})
    return book_info


if __name__ == '__main__':
    url = 'https://www.manhuadb.com/manhua/3481'
    book_info = get_book_info(pq(url))
    with open("铳梦-火星战记.json", 'w') as fp:
        json.dump(book_info, fp, indent=2)

    url = 'https://www.manhuadb.com/manhua/369'
    book_info = get_book_info(pq(url))
    with open("铳梦-LastOrder.json", 'w') as fp:
        json.dump(book_info, fp, indent=2)

    url = 'https://www.manhuadb.com/manhua/370'
    book_info = get_book_info(pq(url))
    with open("铳梦.json", 'w') as fp:
        json.dump(book_info, fp, indent=2)
