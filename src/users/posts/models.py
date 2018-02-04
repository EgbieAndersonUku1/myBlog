from users.utils.generator.id_generator import gen_id
from users.utils.generator.date_generator import time_now as date_created
from users.records.record import Record
from users.utils.security.user_session import UserSession
from users.drafts.model import Draft
from users.utils.html_stripper import strip_html_tags


class Post(object):
    """The post allows the blog to create, save and delete a post. The
        class should not be accessed directly and should only be accessed
        from the User blog class
     """
    def __init__(self, user_id, parent_blog_id, child_blog_id, post_id):
        self._user_id = user_id
        self._blog_id = parent_blog_id
        self.child_blog_id = child_blog_id
        self.post_id = post_id
        self.Draft = Draft(self.child_blog_id, self.post_id)

    @staticmethod
    def get_post_by_id(post_id):
        """Test a post ID and returns that particular post."""

        post_data = Record.Query.Filter.filter_by_key_and_value({"child_post_id":post_id})
        return _ChildPost(**post_data) if post_data else None

    def get_all_posts(self):
        """Returns all posts belonging to a particular blog"""

        query = {"parent_blog_id": self._blog_id,
                 "child_blog_id" : self.child_blog_id,
                 "user_id": self._user_id,
                 "parent_post_id": self.post_id, "post_live": True}

        posts = Record.Query.find_all(query)
        return [_ChildPost(**post) for post in posts] if posts else None

    def create_new_post(self, title, post):
        """create_new_post(str, str) -> returns Post Object

        Takes a post form object containing the user post details
        and then creates a new post. Returns a post objects.
        """

        child_post_id = gen_id()
        publish_date = date_created()
        child_post = self._to_json(title, post, child_post_id, publish_date)

        Record.save(child_post)

        return _ChildPost(self._blog_id, self.post_id,
                          self.child_blog_id, self._user_id,
                          self.post_id, child_post_id,
                          title, post,
                          publish_date
                         )

    @classmethod
    def delete_post(cls, post_id):
        """"""
        child_post = cls.get_post_by_id(post_id)
        Record.Delete.delete_post(child_post.child_blog_id, child_post.child_post_id)

    def _to_json(self, title, post, child_post_id, publish_date):
        """_to_json(post_obj, str) -> return a dictionary object

        Returns the data for post model object as json object

        :param
            `title`: Post title
            `description`: The post description.
            `child_post_id`: The post id for the post.
            `publish_date`: The date the post was created

        :returns
                Returns a json object
        """
        return {
            "user_id": self._user_id,
            "parent_blog_id": self._blog_id,
            "child_blog_id": self.child_blog_id,
            "parent_post_id": self.post_id,
            "child_post_id": child_post_id,
            "title": title,
            "post": post,
            "post_live": True,
            "publish_date": publish_date,
        }


class _ChildPost(object):
    """This _ChildPost is a container and should not be accessed directly"""

    def __init__(self, parent_blog_id, parent_post_id, child_blog_id,
                 child_post_id, user_id, title, post, publish_date,
                 post_live, _id=None, image=None):

        self.child_post_id = child_post_id
        self.child_blog_id = child_blog_id
        self.user_id = user_id
        self.title = title
        self.post = post
        self.image = image
        self.post_live = post_live
        self.publish_date = publish_date
        self.author = UserSession.get_username()
        self._id = _id if _id else gen_id()
        self._parent_blog_id = parent_blog_id
        self._parent_post_id = parent_post_id

    @staticmethod
    def html_strip(text):
        return strip_html_tags(text)

    def update_post(self, data):
        """"""
        Record.Update.update(field_name='child_post_id', field_id=self.child_post_id, data=data)
