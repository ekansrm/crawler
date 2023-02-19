import json
import requests
import minio

endpoint = 'ekans.tpddns.cn:9900'

MINIO_CONF = {
    'endpoint': endpoint,
    'access_key': 'admin',
    'secret_key': 'rm19223ewkl#s',
    'secure': False
}

client = minio.Minio(**MINIO_CONF)


def upload_img_to_minio(bucket:str, file_name:str, file_path:str):
    client.fput_object(bucket_name=bucket, object_name=file_name,
                       file_path=file_path,
                       content_type='image/jpeg'
                       )

    return 'http://' + endpoint + '/' + bucket + '/' + file_name


if __name__ == '__main__':
    upload_img_to_minio("sys", "/1231/123132.jpg", '''D:\\Work\\Project.Crawler\\_rst\\hdq\\1816\\235604cbns4ejnsejzg4je.jpg''')
