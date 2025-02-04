from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

CLIENT = pytest.lazy_fixture('client')
NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
NEWS_HOME = pytest.lazy_fixture('news_home_url')
NEWS_DETAIL = pytest.lazy_fixture('news_detail_url')
USER_LOGIN = pytest.lazy_fixture('user_login_url')
USER_LOGOUT = pytest.lazy_fixture('user_logout_url')
USER_SIGNUP = pytest.lazy_fixture('user_signup_url')
COMMENT_EDIT = pytest.lazy_fixture('comment_edit_url')
COMMENT_DELETE = pytest.lazy_fixture('comment_delete_url')
REDIRECT_EDIT_URL = pytest.lazy_fixture('redirect_edit_url')
REDIRECT_DELETE_URL = pytest.lazy_fixture('redirect_delete_url')


@pytest.mark.parametrize(
    'url, client_fixture, expected_status',
    [
        (NEWS_HOME, CLIENT, HTTPStatus.OK),
        (NEWS_DETAIL, CLIENT, HTTPStatus.OK),
        (USER_LOGIN, CLIENT, HTTPStatus.OK),
        (USER_LOGOUT, CLIENT, HTTPStatus.OK),
        (USER_SIGNUP, CLIENT, HTTPStatus.OK),
        (COMMENT_EDIT, CLIENT, HTTPStatus.FOUND),
        (COMMENT_DELETE, CLIENT, HTTPStatus.FOUND),
        (COMMENT_EDIT,
         NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (COMMENT_DELETE,
         NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (COMMENT_EDIT, AUTHOR_CLIENT, HTTPStatus.OK),
        (COMMENT_DELETE, AUTHOR_CLIENT, HTTPStatus.OK),
    ],
)
def test_pages_availability(url, client_fixture, expected_status):
    assert client_fixture.get(url).status_code == expected_status


@pytest.mark.parametrize(
    'url, redirect_url',
    [
        (COMMENT_EDIT, REDIRECT_EDIT_URL),
        (COMMENT_DELETE, REDIRECT_DELETE_URL),
    ]
)
def test_redirect_for_anonymous_users(client, url, redirect_url):
    assertRedirects(client.get(url), redirect_url)
