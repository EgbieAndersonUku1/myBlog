from users.util.id_generator import gen_id
from users.posts.models import Post


class ParentBlog(object):
    """ ParentBlog: class
    Each user on the application has a parent blog and from the parent blog
    many child blogs can be generated. This class SHOULD only be accessed
    from the user class and not directly.
    """

    def __init__(self, user_id, blog_id):
        self._blog_id = blog_id
        self._user_id = user_id

    def create_blog(self):
        return _ChildBlog(self._user_id, self._blog_id)

    def find_child_blog(self, child_blog_id):
        pass

    def find_all_child_blogs(self):
        """Returns all child blog created by this parent blog"""
        pass

    def delete_child_blog(self, child_blog_id):
        pass

    def delete_all_child_blogs(self):
        pass


class _ChildBlog(object):
    """The Child blog is a child of the Parent blog"""

    def __init__(self, user_id, parent_blog_id, _id=None):
        self._user_id = user_id
        self._parent_blog_id = parent_blog_id
        self._child_blog_id = gen_id() if _id is None else _id
        self._post = Post(self._user_id, self._parent_blog_id, self._child_blog_id)

    def get_post_by_id(self, post_id):
        """Takes an ID associated and returns the post object for that ID"""
        return self._post.get_post_by_id(post_id)

    def new_post(self, post_form, author_id):
        """new_post(object, str) -> returns None

        Creates a new post

        :param
                `post_form`: The post details which include the title, post content
                `author_id`: The ID associated with the author.
        """
        self._post.create_new_post(post_form, author_id)

    def update_post(self, post_form):
        """ """
        self._post.update_post(post_form)

    def delete_post(self, post_id):
        """Deletes a post from the blog"""
        self._post.delete_post(post_id)
