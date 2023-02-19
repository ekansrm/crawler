from wordpress_xmlrpc import Client, WordPressPost

from wordpress_xmlrpc.methods import posts

wp = Client('http://ekans.tpddns.cn:10084/xmlrpc.php', 'admin', '2271989wl')

a = {
    'category': ['分类目录'],
    'post_tag': ['标签1', '标签2'],
}

def delete_article(post_id):
    wp.call(posts.DeletePost(post_id))


def edit_article(post_id, title, content, terms_names, featured_img=None):

    post = WordPressPost()

    post.title = title

    post.content = content

    post.post_status = 'private' # 文章状态，不写默认是草稿，private表示私密的，draft表示草稿，publish表示发布

    post.terms_names = terms_names

    if featured_img is not None:
        post.custom_fields = []
        post.custom_fields.append(
            {'key': 'fifu_image_url', 'value': featured_img}
        )



    wp.call(posts.EditPost(post_id, post))


def post_new_article(title, content, terms_names, featured_img=None):

    post = WordPressPost()

    post.title = title

    post.content = content

    post.post_status = 'publish' # 文章状态，不写默认是草稿，private表示私密的，draft表示草稿，publish表示发布

    post.terms_names = terms_names

    if featured_img is not None:
        post.custom_fields = []
        post.custom_fields.append(
            {'key': 'fifu_image_url', 'value': featured_img}
        )

    post.id = wp.call(posts.NewPost(post))


    return post.id

if __name__ == '__main__':
    # post = wp.call(posts.GetPost(876))

    post_id = post_new_article("1", '2', a, 'http://ekans.tpddns.cn:9900/sys/IMG_20140615_093741.jpg')