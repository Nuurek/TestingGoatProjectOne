from django.conf import settings
from .base import FunctionalTest
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        response = self.client.get(
            '/rest/session_key/{}/'.format(email),
        )
        print(response.content)
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        session_key = data['session_key']
        # To set a cookie we need to first visit the domain
        # 404 pages load the quickest
        self.browser.get(self.server_url + "/404_no_such_url")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'example@example.com'
        self.browser.get(self.server_url)
        self.assert_logged_out(email)

        # Edith is a logged-in user
        self.create_pre_authenticated_session(email)
        self.browser.get(self.server_url)
        self.assert_logged_in(email)
