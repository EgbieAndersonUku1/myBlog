from users.records.database.database import Database


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
                return cls._filter_query({'username': username.lower()})

            @classmethod
            def filter_user_by_email(cls, email):
                return  cls._filter_query({'email': email.lower()})

            @classmethod
            def filter_user_by_id(cls, user_id):
                return cls._filter_query(user_id)

            @classmethod
            def _filter_query(cls, query, collection='blogs'):
                return Database.find_one(query, collection) # Cache system to go here.
                # ToDo
                # First, the cache will be searched
                # If the data is found in the cache then return it from the cache.
                # If the data is not found then query the database, cache the results and then return the results





