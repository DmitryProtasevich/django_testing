from http import HTTPStatus

from notes.tests.constants import BaseTest, get_redirect_url


class TestRoutes(BaseTest):

    def test_status_codes(self):
        test_cases = [
            (self.NOTES_HOME_URL, self.client, HTTPStatus.OK),
            (self.USERS_LOGIN_URL, self.client, HTTPStatus.OK),
            (self.USERS_LOGOUT_URL, self.client, HTTPStatus.OK),
            (self.USERS_SIGNUP_URL, self.client, HTTPStatus.OK),

            (self.USERS_LOGIN_URL, self.other_author, HTTPStatus.OK),
            (self.USERS_LOGOUT_URL, self.other_author, HTTPStatus.OK),
            (self.USERS_SIGNUP_URL, self.other_author, HTTPStatus.OK),
            (self.NOTES_ADD_URL, self.other_author, HTTPStatus.OK),
            (self.NOTES_LIST_URL, self.other_author, HTTPStatus.OK),
            (self.NOTES_SUCCESS_URL, self.other_author, HTTPStatus.OK),
            (self.NOTES_DETAIL_URL, self.other_author, HTTPStatus.NOT_FOUND),
            (self.NOTES_DELETE_URL, self.other_author, HTTPStatus.NOT_FOUND),
            (self.NOTES_EDIT_URL, self.other_author, HTTPStatus.NOT_FOUND),

            (self.USERS_LOGIN_URL, self.author, HTTPStatus.OK),
            (self.USERS_LOGOUT_URL, self.author, HTTPStatus.OK),
            (self.USERS_SIGNUP_URL, self.author, HTTPStatus.OK),
            (self.NOTES_DETAIL_URL, self.author, HTTPStatus.OK),
            (self.NOTES_DELETE_URL, self.author, HTTPStatus.OK),
            (self.NOTES_EDIT_URL, self.author, HTTPStatus.OK),
        ]

        for url, client, expected_status in test_cases:
            with self.subTest(url=url, client=client):
                if client != self.client:
                    self.client.force_login(client)
                self.assertEqual(
                    self.client.get(url).status_code,
                    expected_status
                )

    def test_redirect_anonymous_users_to_login(self):
        urls = (
            (self.NOTES_LIST_URL),
            (self.NOTES_ADD_URL),
            (self.NOTES_DETAIL_URL),
            (self.NOTES_DELETE_URL),
            (self.NOTES_EDIT_URL),
        )
        for url in urls:
            with self.subTest(name=url):
                self.assertRedirects(
                    self.client.get(url),
                    get_redirect_url(url)
                )
