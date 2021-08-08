from flask import Flask, render_template
from jinja2 import Template
import os

app = Flask(__name__)
html_dir = os.path.join('.', 'app', 'bhc')
index_path = os.path.join(html_dir, 'index.html')
with open(index_path, 'r', encoding='utf-8') as fp:
    index_line = fp.readlines()
    index_htm = '\n'.join(index_line)
    index_tpl = Template(index_htm)


@app.route('/')
def index():
    text = """
    <h1>hello world</h1>
    """
    return index_tpl.render(text=text)


if __name__ == '__main__':
    app.run()
