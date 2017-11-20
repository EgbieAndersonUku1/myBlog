from unittest import TestCase

from src.users.records.database.database import Database
from src.users.utils.generator.id_generator import gen_id


class DataBaseTest(TestCase):

    def setUpClass(cls):
        """"""
        setup_data = { "first_name": 'Egbie',
                       "last_name": 'Uku',
                       "username": 'abby',
                       "email": 'egbie@example.com',
                       "author_name": 'egbies',
                       "password": 'password',
                       "configuration_codes" : gen_id()
        }
        Database.db_init()

    def test_if_a_single_user_details_can_be_saved_to_the_database__Should_save_the_user_details_to_database(self):
        pass

    def test_if_two_user_details_can_be_saved_to_the_database__Should_save_two_the_user_details_to_database(self):
        pass

    def test_if_three_user_details_can_be_saved_to_the_database__Should_save_three_user_details_to_database(self):
        pass

    def test_if_a_user_data_can_be_retreived_from_the_database_using_a_correct_username__Should_retreive_all_data_belonging_to_the_user(self):
        pass

    def test_if_user_data_can_retreived_from_the_database_with_an_invalid_username_is_entered__Should_return_none(self):
        pass

    def test_if_user_data_can_be_retrieived_from_database_with_a_correct_email_address__Should_return_all_data_belonging_to_the_user(self):
        pass

    def test_if_user_data_can_retreived_from_the_database_with_an_invalid_email_is_entered__Should_return_none(self):
        pass
