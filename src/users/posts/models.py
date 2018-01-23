from users.utils.generator.id_generator import gen_id
from users.utils.generator.date_generator import time_now
from users.records.record import Record
from users.utils.session.user_session import UserSession


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

    def get_post_by_id(self, post_id):
        """Test a post ID and returns that particular post."""

        data = Record.Query.Filter.filter_by_key_and_value("child_post_id", post_id)
        return _ChildPost(**data) if data else None

    def get_all_posts(self):
        """Returns all posts belonging to a particular blog"""

        query = {"parent_blog_id": self._blog_id,
                 "child_blog_id" : self.child_blog_id,
                 "parent_post_id": self.post_id, "post_live": True}

        posts = Record.Query.find_all(query)
        return [_ChildPost(**post) for post in posts] if posts else None

    def create_new_post(self, post_form):
        """create_new_post(form_post_obj) -> returns Post Object

        Takes a post form object containing the user post details
        and then creates a new post. Returns a post objects.
        """

        child_post_id = gen_id()
        child_post = self._to_json(post_form, child_post_id)
        publish_date = time_now()

        Record.save(child_post)

        return _ChildPost(self._blog_id, self.post_id,
                          self.child_blog_id,
                          self.post_id, child_post_id,
                          post_form.title, post_form.description,
                          publish_date
                        )

    def _to_json(self, post_form, child_post_id):
        """_to_json(post_obj, str) -> return a dictionary object

        Returns the data for post model object as json object

        :param
            `post_form`: A form object containing the user posts
                        .e.g title, description.
            `child_post_id`: The post id for the post.

        :returns
                Returns a json object
        """
        return {
            "parent_blog_id": self._blog_id,
            "child_blog_id": self.child_blog_id,
            "parent_post_id": self.post_id,
            "child_post_id": child_post_id,
            "title": post_form.title.data,
            "post": post_form.description.data,
            "post_live": True,
            "publish_date" : time_now(),
        }


class _ChildPost(object):

    def __init__(self, parent_blog_id, parent_post_id, child_blog_id,
                 child_post_id, title, post, publish_date, post_live, _id=None):

        self.child_post_id = child_post_id
        self.child_blog_id = child_blog_id
        self.title = title
        self.post = post
        self.post_live = post_live
        self.publish_date = publish_date
        self.author = UserSession.get_username()
        self._id = _id if _id else gen_id()
        self._parent_blog_id = parent_blog_id
        self._parent_post_id = parent_post_id

    def update_post(self, post_form, post_id):
        """"""
        post = self.get_post_by_id(post_id)

        # Add the functionality to update posts here
        pass

    def delete_post(self, post_id):
        """"""
        Record.Delete.delete_post(self.child_blog_id, self.child_post_id)