import requests
import os


def download_img(url, path, full_path=False, verify=False):
    response = requests.get(url, verify=verify)

    if not full_path:
        if not os.path.exists(path):
            os.makedirs(path)

        file_name = url.split('/')[-1]
        file_path = os.path.join(path, file_name)
    else:
        dir_path = os.path.dirname(path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        file_path = path

    with open(file_path, 'wb') as fp:
        fp.write(response.content)
