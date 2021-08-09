import os
from flask import Flask, render_template
from jinja2 import Template
from utils.fs import FsRowDict

page_dir = os.path.join('.', 'app', 'bhc', 'page')
view_path = os.path.join(page_dir, 'view.html')
with open(view_path, 'r', encoding='utf-8') as fp:
    view_htm = '\n'.join(fp.readlines())
    view_tpl = Template(view_htm)


class Browser(object):
    _base_dir = ''
    _row_dict = None

    def __init__(self, base_dir):
        self._base_dir = base_dir
        self._row_dict = FsRowDict(os.path.join(base_dir, 'all.json'))

    def _list_img(self, tid):
        img_dir = os.path.join(self._base_dir, tid)
        if os.path.exists(img_dir):
            img_list = ['/' + tid + '/' + e for e in os.listdir(img_dir)]
        else:
            img_list = []
        return img_list

    def render_qm_info_by_tid(self, tid_list):
        rv = []
        for tid in tid_list:
            row = self._row_dict.select(tid)
            _row = dict(row)
            _row['img_local'] = self._list_img(tid)
            _row['txt_line'] = _row['txt'].split('\n')
            rv.append(_row)
        return rv

    def select_all_tid(self):
        return self._row_dict.select_all().keys()



base_dir = os.path.join('.', '_rst', 'bhc')
browser = Browser(base_dir)

app = Flask(__name__, static_url_path='', static_folder='../../_rst/bhc')

@app.route('/')
def index():
    return view_tpl.render(rows=browser.render_qm_info_by_tid(browser.select_all_tid()))


if __name__ == '__main__':
    app.run()
