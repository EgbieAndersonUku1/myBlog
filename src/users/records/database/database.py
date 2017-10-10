import pymongo

__author__ = 'Egbie Uku'


class Database(object):
    """Database(class): Will store all the users in the blog"""

    DATABASE = None
    URI = 'mongodb://127.0.0.1:27017'

    @classmethod
    def db_init(cls):
        """Initalize the database"""
        client = cls._setup()
        cls._create_indexes(client)
    
    @classmethod
    def _setup(cls):
        """Setups the databases"""
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['blog']
        return client
    
    @classmethod
    def _create_indexes(cls, client):
        """Create the indexes in the database for faster lookup"""
        blog = client['blog']['blog']
        blog.create_index([('user_name', pymongo.ASCENDING)])
        blog.create_index([('email', pymongo.ASCENDING)])
        blog.create_index([('time_created', pymongo.ASCENDING)])

    @staticmethod
    def insert_one(collection, data):
        """insert_one(str) -> return(none)
        Inserts data into a collection(table) for a given database.

        :parameters
            - collection: The table name for the data to be inserted into.
            - data: The data will be inserted into the collection.
        """
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find_all(collection):
        """find_all(str) -> return(cursor)
        Returns all users in the collection.
        """
        return Database.DATABASE[collection].find()

    @staticmethod
    def find_one(collection, query):
        """find_one(str, dict) -> return(dict)

        Return a json object from from the database.

        parameters:
           - collections: A table name from the database
           - query      : The information to query from the database
        """
        return Database.DATABASE[collection].find_one(query)

    @classmethod
    def delete_one(cls, collection, data):
        """delete_row(str, dict) -> return(None)

        Deletes and entry from the row. Returns True
        if name was successful deleted otherwise False.

        parameters:
           - collections: A table name from the database
           - data      : The information to delete from the database
        """
        Database.DATABASE[collection].find_one_and_delete(data)
        return False if cls.find_one(collection, data) else True

    @staticmethod
    def update(collection, field_name, field_id , data):
        """update_row(str, str, dict) -> return(None)

        Updates a single row in the table.

        parameters:
           - collections: A table name from the database.
           - field_name & field_id :
                        The field_name and field_id work as a pair.
                        They are both used to identify the document
                        that will be updated.
           - data       : The information used to update to the database
        """
        Database.DATABASE[collection].update({field_name:field_id}, {'$set': data})