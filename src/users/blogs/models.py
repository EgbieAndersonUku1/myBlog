from users.utils.generator.id_generator import gen_id
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
           raise Exception('Error, The blog data was not saved on the database.')
        return _ChildBlog(self._user_id, self._blog_id, child_blog_id,
                          blog_form.title, blog_form.description, _id=None,
                          blog_live=True)

    def find_child_blog(self, child_blog_id):
        """Takes a child blog id and if found returns that blog as an object"""

        data = Record.Query.Filter.filter_by_key_and_value("child_blog_id", child_blog_id)
        return _ChildBlog(**data) if data else None


    def find_all_child_blogs(self):
        """Returns all child blog created by this parent blog"""

        blogs = Record.Query.find_all(self._blog_id)
        return [_ChildBlog(**blog) for blog in blogs] if blogs else None

    def delete_child_blog(self, child_blog_id):
        return Record.Delete.delete_blog(child_blog_id)

    def delete_all_child_blogs(self):
        pass

    def update_child_blog(self, blog_id, data):
        """"""
        Record.Update.update(field_name='child_blog_id', field_id=blog_id, data=data)

    def _to_json(self, blog_form, child_blog_id):
        """"""
        return {
            "user_id": self._user_id,
            "parent_blog_id": self._blog_id,
            "child_blog_id": child_blog_id,
            "title": blog_form.title.data,
            "description": blog_form.description.data,
            "blog_live": True
        }


class _ChildBlog(object):
    """The Child blog is a child of the Parent blog"""

    def __init__(self, user_id, parent_blog_id, child_blog_id,
                  title, description, _id, blog_live):
        self._id = _id
        self.child_blog_id = child_blog_id
        self.title = title
        self.description = description
        self._user_id = user_id
        self._blog_live = blog_live
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