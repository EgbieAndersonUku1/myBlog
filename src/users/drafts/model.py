from users.records.record import Record

from users.utils.generator.date_generator import time_now as date_created
from users.utils.generator.id_generator import gen_id


class Draft(object):
    """ """

    def __init__(self, blog_id, post_id):
        self.blog_id = blog_id
        self.post_id = post_id
        self.draft_id = gen_id()

    def save(self, form):
        """"""
        Record.save(self._to_json(form))

    def get_draft_post(self, draft_id):
        """"""

        return Record.Query.Filter.filter_by_key_and_value(query={
            "collection_name": "draft",
            "blog_id": self.blog_id,
            "post_id": self.post_id,
            "draft_id": draft_id
        })

    def get_all_draft_posts(self):
        """"""

        drafts = Record.Query.find_all(query={"collection_name":"draft", "blog_id": self.blog_id, "post_id":self.post_id})
        return [_Draft(**draft) for draft in drafts] if drafts else None

    def delete_draft(self, draft_id):
        """"""
        return Record.Delete.delete_draft(self.blog_id, draft_id)

    def _to_json(self, form):
        """"""
        return {
            "collection_name": "draft",
            "blog_id": self.blog_id,
            "post_id": self.post_id,
            "title": form.title.data,
            "post": form.description.data,
            "date_created": date_created(),
            "draft_id": self.draft_id,

        }


class _Draft(object):
    """ """

    def __init__(self, _id, blog_id, post_id, draft_id, title, post, collection_name, date_created):
        self._table_name = collection_name
        self._id = _id
        self._blog_id = blog_id
        self.post_id = post_id
        self.draft_id = draft_id
        self.title = title
        self.post = post
        self.date_created = date_created
