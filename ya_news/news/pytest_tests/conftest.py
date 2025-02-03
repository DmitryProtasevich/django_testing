from datetime import datetime, timedelta

import pytest
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News
from yanews import settings


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def news_home_url():
    return reverse('news:home')


@pytest.fixture
def news_detail_url(news):
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture
def user_login_url():
    return reverse('users:login')


@pytest.fixture
def user_logout_url():
    return reverse('users:logout')


@pytest.fixture
def user_signup_url():
    return reverse('users:signup')


@pytest.fixture
def comment_edit_url(comment):
    return reverse('news:edit', args=(comment.pk,))


@pytest.fixture
def comment_delete_url(comment):
    return reverse('news:delete', args=(comment.pk,))


@pytest.fixture
def redirect_edit_url(user_login_url, comment_edit_url):
    return f"{user_login_url}?next={comment_edit_url}"


@pytest.fixture
def redirect_delete_url(user_login_url, comment_delete_url):
    return f"{user_login_url}?next={comment_delete_url}"


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )


@pytest.fixture
def all_news(news):
    return News.objects.bulk_create(
        News(
            title=f'{news.title} {index}',
            text=f'{news.text} {index}',
            date=datetime.today() - timedelta(days=index),
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def all_comments(news, author, comment):
    COMMENTS_QTY = 5
    all_comments = []
    for index in range(COMMENTS_QTY):
        new_comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'{comment.text} {index}',
        )
        new_comment.created = timezone.now() + timedelta(days=index)
        new_comment.save()
        all_comments.append(new_comment)
    return all_comments
