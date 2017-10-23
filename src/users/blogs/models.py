from users.util.id_generator import gen_id
from users.posts.models import Post
from users.drafts.model import Draft
from users.records.record import Record


class ParentBlog(object):
    """ ParentBlog: class
    Each user on the application has a parent blog and from the parent blog
    many child blogs can be generated. This class SHOULD only be accessed
    from the user class and not directly.
    """

    def __init__(self, user_id, blog_id):
        self._blog_id = blog_id
        self._user_id = user_id

    def create_blog(self, blog_form):
        """create_blog(blog form object) -> returns child blog object
        Creates a child blog that allows the user to create or delete a post

        :param
            `blog_form`: The post details which include the title, post content
        :returns
            Returns a blog object
        """
        child_blog_id = gen_id()
        blog_data = self._to_json(blog_form, child_blog_id)

        if not Record.save(blog_data):
           # will create a base exception here
           pass
        return _ChildBlog(self._user_id, self._blog_id, child_blog_id,
                          blog_form.name, blog_form.description)

    def find_child_blog(self, child_blog_id):
        pass

    def find_all_child_blogs(self):
        """Returns all child blog created by this parent blog"""
        pass

    def delete_child_blog(self, child_blog_id):
        pass

    def delete_all_child_blogs(self):
        pass

    def _to_json(self, blog_form, child_blog_id):
        """"""
        return {
            "user_id": self._user_id,
            "parent_blog_id": self._blog_id,
            "child_blog_id": child_blog_id,
            "blog_title": blog_form.title(),
            "blog_description": blog_form.description,
            "blog_live": True
        }


class _ChildBlog(object):
    """The Child blog is a child of the Parent blog"""

    def __init__(self, user_id, parent_blog_id, child_blog_id, blog_name, blog_descr):
        self._blog_name = blog_name
        self._blog_descr = blog_descr
        self._child_blog = child_blog_id
        self._user_id = user_id
        self._post = Post(user_id, parent_blog_id, child_blog_id)

    @property
    def blog_name(self):
        return self._blog_name

    @property
    def blog_description(self):
        return self._blog_descr

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

