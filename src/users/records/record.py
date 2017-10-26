from users.records.database.database import Database


class Record(object):

    @staticmethod
    def save(data):
        pass
        #return Database.insert_one(data)

    class Update(object):

        @staticmethod
        def update(rec):
            pass

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
            def filter_user_by_email(cls, email):
                return  cls._filter_query(email)

            @classmethod
            def filter_user_by_id(cls, user_id):
                return cls._filter_query(user_id)

            @classmethod
            def _filter_query(query, collection='blogs'):
                return Database.find_one(query, collection)



