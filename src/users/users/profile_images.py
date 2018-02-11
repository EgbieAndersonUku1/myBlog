from users.records.record import Record
from app import cache

class ProfileImages(object):

    def __init__(self, profile_image_id, img):
        self.profile_image_id = profile_image_id
        self.img = img
        self._save()

    def _save(self):
        Record._save(self._to_json())

    @cache.memoize(300)
    def get_image(self):
        Record.Query.Filter.filter_by_key_and_value("profile_image_id", self.profile_image_id)

    def _to_json(self):
        return {"profile_image_id": self.profile_image_id,
                "image": self.img
        }