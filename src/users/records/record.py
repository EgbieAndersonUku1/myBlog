from users.records.database.database import Database
from app import cache


class Record(object):

    @staticmethod
    def save(data):
        return Database.insert_one(data)

    class Update(object):

        @staticmethod
        def update(row_name, row_id, data):
            Database.update(row_name, row_id, data)

    class Delete(object):

        @staticmethod
        def delete_blog(blog_id):
            """"""
            pass

        @staticmethod
        def delete_account(user_id):
            pass

    class Query(object):

        class Filter(object):

            @classmethod
            def filter_user_by_username(cls, username):
                return cls._filter_query('username', username)

            @classmethod
            def filter_user_by_email(cls, email):
                return  cls._filter_query('email', email)

            @classmethod
            def filter_by_id(cls, id_type, value):
                return cls._filter_query(id_type, value)

            @classmethod
            def _filter_query(cls, query_name, query_value, collection='blogs'):
                """"""
                return Database.find_one({query_name: query_value}, collection) if query_value else None

                # ToDo
                # Line 46 will be replaced by a Flask-cache
                # First, the cache will be searched
                # If the data is found in the cache then return it from the cache.
                # If the data is not found then query the database, cache the results and then return the results





