from users.utils.generator.id_generator import gen_id
from users.utils.email.sender import email_user_verification_code, email_user_forgotten_password_verification_code
from users.blogs.models import ParentBlog
from users.records.record import Record
from users.utils.generator.id_generator import gen_id as gen_code
from users.utils.security.password_implementer import PasswordImplementer
from users.utils.security.user_session import UserSession


class _UserSearch(object):

    @classmethod
    def get_by_username(cls, username):
        """"""
        return Record.Query.Filter.filter_user_by_username(username)

    @classmethod
    def get_by_email(cls, email):
        """Searches the records by email address"""
        return Record.Query.Filter.filter_user_by_email(email)


class _UserAccount(object):
    """"""
    def __init__(self, username, email, password, account_confirmed=False,
                 configuration_codes={}, _id=None, user_id=None):

        self.email = email.lower()
        self.username = username.lower()
        self.password = password
        self.account_confirmed = account_confirmed
        self.configuration_codes = configuration_codes
        self.user_id = user_id if user_id else gen_id()
        self._id = _id

    def login(self, password):
        return PasswordImplementer.check_password(password, self.password)

    def is_user_email_confirmed(self):
        """Checks whether the user has confirmed their email account and returns the appropriate action.

        Returns the appropriate status based on the user's account status:

        If the user has registered but not confirmed their email address returns a 'NOT_CONFIRMED' message.
        If the user has registered and confirmed their email address Returns 'ACCOUNT_CONFIRMED'.
        if the user is not registered or is using an incorrect username/password returns 'ACCOUNT_NOT_FOUND'.
        """

        if not self.account_confirmed:
            confirmation = 'NOT_CONFIRMED'
        elif self.account_confirmed:
            confirmation = 'EMAIL_CONFIRMED'
        else:
            confirmation = 'ACCOUNT_NOT_FOUND'
        return confirmation

    @classmethod
    def get_account_by_username(cls, username):
        return cls._to_class(_UserSearch.get_by_username(username))

    @classmethod
    def get_account_by_email(cls, email):
        return cls._to_class(_UserSearch.get_by_email(email))

    def register(self):
        """"""
        self._gen_user_verification_code()
        self._email_user_verification_code()
        self._save()

    def _gen_user_verification_code(self):
        self.configuration_codes['verification_code'] = self._gen_code()

    def _gen_email_change_verification_code(self):
        self.configuration_codes['email_code'] = self._gen_code()

    def _save(self):
        """"""
        return Record.save(self._to_json())

    @classmethod
    def verify_registration_code(cls, username, registration_code):
        """"""

        user = cls.get_account_by_username(username)

        if user and user.configuration_codes.get('verification_code') == registration_code:
            user.configuration_codes.pop('verification_code')
            user.account_confirmed = True
            user.update_account()
            return True
        return False

    def update_forgotten_password(self, new_password):
        """"""
        self.configuration_codes.pop('forgotten_password_code')
        self.password = PasswordImplementer.hash_password(new_password)
        self.update_account()

    @classmethod
    def verify_forgotten_password_code(cls, username, code):
        """"""
        user = cls.get_account_by_username(username)
        return user if user and user.configuration_codes['forgotten_password_code'] == code else None

    def reset_forgotten_password(self):
        """"""
        self._gen_forgotten_password_code()
        self.update_account()
        self._email_user_verification_code(code_type='forgotten_password_code')

    def _gen_forgotten_password_code(self):
        """"""
        self.configuration_codes['forgotten_password_code'] = self._gen_code()

    def update_account(self):
        """"""
        Record.Update.update('_id', self._id, self._to_json())

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
            "verification_code": email_user_verification_code,
            "forgotten_password_code": email_user_forgotten_password_verification_code,
        }.get(type_of_email)

    def _to_json(self):
        """ """

        return {
            "_id": self._id,
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "configuration_codes": self.configuration_codes,
            "account_confirmed": self.account_confirmed
        }

    @classmethod
    def _to_class(cls, query):
        return cls(**query) if query else None


class User(_UserAccount):
    """ """
    def __init__(self, username, email, password, account_confirmed=False,
                 configuration_codes={}, _id=None, user_id=None):

        super().__init__(username, email, password, account_confirmed,
                         configuration_codes, _id, user_id)

    @classmethod
    def extract_web_form(cls, form):
        """"""
        return cls(form.username.data, form.email.data,
                   PasswordImplementer.hash_password(form.password.data)
                   )



class UserBlog(object):
    """The user blog class allows the user to created either a single blog,
       multiple blogs, delete blogs.
     """
    def __init__(self):
        user = UserBlog._retreive_user_info()
        self._parent_blog = ParentBlog(user.user_id)

    def create_blog(self, blog_form):
        """create_blog(obj) -> return blog object
        Takes a blog form and creates a child blog object.

        :param
            `blog_form`: Contains the details that will be used to create
                        the blog i.e title, description
        :returns
            A child blog containing the new details.
        """
        return self._parent_blog.create_blog(blog_form)

    def get_blog(self, child_blog_id):
        """Using the blog ID returns the child blog object associated with that ID"""
        return self._parent_blog.find_child_blog(child_blog_id)

    def get_all_blogs(self):
        """Return a list of objects that contains all the blogs created by the user"""
        return self._parent_blog.find_all_child_blogs()

    def update_blog(self, blog_id, data):
        """Takes data and a blog id and updates that blog using the data"""
        self._parent_blog.update_child_blog(blog_id, data)

    def delete_blog(self, blog_id):
        """Deletes a blog by ID"""
        child_blog = self._parent_blog.find_child_blog(child_blog_id=blog_id)
        child_blog.delete_blog()

    def delete_all_blogs(self):
        """Deletes all blogs created by the user"""
        self._parent_blog.delete_all_child_blogs()

    @staticmethod
    def _retreive_user_info():
        """A helper function that returns the user object"""
        return User.get_account_by_email(UserSession.get_value_by_key("email"))

