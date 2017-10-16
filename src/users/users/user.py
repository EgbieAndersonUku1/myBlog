from flask import session

from src.users.util.id_generator import gen_id
from users.blogs.models import ParentBlog


class _UsersDetails(object):
    """ """
    def __init__(self, first_name, last_name, username, email, _id=None, blog_id=None, author_id=None):
        self._id = gen_id() if _id else _id
        self.blog_id = gen_id() if blog_id is None else blog_id
        self.author_id = gen_id() if author_id is None else author_id
        self.first_name = first_name
        self.last_name = last_name
        self.username  = username
        self.email = email

    @staticmethod
    def get_by_email(email):
        # search the records and return the first name of the user
        pass

    @staticmethod
    def get_by_author_by_id(author_id):
        pass

    def save(self):
        data = self._to_json()

        # add a record object that will save the data to database HERE

    def _to_json(self):
        """ """

        return {
            "_id": self._id,
            "blog_id": self.blog_id,
            "author_id": self.author_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }


class User(object):
    """The user class is the class allows the user to created a single blog
         or create multiple blogs, delete blogs, create, save and deletes
        all through the blog object.
     """

    def find_blog(self, child_blog_id):
        """Using the ID returns the child blog object that is associated with that ID"""

        user = self._retreive_user_info()
        parent_blog = ParentBlog(user.user_id, user.blog_id)
        return parent_blog.find_child_blog(child_blog_id)

    def get_all_blogs(self):
        """Return a list containing all the blogs created by the user"""

        user = self._retreive_user_info()
        parent_blog = ParentBlog(user.user_id, user.blog_id)
        return parent_blog.find_all_child_blogs()

    def get_author(self):
        """Returns the an author of the post as an object"""

        user = self._retreive_user_info()
        return _UsersDetails.get_by_author_by_id(user.author_id)

    def _retreive_user_info(self):
        """A helper function that returns the user object"""
        return _UsersDetails.get_by_email(session.get('email'))