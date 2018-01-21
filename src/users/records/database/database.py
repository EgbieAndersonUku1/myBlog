import pymongo

__author__ = 'Egbie Uku'


class Database(object):
    """Database(class): Will store all the users in the blog"""

    DATABASE = None
    URI = 'mongodb://127.0.0.1:27017'
    client = None

    @classmethod
    def db_init(cls, database_name='blogs'):
        """Initalize the database"""

        client = cls.setup(database_name)
        cls._create_indexes()

    @classmethod
    def setup(cls, database_name):
        """For maual setup the database"""

        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client[database_name]
        Database.client = client

    @classmethod
    def remove_db(cls, db_name):
        """"""
        Database.client.drop_database(db_name)

    @classmethod
    def _create_indexes(cls):
        """Create the indexes in the database for faster lookup"""

        blog = Database.client['blogs']['blog']
        blog.create_index([('user_id', pymongo.ASCENDING)])
        blog.create_index([('author_id', pymongo.ASCENDING)])
        blog.create_index([('parent_blog_id', pymongo.ASCENDING)])
        blog.create_index([('child_blog_id', pymongo.ASCENDING)])
        blog.create_index([('blog_live', pymongo.ASCENDING)])
        blog.create_index([('post_live', pymongo.ASCENDING)])
        blog.create_index([('email', pymongo.ASCENDING)])
        blog.create_index([('time_created', pymongo.ASCENDING)])

    @staticmethod
    def insert_one(data, db_name="blogs"):
        """insert_one(str) -> return(boolean)
        Inserts data into a given db_name(table) for a given database.

        :parameter
           `db_name`: The table name for the data to be inserted into.
           `data`: The data will be inserted into the db_name.
        :returns
            Returns True if the data was successful saved to database else False
        """
        return True if Database.DATABASE[db_name].insert(data) else False

    @staticmethod
    def find_all(blog_id, db_name="blogs"):
        """find_all(str) -> return(cursor)
        Returns all users in the db_name.
        """
        return Database.DATABASE[db_name].find({"parent_blog_id": blog_id, "blog_live": True})

    @staticmethod
    def find_one(query, db_name="blogs"):
        """find_one(str, dict) -> return(dict)

        Return a json object from from the database.

        parameters:
           - collections: A table name from the database
           - query      : The information to query from the database
        """
        return Database.DATABASE[db_name].find_one(query)

    @classmethod
    def delete_one(cls, db_name="blogs", data=None):
        """delete_row(str, dict) -> return(None)

        Deletes and entry from the row. Returns True
        if name was successful deleted otherwise False.

        parameters:
           - collections: A table name from the database
           - data      : The information to delete from the database
        """
        Database.DATABASE[db_name].delete_one(data)

    @staticmethod
    def update(field_name, field_value, data, db_name="blogs"):
        """update_row(str, str, dict) -> return(None)

        Updates a single row in the table.

        parameters:
           - collections: A table name from the database.
           - field_name & field_value :
                        The field_name and field_value work as a pair.
                        They are both used to identify the document
                        that will be updated.
           - data       : The information used to update to the database
        """
        Database.DATABASE[db_name].update({field_name:field_value}, {'$set': data})


