from users.utils.generator.id_generator import gen_id


class Draft(object):

    def __init__(self, blog_id, user_id):
        self._blog_id = blog_id
        self._user_id = user_id


    def save(self, post_form):
        pass

        # save to database

