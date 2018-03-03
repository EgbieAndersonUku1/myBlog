from users.utils.generator.id_generator import gen_id
from users.utils.email.sender import email_user_verification_code, email_user_forgotten_password_verification_code
from users.blogs.models import ParentBlog
from users.records.record import Record
from users.utils.generator.id_generator import gen_id as gen_code
from users.utils.security.password_implementer import PasswordImplementer
from users.utils.security.user_session import UserSession


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
        self._id = _id if _id else gen_id()

    @classmethod
    def get_account_by_username(cls, username):
        """Returns an account using the username if found else None"""
        return cls._to_class(query=Record.Query.Filter.filter_user_by_username(username))

    @classmethod
    def get_account_by_email(cls, email):
        """Returns an account using an email address if found else None"""
        return cls._to_class(query=Record.Query.Filter.filter_user_by_email(email))

    @classmethod
    def get_account_by_user_id(cls, user_id):
        return cls._to_class(query=Record.Query.Filter.filter_user_by_id(user_id))

    def verify_registration_code(self, registration_code):
        """Verify whether registration code sent is legit"""
        return self.configuration_codes.get('verification_code') == registration_code

    def register(self):
        """Register the user to the application"""

        self.configuration_codes.pop('verification_code')
        self.account_confirmed = True
        self.update_account()

    def is_login_valid(self, password):
        """Check whether the user login password is correct"""
        return PasswordImplementer.check_password(password, self.password)

    def login(self):
        """Takes a password and if the user's password is valid.
           Returns True if the password is valid otherwise False.
        """
        self._add_username_email_and_admin_to_secure_user_session()
        self._gen_login_token()

    def _add_username_email_and_admin_to_secure_user_session(self):
        """Adds the username and admin name to the user's secure session"""

        UserSession.add_username(self.username)
        UserSession.add_value_to_session('email', self.email.lower())
        UserSession.add_value_to_session('admin', True)

    def _gen_login_token(self):
        """Generate a secure login token"""
        UserSession.add_value_to_session('login_token', gen_id())

    def get_email_confirmed_status(self):
        """Checks whether the user has confirmed their email account and returns the appropriate action.

        Returns the appropriate status based on the user's account status:

        If the user has registered but not confirmed their email address returns a 'NOT_CONFIRMED' message.
        If the user has registered and confirmed their email address Returns 'ACCOUNT_CONFIRMED'.
        if the user is not registered or is using an incorrect username/password returns 'ACCOUNT_NOT_FOUND'.
        """

        if not self.account_confirmed:
            confirmation = 'The registered email address needs to be confirmed before login can proceed'
        elif self.account_confirmed:
            confirmation = 'EMAIL_CONFIRMED'
        else:
            confirmation = 'Incorrect password and username'
        return confirmation

    def send_registration_code(self):
        """Sends a registration verification code to the user's email"""
        self._gen_registration_verification_code()
        self._email_user_verification_code()
        self._save()

    def _gen_registration_verification_code(self):
        """Generates a registration verification code"""
        self.configuration_codes['verification_code'] = self._gen_code()

    def _gen_email_change_verification_code(self):
        """Generates an email verification code"""
        self.configuration_codes['email_code'] = self._gen_code()

    def _gen_code(self):
        """Generates and returns a string code"""
        return gen_code()

    def _save(self):
        """"""
        return Record.save(self._to_json())

    def verify_forgotten_password_code(self, code):
        """Takes a username and code and verifies whether the forgotten password code
           is the one that was sent to the user.
        """
        return self.configuration_codes['forgotten_password_code'] == code

    def reset_forgotten_password(self, new_password):
        """Updates the user's forgotten password with the new password"""

        self.configuration_codes.pop('forgotten_password_code')
        self.password = PasswordImplementer.hash_password(new_password)
        self.update_account()

    def send_forgotten_password_code(self):
        """"""
        self._gen_forgotten_password_code()
        self.update_account()
        self._email_user_verification_code(code_type='forgotten_password_code')

    def _gen_forgotten_password_code(self):
        """generates a password reset code"""
        self.configuration_codes['forgotten_password_code'] = self._gen_code()

    def update_account(self):
        """Updates any changes made to the user's account"""
        Record.Update.update('_id', self._id, self._to_json())

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

    def delete_all_blogs(self):
        """Deletes all blogs created by the user"""
        self._parent_blog.delete_all_child_blogs()

    @staticmethod
    def _retreive_user_info():
        """A helper function that returns the user object"""
        return User.get_account_by_email(UserSession.get_value_by_key("email"))
