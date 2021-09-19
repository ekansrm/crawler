import time
import json
from tqdm import tqdm
import requests
from pyquery import PyQuery as pq
import os
from utils.fs import FsRowDict
from utils.img import download_img


class Crawler(object):
    _base_dir = ''
    _session = None
    _row_dict = None

    @staticmethod
    def base_url():
        return 'https://www.manhuadb.com'

    @staticmethod
    def manhua_url(bid):
        return Crawler.base_url() + '/manhua/' + bid

    @staticmethod
    def _get_img_url(doc):
        img_url = doc("""img[class="img-fluid show-pic"]""").attr('src')
        return img_url

    @staticmethod
    def _get_vol_name(doc):
        vol_name = doc("""h2[class~="text-center"]""").text()
        return vol_name


    @staticmethod
    def _get_next_page_url(doc):
        next_url = doc("""a[id="right"]""").attr('href')

        # 这一章已经完成
        if 'goNumPage' in next_url:
            next_url = None
        return next_url


    @staticmethod
    def get_book_details(book_url):
        url = Crawler.base_url() + book_url
        doc = pq(url=url)

        total_pages = []
        fail_pages = []


        while True:
            img_url = Crawler._get_img_url(doc)
            print("processing " + img_url)
            try:
                total_pages.append(img_url)
                download_img(img_url, '.')

                # _save_img(vol_dir, base_url + img_url)
                next_url = Crawler._get_next_page_url(doc)
                if next_url is None:
                    break
                doc = pq(url=Crawler.base_url() + next_url)
            except Exception as e:
                fail_pages.append(img_url)

    @staticmethod
    def _get_book_id_title_list(keyword):
        url = Crawler.base_url() + '/search?q=' + keyword
        doc = pq(url)
        book_list_doc = doc("""a[class="d-block"]""")
        book_list = [(e.attr('href').split('/')[-1], e.attr('title'), ) for e in book_list_doc.items()]
        return book_list


    @staticmethod
    def _get_book_info(bid):
        url = Crawler.manhua_url(bid)
        doc = pq(url)

        book_info_title_doc = doc("""h3[class~="comic_version_title"]""")
        book_info_list_doc = doc("""ol[class~="links-of-books"]""")

        # 可能有番外篇、单行本什么的
        book_info = {}
        for i in range(0, book_info_list_doc.length):
            version = book_info_title_doc.eq(i).text()
            title = version[version.find('[') + 1:version.find(']')]
            columns_doc = book_info_list_doc.eq(i).children()
            columns = {}
            for j in range(0, columns_doc.length):
                column_url = columns_doc.eq(j).children().attr('href')
                column_title = columns_doc.eq(j).children().attr('title')
                columns[column_url] = {
                    'title': column_title,
                    'url': column_url,

                }

            book_info[version] = {
                'title': title,
                'version': version,
                'columns': columns
            }

        return book_info

    def __init__(self, base_dir):
        self._base_dir = base_dir
        self._row_dict = FsRowDict(os.path.join(base_dir, 'all.json'))

    def get_book_info_by_keyword(self, keyword):

        book_list = Crawler._get_book_id_title_list(keyword)
        pbar = tqdm(book_list)
        i = 0
        u = 1
        rv = {}
        for b_id, b_title in pbar:
            pbar.set_description('抓取详情 {0}(id={1})'.format(b_id, b_title))
            _row = Crawler._get_book_info(b_id)
            rv[b_id] = _row
            self._row_dict.upsert(b_id, _row)

            i += 1
            if i >= u:
                i = 0
                self._row_dict.commit()

        self._row_dict.commit()


    def get_book_download(self, reflesh=False):

        all_book = self._row_dict.select_all()

        for bid in all_book:
            books = all_book[bid]
            for book_id in books:
                book = books[book_id]
                columns = book['columns']
                for column_id in columns:
                    column = columns[column_id]
                    column_url = column['url']
                    column_title = column['title']

                    Crawler.get_book_details(column_url)













if __name__ == '__main__':
    # url = 'https://www.manhuadb.com/manhua/3481'
    # book_info = get_book_info(pq(url))
    # with open("铳梦-火星战记.json", 'w') as fp:
    #     json.dump(book_info, fp, indent=2)
    #
    # url = 'https://www.manhuadb.com/manhua/369'
    # book_info = get_book_info(pq(url))
    # with open("铳梦-LastOrder.json", 'w') as fp:
    #     json.dump(book_info, fp, indent=2)
    #
    # url = 'https://www.manhuadb.com/manhua/370'
    # book_info = get_book_info(pq(url))
    # with open("铳梦.json", 'w') as fp:
    #     json.dump(book_info, fp, indent=2)
    # get_book_list('伊藤润二')

    base_dir = os.path.join('.', '_rst', 'manhuadb')
    crawler = Crawler(base_dir)
    # crawler.get_book_info_by_keyword('伊藤润二')
    crawler.get_book_download()
    # Crawler._get_book_info('3481')

