from users.authors.model import Author
from users.util.id_generator import gen_id

from users.util.date_generator import time_now


class Post(object):
    """The post allows the blog to create, save and delete a post. The
        class should not be accessed directly.
     """
    def __init__(self, user_id, blog_id, post_id):
        self._user_id = user_id
        self._blog_id = blog_id
        self._post_id = gen_id() if  post_id is None else post_id

    def get_post_by_id(self, post_id):
        """get_post_by_id(str, str) -> returns post obj

        Returns a post from .

        :param
                blog_id: The blog ID that housed the post that is been queried.
                post_id: The post ID to query from the blog.

        :returns
            returns a post object.

        >>> post = Post.get_post_by_id(blog_id, post_id)
        >>> post
        >>> post_object([.....])
        """
        # Add a function that calls the records to find the posts
        pass

    def get_all_posts(self):
        """"""
        pass

    def create_new_post(self, post_form, author_id):
        """ """

        author = Author.get_author_by_id(author_id)

        json_data = self._to_json(post_form, author)
        self.save(json_data)

    def update_post(self, post_form, post_id):
        """"""
        post = self.get_post_by_id(post_id)

        # Add the functionality to update posts here
        pass

    def delete_post(self, post_id):
        """"""
        pass

    def _save_to_blog(self, data):

        # Save to the records will add it here
        pass

    def _to_json(self, post_form, author):
        """_to_json(str, str, str) -> return dict

        Returns the data for post model object as json object

        :param
                `title`: The title for the post
                `description`: The description for the post here
                `author_id`: The author id

        :returns
                Returns a json object
        """
        return {
            "blog_id": self._blog_id,
            "post_id": self._post_id,
            "author_id": author.id,
            "title": post_form.title.title(),
            "description": post_form.description,
            "author_name": author.name,
            "post_live": True,
            "created" : time_now()
        }
