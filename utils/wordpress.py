from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc import xmlrpc_client
import base64
from wordpress_xmlrpc.methods import posts, media

wp = Client('http://ekans.tpddns.cn:10084/xmlrpc.php', 'admin', '2271989wl')

a = {
    'category': ['分类目录'],
    'post_tag': ['标签1', '标签2'],
}

def delete_article(post_id):
    wp.call(posts.DeletePost(post_id))


def edit_article(post_id, title, content, terms_names, thumbnail_id):

    post = WordPressPost()

    post.title = title

    post.content = content

    post.post_status = 'publish' # 文章状态，不写默认是草稿，private表示私密的，draft表示草稿，publish表示发布

    post.terms_names = terms_names

    post.thumbnail = thumbnail_id

    wp.call(posts.EditPost(post_id, post))


def post_new_article(title, content, terms_names, thumbnail_id):

    post = WordPressPost()

    post.title = title

    post.content = content

    post.post_status = 'publish' # 文章状态，不写默认是草稿，private表示私密的，draft表示草稿，publish表示发布

    post.thumbnail = thumbnail_id

    post.terms_names = terms_names

    post.id = wp.call(posts.NewPost(post))


    return post.id

def upload_feature_img(img_path):
    data = {
        'name': 'gggpicture.jpg',
        'type': 'image/jpeg',
    }
    with open(img_path, 'rb') as img:
        data['bits'] = xmlrpc_client.Binary(img.read())
    response = wp.call(media.UploadFile(data))
    return response




if __name__ == '__main__':
    # post = wp.call(posts.GetPost(876))

    # post_id = post_new_article("1", '2', a, 'http://ekans.tpddns.cn:9900/sys/IMG_20140615_093741.jpg')
    r = upload_feature_img("D:\\Work\\Project.Crawler\\_rst\\hdq\\237\\233001cedus7u8e1d19l1z.jpg")
    print(r)