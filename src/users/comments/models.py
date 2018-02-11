from users.records.record import Record
from users.utils.generator.date_generator import time_now as date_created

from users.utils.generator.id_generator import gen_id


class Comment(object):

    def __init__(self, blog_id, user_id, post_id):
        self.blog_id = blog_id
        self.user_id = user_id
        self.post_id = post_id

    def get_comment(self, comment_id):
        pass

    def delete_comment(self, comment_id):
        """"""
        Record.Delete.delete_comment(self.blog_id, comment_id)

    def get_all_comments(self):
        """"""
        comments = Record.Query.find_all(query={"collection_name":"comments",
                                     "child_blog_id": self.blog_id,
                                     "user_id": self.user_id,
                                     "comment_live": True,
                                     "post_id":self.post_id,
                                     })
        if comments:
            return [_Comment(**comment) for comment in comments]

    def save_comment(self,comment):
        """"""
        Record.save(self._to_json(comment))

    def _to_json(self, comment):
        return {
            "comment": comment,
            "collection_name": "comments",
            "child_blog_id": self.blog_id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "comment_live": True,
            "comment_on": date_created(),
            "comment_id": gen_id(),
        }


class _Comment(object):
    def __init__(self, user_id, child_blog_id, post_id, comment,
                 comment_live, comment_id, collection_name, comment_on, _id):
        self.user_id = user_id
        self.child_blog_id = child_blog_id
        self.post_id = post_id
        self.comment = comment
        self.comment_id = comment_id
        self.comment_live = comment_live
        self.collection_name = collection_name
        self.comment_on = comment_on
        self._id = _id


    def delete_comment(self, comment_id):
        """"""
        Record.Delete.delete_comment(self.blog_id, comment_id)