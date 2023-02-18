import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyquery import PyQuery as pq
from utils.fs import FsRowDict, build_fill_zero


class Crawler(object):
    _base_dir = ''
    _base_id = ''
    _session = None
    _row_dict = None

    @staticmethod
    def base_url():
        return 'https://mangabz.com'

    def __init__(self, base_dir, base_id):
        self._base_dir = base_dir
        self._base_id = base_id
        self._row_dict = FsRowDict(os.path.join(base_dir, 'all.json'))

    def crawl_book(self, refresh=False, interval=0.02):
        url = Crawler.base_url() + '/' + self._base_id + '/'
        doc = pq(url)
        column_list_doc = doc("""div[id~="chapterlistload"]""")
        columns_doc = column_list_doc.children()

        u = 10
        i = 0
        column_page_num_pattern = re.compile(r'\s*（(\d+)P）')
        for j in range(0, columns_doc.length):
            column_doc = columns_doc.eq(j)

            column_url = column_doc.attr('href').strip('/')

            column_title_raw = column_doc.text()
            column_page_num_match = re.search(column_page_num_pattern, column_title_raw)
            if column_page_num_match is None:
                continue
            column_page_num = int(column_page_num_match.group(1))
            column_title = re.sub(column_page_num_pattern, '', column_title_raw)

            # 将书籍信息合并到字典里
            column_info = self._row_dict.select(column_url)
            column_info['href'] = column_url

            if 'title' not in column_info:
                column_info['title'] = column_title

            if 'page_num' not in column_info:
                column_info['page_num'] = column_page_num

            if 'pages' not in column_info:
                column_info['pages'] = {}
            self._row_dict.upsert(column_url, column_info)

            i += 1
            if i >= u:
                i = 0
                self._row_dict.commit()

    def download_column(self, refresh=False, interval=0.02):
        all_columns = self._row_dict.select_all()

        for column_href in all_columns:
            column_info = all_columns[column_href]
            column_page_num = column_info['page_num']
            column_url = Crawler.base_url() + '/' + column_href + '/'
            column_pages = column_info['pages']

            page_zero_filler = build_fill_zero(column_page_num)

            for i in range(1, column_page_num+1):
                page_url = column_url + '#ipg{0}'.format(i)
                pad_idx = page_zero_filler(i)
                page_doc = pq(page_url)
                page_img_doc = page_doc("""img[id="cp_image"]""")
                print(page_img_doc)


    def test(self):
        options = Options()
        options.binary_location = "./chromedriver.exe"
        driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')  # Chrome浏览器
        driver.get("www.baidu.com")
        print(123)


if __name__ == '__main__':

    crawler = Crawler(os.path.join('.', '_rst', 'mangabz', '辉夜姬想让人告白~天才们的恋爱头脑战'), '60bz')
    # crawler.crawl_book(interval=0.01)
    # crawler.download_column()
    crawler.test()




