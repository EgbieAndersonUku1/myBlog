from unittest import TestCase

from src.users.records.database.database import Database
from src.users.utils.generator.id_generator import gen_id


######################################################################################
# Running the Test.
#
# To begin running the tests first start the mongod server on a terminal window
#
#
######################################################################################


def _update_data(data):

    user_data = data
    user_data['first_name'] = 'Egbie1'
    user_data['_id'] = '246810'
    return user_data

def _get_test_data():
    """"""
    return {"first_name": 'Egbie',
            "last_name": 'Uku',
            "username": 'abby',
            "email": 'egbie@example.com',
            "author_name": 'egbies',
            "password": 'password',
            "configuration_codes": gen_id(),
            "_id": '123456789'
            }


class DatabaseTest(TestCase):
    """The class is designed to test whether the database. It does so by testing a few things

       1) whether the database can successful store any user detail to the the database.
       2) whether it can successful retrieve those stored details. This is done by calling
       the database on its attributes e.g.their email, username or author name.
    """
    @classmethod
    def setUpClass(cls):
        """Initialise the entire Database class by creating a test fissure"""
        Database.db_init('test_db')
        Database.insert_one(_get_test_data(), 'test_db')

    @classmethod
    def tearDownClass(cls):
        """Tears down the database"""
        Database.remove_db('test_db')

    def test_can_a_single_user_details_be_saved_to_the_database__Should_save_the_user_details_to_database(self):
        """Test whether the database can save a single user data"""
        self.assertIsNotNone(Database.find_one({'first_name':'Egbie'}, 'test_db'))

    def test_can_two_user_details_be_saved_to_the_database__Should_save_two_the_user_details_to_database(self):
        """Test whether the database can save two user data"""

        user_data = _update_data(_get_test_data())
        Database.insert_one(user_data, 'test_db')

        query_data1 = Database.find_one({'first_name':'Egbie'}, 'test_db')
        query_data2 = Database.find_one({'first_name':'Egbie1'}, 'test_db')

        self.assertIsNotNone(query_data1, msg='The data for user1 was not returned')
        self.assertIsNotNone(query_data2, msg='The data for user2 was not returned')

    def test_can_the_user_data_be_retreived_from_the_database_using_a_correct_username__Should_retreive_all_data_belonging_to_the_user(self):
        """A test to see whether the database can retrieve the user using the correct username"""
        self.assertIsNotNone(Database.find_one({'username': 'abby'}, 'test_db'))

    def test_can_the_user_data_be_retreived_from_the_database_when_an_invalid_username_is_entered__Should_return_none(self):
        """A test to see whether the database retrieves the user's data using an incorrect username"""
        self.assertIsNone(Database.find_one({'username': 'name_does_not_exist_in_db'}, 'test_db'))

    def test_can_the_user_data_be_retrieived_from_the_database_with_a_correct_email_address__Should_return_all_data_belonging_to_the_user(self):
        """A test to see whether the database can retrieve data using the correct email address"""
        self.assertIsNotNone(Database.find_one({'email': 'egbie@example.com'}, 'test_db'))

    def test_can_the_user_data_be_retreived_from_the_database_when_an_invalid_email_is_entered__Should_return_none(self):
        """A test to see whether the database retrieves the user's data using an incorrect email"""
        self.assertIsNone(Database.find_one({'email': 'email_does_not_exist@example.com'}, 'test_db'))

    def test_can_the_user_data_be_retrieived_from_the_database_using_the_author_name__Should_return_all_data_belonging_to_the_user(self):
        """A test to see whether the database can retrieve data using the correct author name"""
        self.assertIsNotNone(Database.find_one({'author_name': 'egbies'}, 'test_db'))

    def test_can_the_user_data_be_retrieived_from_the_database_using_an_incorrect_author_name__Should_return_none(self):
        """A test to see whether the database retrieves the user's data using an incorrect author name"""
        self.assertIsNone(Database.find_one({'author_name': 'fake_name'}, 'test_db'))

    def test_can_the_user_update_the_data_in_the_database__Should_update_the_user_details(self):
        """Test whether the database can be used to update the user's details """

        data = Database.find_one({'first_name': 'Egbie'}, 'test_db')
        data['last_name'] = 'Ullu'
        Database.update('_id', '123456789', data, 'test_db')
        self.assertIsNotNone(Database.find_one({'last_name': 'Ullu'}, 'test_db'))
