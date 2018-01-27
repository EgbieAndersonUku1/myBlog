from users.utils.generator.id_generator import gen_id
from users.posts.models import Post
from users.drafts.model import Draft
from users.records.record import Record
from users.utils.generator.date_generator import time_now as date_created
from users.utils.html_stripper import strip_html_tags


class ParentBlog(object):
    """ ParentBlog: class
    Each user on the application has a parent blog and from the parent blog
    many child blogs can be generated. This class SHOULD only be accessed
    from the user class and not directly.
    """

    def __init__(self, user_id, blog_id, post_id):
        self._blog_id = blog_id
        self._user_id = user_id
        self._post_id = post_id

    def create_blog(self, blog_form):
        """create_blog(blog form object) -> returns child blog object
        Creates a child blog that allows the user to create or delete a post

        :param
            `blog_form`: The post details which include the title, post content
        :returns
            Returns a blog object
        """
        child_blog_id = gen_id()
        blog_data = self._to_json(blog_form, child_blog_id, date_created)

        if not Record.save(blog_data):
           raise Exception('Error, The blog data was not saved on the database.')

        return _ChildBlog(self._user_id, self._blog_id, child_blog_id, self._post_id,
                          blog_form.blog_name, blog_form.title, blog_form.description, _id=None,
                          blog_live=True, date_created=date_created)

    def find_child_blog(self, child_blog_id):
        """Takes a child blog id and if found returns that blog as an object"""

        data = Record.Query.Filter.filter_by_key_and_value({"child_blog_id":child_blog_id})
        return _ChildBlog(**data) if data else None

    def find_all_child_blogs(self):
        """Returns all child blog created by this parent blog"""

        blogs = Record.Query.find_all(query={"parent_blog_id": self._blog_id, "blog_live": True})
        return [_ChildBlog(**blog) for blog in blogs] if blogs else None

    @staticmethod
    def delete_child_blog(child_blog_id):
        """"""
        Record.Delete.delete_blog(child_blog_id)

    def delete_all_child_blogs(self):
        Record.Delete.delete_all_blogs(data={"parent_blog_id": self._blog_id, "blog_live": True})

    def update_child_blog(self, blog_id, data):
        """"""
        Record.Update.update(field_name='child_blog_id', field_id=blog_id, data=data)

    def _to_json(self, blog_form, child_blog_id, date_created):
        """"""
        return {
            "user_id": self._user_id,
            "parent_blog_id": self._blog_id,
            "post_id": self._post_id,
            "child_blog_id": child_blog_id,
            "blog_name": blog_form.blog_name.data,
            "title": blog_form.title.data,
            "description": blog_form.description.data,
            "blog_live": True,
            "date_created": date_created()
        }


class _ChildBlog(object):
    """The Child blog is a child of the Parent blog and should not be called directly.
       It is a container
    """
    def __init__(self, user_id, parent_blog_id, child_blog_id, post_id,
                  blog_name, title, description, _id, blog_live, date_created):

        self.child_blog_id = child_blog_id
        self.post_id = post_id
        self.blog_name = blog_name
        self.title = title
        self.description = description
        self.date_created = date_created
        self._id = _id
        self._user_id = user_id
        self._blog_live = blog_live
        self.Post = Post(user_id, parent_blog_id, child_blog_id, post_id)

    def html_strip(self, text):
        return strip_html_tags(text)