from http import HTTPStatus

from ya_note.notes.tests.utils import (
    BaseTest,
    NOTES_EDIT_URL,
    NOTES_DELETE_URL,
    NOTES_DETAIL_URL,
    NOTES_ADD_URL,
    NOTES_LIST_URL,
    NOTES_HOME_URL,
    NOTES_SUCCESS_URL,
    USERS_LOGIN_URL,
    USERS_LOGOUT_URL,
    USERS_SIGNUP_URL,
    REDIRECT_LIST_URL,
    REDIRECT_ADD_URL,
    REDIRECT_DETAIL_URL,
    REDIRECT_DELETE_URL,
    REDIRECT_EDIT_URL
)


class TestRoutes(BaseTest):

    def test_status_codes(self):
        test_cases = [
            (NOTES_HOME_URL, self.client, HTTPStatus.OK),
            (USERS_LOGIN_URL, self.client, HTTPStatus.OK),
            (USERS_LOGOUT_URL, self.client, HTTPStatus.OK),
            (USERS_SIGNUP_URL, self.client, HTTPStatus.OK),

            (NOTES_ADD_URL, self.other_author_client, HTTPStatus.OK),
            (NOTES_LIST_URL, self.other_author_client, HTTPStatus.OK),
            (NOTES_SUCCESS_URL, self.other_author_client, HTTPStatus.OK),
            (NOTES_DETAIL_URL, self.other_author_client, HTTPStatus.NOT_FOUND),
            (NOTES_DELETE_URL, self.other_author_client, HTTPStatus.NOT_FOUND),
            (NOTES_EDIT_URL, self.other_author_client, HTTPStatus.NOT_FOUND),
            (USERS_LOGIN_URL, self.other_author_client, HTTPStatus.OK),
            (USERS_SIGNUP_URL, self.other_author_client, HTTPStatus.OK),
            (USERS_LOGOUT_URL, self.other_author_client, HTTPStatus.OK),

            (NOTES_DETAIL_URL, self.author_client, HTTPStatus.OK),
            (NOTES_DELETE_URL, self.author_client, HTTPStatus.OK),
            (NOTES_EDIT_URL, self.author_client, HTTPStatus.OK),
            (USERS_LOGIN_URL, self.author_client, HTTPStatus.OK),
            (USERS_SIGNUP_URL, self.author_client, HTTPStatus.OK),
            (USERS_LOGOUT_URL, self.author_client, HTTPStatus.OK),

            (NOTES_LIST_URL, self.client, HTTPStatus.FOUND),
            (NOTES_ADD_URL, self.client, HTTPStatus.FOUND),
            (NOTES_DETAIL_URL, self.client, HTTPStatus.FOUND),
            (NOTES_DELETE_URL, self.client, HTTPStatus.FOUND),
            (NOTES_EDIT_URL, self.client, HTTPStatus.FOUND),
        ]

        for url, client, expected_status in test_cases:
            with self.subTest(url=url, client=client):
                self.assertEqual(
                    client.get(url).status_code,
                    expected_status,
                )

    def test_redirect_anonymous_users_to_login(self):
        urls = (
            (NOTES_LIST_URL, REDIRECT_LIST_URL),
            (NOTES_ADD_URL, REDIRECT_ADD_URL),
            (NOTES_DETAIL_URL, REDIRECT_DETAIL_URL),
            (NOTES_DELETE_URL, REDIRECT_DELETE_URL),
            (NOTES_EDIT_URL, REDIRECT_EDIT_URL),
        )
        for url, redirect_url in urls:
            with self.subTest(name=url):
                self.assertRedirects(
                    self.client.get(url),
                    redirect_url
                )
