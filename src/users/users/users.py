from flask import session

from users.utils.generator.id_generator import gen_id
from users.utils.email.sender import email_user_verification_code, email_user_forgotten_password_verification_code
from users.blogs.models import ParentBlog
from users.records.record import Record
from users.utils.generator.id_generator import gen_id as gen_code
from users.utils.implementer.password_implementer import PasswordImplementer
from users.users.helper import save_to_db, update_db, to_class


class User(object):
    """ """
    def __init__(self, username, email, password, configuration_codes={}, account_confirmed=False,
                 _id=None, parent_blog_id=None, post_id=None):

        self._id = gen_id() if _id is None else _id
        self.parent_blog_id = gen_id() if parent_blog_id is None else parent_blog_id
        self.post_id = gen_id() if post_id is None else post_id
        self.username = username.lower()
        self.email = email.lower()
        self.password = password
        self.account_confirmed = account_confirmed
        self.configuration_codes = configuration_codes

    @classmethod
    def extract_web_form(cls, form):
        """"""
        return cls(form.username.data, form.email.data,
                   PasswordImplementer.hash_password(form.password.data)
                   )

    @classmethod
    def get_by_username(cls, username):
        """"""
        return to_class(cls, Record.Query.Filter.filter_user_by_username(username))

    @classmethod
    def get_by_email(cls, email):
        """Searches the records by email address"""
        return to_class(cls, Record.Query.Filter.filter_user_by_email(email))

    def register(self):
        """"""
        self._gen_user_verification_code()
        self._email_user_verification_code()
        self.save()

    def _gen_user_verification_code(self):
        self.configuration_codes['verification_code'] = self._gen_code()

    def _gen_email_change_verification_code(self):
        self.configuration_codes['email_code'] = self._gen_code()

    def save(self):
        """"""
        return save_to_db(self._to_json())

    def _to_json(self):
        """ """

        return {
            "_id": self._id,
            "parent_blog_id": self.parent_blog_id,
            "post_id": self.post_id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "configuration_codes": self.configuration_codes,
            "account_confirmed": self.account_confirmed
        }

    @classmethod
    def confirm_registration(cls, username, registration_code):
        """"""

        user = cls.get_by_username(username)

        if user and user.configuration_codes.get('verification_code') == registration_code:
            user.configuration_codes.pop('verification_code')
            user.account_confirmed = True
            user.update()
            return True
        return False


    def reset_forgotten_password(self):
        """"""

        self._gen_forgotten_password_code()
        self.update()
        self._email_user_verification_code(code_type='forgotten_password_code')

    def _gen_forgotten_password_code(self):
        """"""
        self.configuration_codes['forgotten_password_code'] = self._gen_code()

    def update(self):
        """"""
        update_db('_id', self._id, self._to_json())


    def _gen_code(self):
        """"""
        return gen_code()

    def _email_user_verification_code(self, code_type='verification_code'):
        """ """
        emailer = self._get_email_sender(code_type)
        emailer(self.email, self.username, self.configuration_codes.get(code_type))

    def _get_email_sender(self, type_of_email):
        """"""
        assert type_of_email in ['verification_code', "forgotten_password_code"]

        return {
            "verification_code":  email_user_verification_code,
            "forgotten_password_code":  email_user_forgotten_password_verification_code,
        }.get(type_of_email)

    def __repr__(self):
        return "Username: <'{}'>".format(self.username)


class UserBlog(object):
    """The user class is the class allows the user to created a single blog
         or create multiple blogs, delete blogs, create, save and deletes
        all through the blog object.
     """
    def __init__(self):
        user = self._retreive_user_info()
        self._parent_blog = ParentBlog(user._id, user.parent_blog_id, user.post_id)

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

    def update_blog(self, blog_id, data):
        """"""
        self._parent_blog.update_child_blog(blog_id, data)

    def delete_blog(self, blog_id):
        self._parent_blog.delete_child_blog(blog_id)

    def _retreive_user_info(self):
        """A helper function that returns the user object"""

        return User.get_by_email(session.get('email'))

