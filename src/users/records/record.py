from users.records.database.database import Database


class Record(object):

    @staticmethod
    def save(data):
        return Database.insert_one(data)

    class Update(object):

        @staticmethod
        def update(field_name, field_id, data):
            Database.update(field_name, field_id, data)

    class Delete(object):

        @classmethod
        def delete_blog(cls, blog_id):
            """"""
            cls._cascade_delete(data={"child_blog_id": blog_id})

        @classmethod
        def delete_all_blogs(cls, data):
            """"""
            assert type(data) == list
            cls._cascade_delete(data={"$or": data})

        @classmethod
        def delete_post(cls, blog_id, post_id):
            cls._delete(data={"child_blog_id": blog_id, "child_post_id": post_id})

        @classmethod
        def delete_draft(cls, blog_id, draft_id):
            cls._delete(data={"child_blog_id": blog_id, "draft_id": draft_id})

        @classmethod
        def delete_comment(cls, blog_id, comment_id):
            cls._delete(data={"child_blog_id": blog_id, "comment_id": comment_id})

        @staticmethod
        def _delete(data):
            assert type(data) == dict
            Database.delete_one(data=data)

        @staticmethod
        def _cascade_delete(data):
            """"""
            assert type(data) == dict
            Database.cascade_delete(data=data)

    class Query(object):

        @staticmethod
        def find_all(query):
            return Database.find_all(query)

        class Filter(object):

            @classmethod
            def filter_user_by_username(cls, username):
                return cls._filter_query({'username': username.lower()})

            @classmethod
            def filter_user_by_email(cls, email):
                return cls._filter_query({'email': email.lower()})

            @classmethod
            def filter_user_by_id(cls, user_id):
                return cls._filter_query({'user_id': user_id})

            @classmethod
            def filter_by_key_and_value(cls, query):
                return cls._filter_query(query)

            @classmethod
            def _filter_query(cls, query, collection='blogs'):
                """"""
                assert type(query) == dict
                return Database.find_one(query, collection) if query else None

                # ToDo
                # Use Flask-cache
                # First, the cache will be searched
                # If the data is found in the cache then return it from the cache.
                # If the data is not found then query the database, cache the results and then return the results

