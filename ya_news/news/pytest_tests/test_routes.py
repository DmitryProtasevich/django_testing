from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'url, client_fixture, expected_status',
    [
        (pytest.lazy_fixture('news_urls'),
         pytest.lazy_fixture('client'), HTTPStatus.OK),
        (pytest.lazy_fixture('user_urls'),
         pytest.lazy_fixture('client'), HTTPStatus.OK),
        (pytest.lazy_fixture('comment_urls'),
         pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('comment_urls'),
         pytest.lazy_fixture('author_client'), HTTPStatus.OK),
    ],
)
def test_pages_availability(url, client_fixture, expected_status):
    for endpoint in url.values():
        assert client_fixture.get(endpoint).status_code == expected_status


def test_redirect_for_anonymous_users(
    comment_urls, client, expected_redirect_url
):
    for endpoint in comment_urls.values():
        assertRedirects(client.get(endpoint), expected_redirect_url + endpoint)
