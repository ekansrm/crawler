import time
import json
from tqdm import tqdm
import requests
from pyquery import PyQuery as pq
import os
from utils.fs import FsRowDict, build_fill_zero
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
    def get_book_details(book_url, interval=0.1):
        url = Crawler.base_url() + book_url
        url_format = url.replace('.html', '') + '_p{0}.html'
        doc = pq(url=url)

        page_select_doc = doc('div[data-page]')
        total_page_num = int(page_select_doc.attr('data-total'))

        img_url_list = []
        img_url_list.append(Crawler._get_img_url(doc))

        for page_num in range(2, total_page_num+1,1):
            n_url = url_format.format(page_num)
            n_doc = pq(url=n_url)
            n_img_url = Crawler._get_img_url(n_doc)
            img_url_list.append(n_img_url)
            time.sleep(interval)

        return img_url_list

        # download_img(img_url_list[0], './123/0001.jpg', True)


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
            title = version[version.find('[') + 1:version.find(']')].replace(' ', '-')

            book_info_doc = book_info_list_doc.eq(i)
            columns_doc = book_info_doc.children()
            columns = {}
            for j in range(0, columns_doc.length):
                column_doc = columns_doc.eq(j)
                column_idx = column_doc.attr('data-sort')
                column_url = column_doc.children().attr('href')
                column_title = column_doc.children().attr('title').replace(' ', '-')
                columns[column_idx] = {
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
        for p_id, p_title in pbar:
            pbar.set_description('获取产品详情: {0}(id={1})'.format(p_id, p_title))
            books = Crawler._get_book_info(p_id)
            row = self._row_dict.select(p_id)
            if 'books' in row:
                books.update(row['books'])
            self._row_dict.upsert(p_id, {'id': p_id, 'title': p_title, 'books': books})

            i += 1
            if i >= u:
                i = 0
                self._row_dict.commit()

        self._row_dict.commit()


    def get_book_download(self, reflesh=False):

        all_product = self._row_dict.select_all()

        all_columns = {}

        for pid in all_product:
            product = all_product[pid]
            p_title = product['title']
            books = product['books']

            for book_id in books:
                book = books[book_id]


                columns = book['columns']
                for column_id in columns:
                    column = columns[column_id]


                    column_title = column['title']

                    big_title = p_title + '-' + book_id + '-' + column_id + '-' + column_title

                    all_columns[big_title] = column

        pbar = tqdm(all_columns)
        for title in pbar:
            pbar.set_description('获取卷详情: {0}'.format(title))

            column = all_columns[title]

            if column.get('fetched', False) and (not reflesh):
                continue

            column_url = column['url']
            try:
                column_img = Crawler.get_book_details(column_url, 0.05)
                column['img'] = column_img
                column['fetched'] = True
                self._row_dict.commit()
            except:
                column['fetched'] = False
                self._row_dict.commit()

    def get_book_download_img(self, reflesh=False, interval=0.02):

        all_product = self._row_dict.select_all()

        all_columns = {}

        for pid in all_product:
            product = all_product[pid]
            p_title = product['title']
            books = product['books']

            for book_id in books:
                book = books[book_id]
                book_version = book['version']
                columns = book['columns']
                columns_ids = [int(i) for i in columns.keys()]
                column_fill_zero = build_fill_zero(max(columns_ids))

                for column_id in columns:
                    column = columns[column_id]

                    column_dir = str(os.path.abspath(os.path.join(self._base_dir, book_version, column_fill_zero(column_id))))

                    all_columns[column_dir] = column

        pbar = tqdm(all_columns)
        for column_dir in pbar:
            pbar.set_description('下载卷: {0}'.format(column_dir))

            column = all_columns[column_dir]

            if 'img' not in column:
                continue

            column_img = column['img']

            if column_img is None or len(column_img) == 0:
                continue

            if 'img_d' not in column:
                column['img_d'] = []
            column_img_d = column['img_d']

            column_dir = column_dir
            try:
                page_fill_zero = build_fill_zero(len(column_img))
                for i, img in enumerate(column_img):
                    if img in column_img_d:
                        continue

                    img_path = os.path.join(column_dir, page_fill_zero(str(i + 1)) + '.' + img.split('.')[-1])
                    download_img(img, img_path, True)
                    column_img_d.append(img)
                    self._row_dict.commit()
                    time.sleep(interval)
            except Exception as e:
                print(e)
                pass










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

    base_dir = os.path.join('.', '_rst', 'manhuadb', '伊藤润二')
    crawler = Crawler(base_dir)
    # crawler.get_book_info_by_keyword('伊藤润二')
    # crawler.get_book_download()
    crawler.get_book_download_img(interval=0.01)
    # Crawler._get_book_info('3481')

