from flask import session

from users.utils.generator.id_generator import gen_id
from users.utils.email.sender import email_user_verification_code, email_user_forgotten_password_verification_code
from users.blogs.models import ParentBlog
from users.records.record import Record
from users.utils.generator.id_generator import gen_id as gen_code
from users.utils.implementer.password_implementer import PasswordImplementer
from users.utils.session.user_session import UserSession
from users.users.profile_images import ProfileImages
from app import cache


def _to_class(class_obj, query):
    return class_obj(**query) if query else None


def _save_to_db(data):
    return Record.save(data)


def _update_db(field_id_to_find, field_id_value, data):
    Record.Update.update(field_id_to_find, field_id_value, data)


class User(object):
    """ """
    def __init__(self, username, email, password, configuration_codes={}, account_confirmed=False,
                 _id=None, parent_blog_id=None, author_id=None, parent_blog_created=False, profile_id=None):

        self._id = gen_id() if _id is None else _id
        self.profile_id = gen_id() if _id is None else profile_id
        self.parent_blog_id = gen_id() if parent_blog_id is None else parent_blog_id
        self.author_id = gen_id() if author_id is None else author_id
        self.username = username
        self.email = email
        self.password = password
        self.parent_blog_created = parent_blog_created
        self.account_confirmed = account_confirmed
        self.configuration_codes = configuration_codes

    def gen_user_verification_code(self):
        self.configuration_codes['verification_code'] = self._gen_code()

    def gen_email_change_verification_code(self):
        self.configuration_codes['email_code'] = self._gen_code()

    def gen_forgotten_password_code(self):
        """"""
        self.configuration_codes['forgotten_password_code'] = self._gen_code()

    def _gen_code(self):
        """"""
        return gen_code()

    def email_user_verification_code(self, code_type='verification_code'):
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


    @classmethod
    def extract_web_form(cls, form):
        """"""
        return cls(form.username.data, form.email.data,
                   PasswordImplementer.hash_password(form.password.data)
                   )

    @classmethod
    def get_by_username(cls, username):
        """"""
        return _to_class(cls, Record.Query.Filter.filter_user_by_username(username))

    @classmethod
    def get_by_email(cls, email):
        """Searches the records by email address"""
        return _to_class(cls, Record.Query.Filter.filter_user_by_email(email))

    def save(self):
        """"""
        return _save_to_db(self._to_json())

    def update(self):
        """"""
        _update_db('_id', self._id, self._to_json())

    def _to_json(self):
        """ """

        return {
            "_id": self._id,
            "parent_blog_id": self.parent_blog_id,
            "profile_id": self.profile_id,
            "author_id": self.author_id,
            "username": self.username.lower(),
            "password": self.password,
            "email": self.email.lower(),
            "parent_blog_created": self.parent_blog_created,
            "configuration_codes": self.configuration_codes,
            "account_confirmed": self.account_confirmed
        }

    def __repr__(self):
        return "Username: <'{}'>".format(self.username)


class UserProfile(object):
    """"""

    def __init__(self, first_name, last_name, author_name, username, email, bio, profile_img):
        self.profile_id = self.get_profile_id()
        self.first_name = first_name
        self.last_name = last_name
        self.author_name = author_name
        self.username = username
        self.email = email
        self.bio = bio
        self.profile_img = ProfileImages(self.profile_id, profile_img)

    @cache.memoize(600)
    def get_profile(self):
        return _to_class(UserProfile, Record.Query.Filter.filter_by_id(self.profile_id))

    def save(self):
        """"""
        return _save_to_db(self._to_json())

    def update(self):
        """"""
        _update_db('profile_id', self.profile_id, self._to_json())

    def _to_json(self):
        """"""
        return {
            "profile_id": self.profile_id,
            "first_name": self.first_name,
            "last_name" : self.last_name,
            "author_name":self.author_name,
            "username": self.username,
            "email": self.email,
            "bio": self.bio,
            "profile_img":self.profile_img
        }

    @cache.memoize(600)
    def get_profile_id(self):
        """"""
        user = User.get_by_username(UserSession.get_username())
        self.profile_id = user.profile_id

    @classmethod
    def extract_web_form(cls, form):
        """"""
        return cls(form.first_name.data,
                   form.last_name.data,
                   form.author_name.data,
                   form.username.data,
                   form.email.data,
                   form.bio.data,
                   form.profile_img.data
                    )


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