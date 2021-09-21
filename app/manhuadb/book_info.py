import os
import time
import traceback
import zipfile
from tqdm import tqdm
from pyquery import PyQuery as pq
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
    def book_url(bid):
        return Crawler.base_url() + '/manhua/' + bid

    @staticmethod
    def search_book_brief(keyword):
        url = Crawler.base_url() + '/search?q=' + keyword
        doc = pq(url)
        book_list_doc = doc("""a[class="d-block"]""")
        book_list = [(e.attr('href').split('/')[-1], e.attr('title'),) for e in book_list_doc.items()]
        return book_list

    @staticmethod
    def crawl_book_columns(bid):
        url = Crawler.book_url(bid)
        doc = pq(url)

        book_info_title_doc = doc("""h3[class~="comic_version_title"]""")
        book_info_list_doc = doc("""ol[class~="links-of-books"]""")

        # 可能有番外篇、单行本什么的
        book_info = {}
        for i in range(0, book_info_list_doc.length):
            version = book_info_title_doc.eq(i).text().replace(' ', '-')
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

    @staticmethod
    def crawl_book_column_pages(book_url, interval=0.1):

        def get_img_url(page_doc):
            img_url = page_doc("""img[class="img-fluid show-pic"]""").attr('src')
            return img_url

        url = Crawler.base_url() + book_url
        url_format = url.replace('.html', '') + '_p{0}.html'
        doc = pq(url=url)

        page_select_doc = doc('div[data-page]')
        total_page_num = int(page_select_doc.attr('data-total'))

        img_url_list = [get_img_url(doc)]

        for page_num in range(2, total_page_num + 1, 1):
            n_url = url_format.format(page_num)
            n_doc = pq(url=n_url)
            n_img_url = get_img_url(n_doc)
            img_url_list.append(n_img_url)
            time.sleep(interval)

        return img_url_list

    def __init__(self, base_dir):
        self._base_dir = base_dir
        self._row_dict = FsRowDict(os.path.join(base_dir, 'all.json'))

    def search_book(self, keyword):
        """查找漫画"""

        book_list = Crawler.search_book_brief(keyword)
        book_process_bar = tqdm(book_list)

        i = 0
        u = 1
        for book_id, book_title in book_process_bar:
            book_process_bar.set_description('获取书籍详情: {0}(id={1})'.format(book_title, book_id))
            book_detail = Crawler.crawl_book_columns(book_id)

            # 将书籍信息合并到字典里
            cached_book_info = self._row_dict.select(book_id)
            if 'books' in cached_book_info:
                book_detail.update(cached_book_info['books'])
            self._row_dict.upsert(book_id, {'id': book_id, 'title': book_title, 'books': book_detail})

            i += 1
            if i >= u:
                i = 0
                self._row_dict.commit()

        self._row_dict.commit()

    def crawl_book(self, refresh=False, interval=0.02):
        """爬取漫画"""

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

        column_process_bar = tqdm(all_columns)
        for title in column_process_bar:
            column_process_bar.set_description('获取卷详情: {0}'.format(title))

            column = all_columns[title]

            if column.get('fetched', False) and (not refresh):
                continue

            column_url = column['url']
            try:
                column_img = Crawler.crawl_book_column_pages(column_url, interval=interval)
                column['img'] = column_img
                column['fetched'] = True
                self._row_dict.commit()
            except Exception as e:
                traceback.print_exc(e)
                column['fetched'] = False
                self._row_dict.commit()

    def download_book(self, refresh=False, interval=0.02):
        """下载漫画"""

        all_product = self._row_dict.select_all()

        all_columns = {}

        for pid in all_product:
            product = all_product[pid]
            books = product['books']

            for book_id in books:
                book = books[book_id]
                book_version = book['version']
                columns = book['columns']
                columns_ids = [int(i) for i in columns.keys()]
                column_fill_zero = build_fill_zero(max(columns_ids))

                for column_id in columns:
                    column = columns[column_id]

                    column_dir = str(
                        os.path.abspath(os.path.join(self._base_dir, book_version, column_fill_zero(column_id))))

                    all_columns[column_dir] = column

        column_process_bar = tqdm(all_columns)
        for column_dir in column_process_bar:
            column_process_bar.set_description('下载卷: {0}'.format(column_dir))

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
                    if img in column_img_d and (not refresh):
                        continue
                    img_path = os.path.join(column_dir, page_fill_zero(str(i + 1)) + '.' + img.split('.')[-1])
                    download_img(img, img_path, True)
                    column_img_d.append(img)
                    self._row_dict.commit()

                    time.sleep(interval)

            except Exception as e:
                traceback.print_exc(e)

    def zip_book(self):
        """压缩漫画为 ZIP 格式"""

        all_product = self._row_dict.select_all()

        all_books = []
        all_columns = []
        for pid in all_product:
            product = all_product[pid]
            books = product['books']

            for book_id in books:
                book = books[book_id]
                book_version = book['version']
                columns = book['columns']
                columns_ids = [int(i) for i in columns.keys()]
                column_fill_zero = build_fill_zero(max(columns_ids))

                for column_id in columns:
                    column = columns[column_id]

                    column_dir = str(
                        os.path.abspath(os.path.join(self._base_dir, book_version, column_fill_zero(column_id))))

                    column_zip = str(
                        os.path.join(self._base_dir, '_zip', book_version, column_fill_zero(column_id) + '.zip.cbz')
                    )

                    all_columns.append((column_dir, column_zip))

        column_process_bar = tqdm(all_columns)
        for column_dir, column_zip in column_process_bar:
            column_process_bar.set_description('压缩文件: {0}'.format(column_zip))

            os.makedirs(os.path.dirname(column_zip), exist_ok=True)
            with zipfile.ZipFile(column_zip, 'w', zipfile.ZIP_STORED) as zf:
                for i in os.walk(column_dir):
                    for j in i[2]:
                        file_path = os.path.join(i[0], j)
                        zip_path = str(file_path).replace(column_dir, '')
                        zf.write(file_path, zip_path)


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

    crawler = Crawler(os.path.join('.', '_rst', 'manhuadb', '妄想学生会'))
    # crawler = Crawler(os.path.join('.', '_rst', 'manhuadb', '伊藤润二'))
    # crawler.search_book('妄想学生会')
    # crawler.crawl_book(interval=0.01)
    crawler.download_book(interval=0.01)
    # crawler.zip_book()
