import requests
import os


def download_img(url, dir_path):
    response = requests.get(url)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    file_name = url.split('/')[-1]
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'wb') as fp:
        fp.write(response.content)
