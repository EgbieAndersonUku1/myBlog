from users.utils.session.user_session import UserSession
from users.users.profile_images import ProfileImages
from app import cache
#from users.users.helper import to_class, update_db, save_to_db

from users.records.record import Record
from users.users.users import User


class UserProfile(object):
    """"""

    def __init__(self, first_name, last_name, username, email, bio, profile_img):
        self.profile_id = self.get_profile_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.bio = bio
        self.profile_img = ProfileImages(self.profile_id, profile_img)

    @cache.memoize(600)
    def get_profile(self):
        pass
        #return to_class(UserProfile, Record.Query.Filter.filter_by_key_and_value(self.profile_id))

    def save(self):
        """"""
        return Record.save(self._to_json())

    def update(self):
        """"""
        Record.Update.update('profile_id', self.profile_id, self._to_json())

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

