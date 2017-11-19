from unittest import TestCase

from users.users.users import User
from users.utils.generator.id_generator import gen_id


class RegistrationTest(TestCase):

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

    def test_if_a_single_user_details_can_be_saved_to_the_database__should_save_the_user_details_to_database(self):
        pass

    def test_if_two_user_details_can_be_saved_to_the_database__should_save_two_the_user_details_to_database(self):
        pass

    def test_if_three_user_details_can_be_saved_to_the_database__should_save_three_user_details_to_database(self):
        pass

    def test_if_a_user_data_can_be_retreived_by_using_a_correct_username__should_retreive_all_data_belonging_to_the_user(self):
        pass

    def test_if_user_data_can_retreived_from_the_database_if_an_invalid_username_is_entered__should_return_a_none(self):
        pass

    def test_if_user_data_can_be_retrieived_from_database_with_a_correct_email_address__should_return_all_data_belonging_to_the_user(self):
        pass

    def test_if_user_data_is_converted_to_json__should_return_a_json_object(self):
        pass

    def test_if_user_account_verification_code_is_generated__should_generate_a_random_generated_string(cls):
        pass

    def test_if_an_assertion_error_is_raised_if_no_details_is_entered(self):
        pass

    def test_if_user_blog_id_code_is_generated__should_generate_a_random_generated_string(cls):
        pass

    def test_if_user_author_id_code_is_generated__should_generate_a_random_generated_string(cls):
        pass

    def test_repr_when_data_is_passed_to_the_object__should_return_a_string_with_first_name_and_a_last_name(self):
        pass

