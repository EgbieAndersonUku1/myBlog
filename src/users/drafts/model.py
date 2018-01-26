from users.records.record import Record


class Draft(object):
    """ """

    def __init__(self, blog_id, post_id):
        self._blog_id = blog_id
        self.post_id = post_id

    def save(self, form):
        """"""
        Record.save(self._to_json(form))

    def get_draft_post(self, post_id):
        pass

    @classmethod
    def get_all_draft_posts(cls, post_id, blog_id):

        drafts = Record.Query.find_all(query={"collection_name":"draft", "blog_id": blog_id})
        return [_Draft(**draft) for draft in drafts] if drafts.count() else None

    def _to_json(self, form):
        """"""
        return {
            "collection_name": "draft",
            "blog_id": self._blog_id,
            "post_id": self.post_id,
            "title": form.title.data,
            "post": form.description.data,
        }


class _Draft(object):
    """ """

    def __init__(self, blog_id, post_id, title, post):
        self._blog_id = blog_id
        self.post_id = post_id
        self.title = title
        self.post = post