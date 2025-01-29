from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
def test_home_availability_for_anonymous_user(client):
    assert client.get(reverse('news:home')).status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_news_availability_for_anonymous_user(client, news):
    assert client.get(
        reverse('news:detail', args=(news.pk,))
    ).status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'url_name',
    ('news:edit', 'news:delete'),
)
def test_pages_comment_availability_for_author(
    author_client, comment, url_name
):
    assert author_client.get(
        reverse(url_name, args=(comment.pk,))
    ).status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url_name',
    ('news:edit', 'news:delete'),
)
def test_pages_comment_availability_for_anonymous_user(
    client, comment, url_name
):
    url = reverse(url_name, args=(comment.pk,))
    assertRedirects(client.get(url), f"{reverse('users:login')}?next={url}")


@pytest.mark.parametrize(
    'url_name',
    ('news:edit', 'news:delete'),
)
def test_pages_comment_availability_for_not_author(
    not_author_client, comment, url_name
):
    assert not_author_client.get(
        reverse(url_name, args=(comment.pk,))
    ).status_code == 404


@pytest.mark.parametrize(
    'url_name',
    ('users:login', 'users:logout', 'users:signup'),
)
def test_pages_availability_for_anonymous_user(client, url_name):
    assert client.get(reverse(url_name)).status_code == HTTPStatus.OK
