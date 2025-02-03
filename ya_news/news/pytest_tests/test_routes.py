from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

CLIENT_FIXTURE = pytest.lazy_fixture('client')
NOT_AUTHOR_CLIENT_FIXTURE = pytest.lazy_fixture('not_author_client')
AUTHOR_CLIENT_FIXTURE = pytest.lazy_fixture('author_client')
NEWS_HOME_FIXTURE = pytest.lazy_fixture('news_home_url')
NEWS_DETAIL_FIXTURE = pytest.lazy_fixture('news_detail_url')
USER_LOGIN_FIXTURE = pytest.lazy_fixture('user_login_url')
USER_LOGOUT_FIXTURE = pytest.lazy_fixture('user_logout_url')
USER_SIGNUP_FIXTURE = pytest.lazy_fixture('user_signup_url')
COMMENT_EDIT_FIXTURE = pytest.lazy_fixture('comment_edit_url')
COMMENT_DELETE_FIXTURE = pytest.lazy_fixture('comment_delete_url')
REDIRECT_EDIT_URL = pytest.lazy_fixture('redirect_edit_url')
REDIRECT_DELETE_URL = pytest.lazy_fixture('redirect_delete_url')


@pytest.mark.parametrize(
    'url, client_fixture, expected_status',
    [
        (NEWS_HOME_FIXTURE, CLIENT_FIXTURE, HTTPStatus.OK),
        (NEWS_DETAIL_FIXTURE, CLIENT_FIXTURE, HTTPStatus.OK),
        (USER_LOGIN_FIXTURE, CLIENT_FIXTURE, HTTPStatus.OK),
        (USER_LOGOUT_FIXTURE, CLIENT_FIXTURE, HTTPStatus.OK),
        (USER_SIGNUP_FIXTURE, CLIENT_FIXTURE, HTTPStatus.OK),
        (COMMENT_EDIT_FIXTURE, CLIENT_FIXTURE, HTTPStatus.FOUND),
        (COMMENT_DELETE_FIXTURE, CLIENT_FIXTURE, HTTPStatus.FOUND),
        (COMMENT_EDIT_FIXTURE,
         NOT_AUTHOR_CLIENT_FIXTURE, HTTPStatus.NOT_FOUND),
        (COMMENT_DELETE_FIXTURE,
         NOT_AUTHOR_CLIENT_FIXTURE, HTTPStatus.NOT_FOUND),
        (COMMENT_EDIT_FIXTURE, AUTHOR_CLIENT_FIXTURE, HTTPStatus.OK),
        (COMMENT_DELETE_FIXTURE, AUTHOR_CLIENT_FIXTURE, HTTPStatus.OK),
    ],
)
def test_pages_availability(url, client_fixture, expected_status):
    assert client_fixture.get(url).status_code == expected_status


@pytest.mark.parametrize(
    'url, redirect_url',
    [
        (COMMENT_EDIT_FIXTURE, REDIRECT_EDIT_URL),
        (COMMENT_DELETE_FIXTURE, REDIRECT_DELETE_URL),
    ]
)
def test_redirect_for_anonymous_users(client, url, redirect_url):
    assertRedirects(client.get(url), redirect_url)
