import bcrypt


class PasswordImplementer(object):
    """"""
    @staticmethod
    def check_password(password, hashed_password):
        """check_password(str, hashed str) -> returns boolean

        Takes a plain-text password and a hashed password and checks
        if that hash was created from the the plaintext password

        :param
            `password`: The plaintext password to check
            `hashed_password` : The hashed password that will be used to compare against
                                 the plaintext password.
        :returns
            Returns True if the hashed password was created from the plaintext password
            else returns False.

        >>> password = 'apple'
        >>> hashed_password = '$2a$12$wSblmWGu/urVJKE5H.oPheYwlzu9DlaGwTFTuVk8FbSsQXK503W3q'
        >>> is_password_correct = PasswordImplementer.check_password(password, hashed_password)
        >>> True
        """
        return bcrypt.checkpw(password, hashed_password)

    @staticmethod
    def hash_password(password):
        """hash_password(str) -> return(hashed str)

        Takes a plaintext password and returns a hashed version of
        the password

        :param
            `password`: The plaintext password that will be turned into a hash

        :return:
             Returns a hashed version of the string.

        >>> password = 'apple'
        >>> hashed_password = PasswordImplementer.hash_password(password)
        >>> hashed_password
        >>> '$2a$12$wSblmWGu/urVJKE5H.oPheYwlzu9DlaGwTFTuVk8FbSsQXK503W3q'
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password, salt)
