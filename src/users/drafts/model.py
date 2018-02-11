from users.records.record import Record

from users.utils.generator.date_generator import time_now as date_created
from users.utils.generator.id_generator import gen_id
from users.utils.html_stripper import strip_html_tags


class Draft(object):
    """ """

    def __init__(self, blog_id, user_id):
        self.blog_id = blog_id
        self.user_id = user_id
        self.draft_id = gen_id()

    def save(self, form):
        """"""
        Record.save(self._to_json(form))

    def get_draft_post(self, draft_id, to_class=False):
        """"""

        draft = Record.Query.Filter.filter_by_key_and_value(query={
            "collection_name": "draft",
            "child_blog_id": self.blog_id,
            "user_id": self.user_id,
            "draft_id": draft_id
        })

        return _Draft(**draft) if to_class else draft

    def get_all_draft_posts(self):
        """"""

        drafts = Record.Query.find_all(query={"collection_name":"draft",
                                              "child_blog_id": self.blog_id,
                                              "user_id":self.user_id
                                              }
                                       )
        return [_Draft(**draft) for draft in drafts] if drafts else None

    def delete_draft(self, draft_id):
        """"""
        return Record.Delete.delete_draft(self.blog_id, draft_id)

    def _to_json(self, form):
        """"""
        return {
            "collection_name": "draft",
            "child_blog_id": self.blog_id,
            "user_id": self.user_id,
            "title": form.title.data,
            "post": form.post.data,
            "date_created": date_created(),
            "draft_id": self.draft_id,
        }


class _Draft(object):
    """This Draft object class should not be called directly as it is a container"""

    def __init__(self, _id, child_blog_id, user_id, draft_id, title, post, collection_name, date_created):
        self._table_name = collection_name
        self._id = _id
        self.child_blog_id = child_blog_id
        self.user_id = user_id
        self.draft_id = draft_id
        self.title = title
        self.post = post
        self.date_created = date_created

    def html_strip(self, text):
        return strip_html_tags(text)

    def update_draft(self, data):
        """"""
        Record.Update.update(field_name='draft_id', field_id=self.draft_id, data=data)
