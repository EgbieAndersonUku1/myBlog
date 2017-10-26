from flask import session

from users.utils.generator.id_generator import gen_id
from users.utils.email.sender import email_user_verification_code
from users.blogs.models import ParentBlog
from users.records.record import Record
from users.utils.generator.id_generator import gen_id as gen_code


class User(object):
    """ """
    def __init__(self, first_name, last_name, username, email, author_name,
                 password, configuration_codes={}, _id=None,
                 blog_id=None, author_id=None,parent_blog_created=False):

        self._id = gen_id() if _id else _id
        self.blog_id = gen_id() if blog_id is None else blog_id
        self.author_id = gen_id() if author_id is None else author_id
        self.first_name = first_name
        self.last_name = last_name
        self.username  = username
        self.email = email
        self.author_name = author_name
        self.password = password
        self.configuration_codes = configuration_codes
        self.parent_blog_created = parent_blog_created

    def _gen_user_verification_code(self):
        self.configuration_codes['verification_code'] = self._gen_code()

    def _gen_email_change_verification_code(self):
        self.configuration_codes['email_code'] = self._gen_code()

    def _gen_code(self):
        """"""
        return gen_code()

    def email_user_account_verification_code(self):
        """ """
        return email_user_verification_code(self.username, self.configuration_codes['verification_code'])

    @staticmethod
    def get_by_email(email):
        # search the records and return the first name of the user
        pass

    @staticmethod
    def get_by_author_by_id(author_id):
        pass

    def save(self):

        return Record.save(self._to_json())

        # add a record object that will save the data to database HERE

    def _to_json(self):
        """ """

        return {
            "_id": self._id,
            "parent_blog_id": self.blog_id,
            "author_id": self.author_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password,
            "email": self.email,
            "author_name": self.author_name,
            "parent_blog_created": self.parent_blog_created
        }


class UserBlog(object):
    """The user class is the class allows the user to created a single blog
         or create multiple blogs, delete blogs, create, save and deletes
        all through the blog object.
     """
    def __init__(self):
        self._user = self._retreive_user_info()
        self._parent_blog = ParentBlog(self._user.user_id, self._user.blog_id)

    def create_blog(self, blog_form):
        """create_blog(obj) -> return blog object
        Takes a blog form and creates a child blog object.

        :param
                `blog_form`: Contains the details that will be used to create the blog i.e title, description
        :returns
                A child blog containing the new details.
        """
        return self._parent_blog.create_blog(blog_form)

    def get_blog(self, child_blog_id):
        """Using the ID returns the child blog object that is associated with that ID"""
        return self._parent_blog.find_child_blog(child_blog_id)

    def get_all_blogs(self):
        """Return a list containing all the blogs created by the user"""
        return self._parent_blog.find_all_child_blogs()

    def get_blog_author(self):
        """Returns the an author of the post as an object"""
        return User.get_by_author_by_id(self._user.author_id)

    def _retreive_user_info(self):
        """A helper function that returns the user object"""
        return User.get_by_email(session.get('email'))