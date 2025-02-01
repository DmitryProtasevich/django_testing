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
def news_urls(news):
    return {
        'home': reverse('news:home'),
        'detail': reverse('news:detail', args=(news.pk,)),
    }


@pytest.fixture
def user_urls():
    return {
        'login': reverse('users:login'),
        'logout': reverse('users:logout'),
        'signup': reverse('users:signup'),
    }


@pytest.fixture
def expected_redirect_url(user_urls):
    return f"{user_urls['login']}?next="


@pytest.fixture
def comment_urls(comment):
    return {
        'edit': reverse('news:edit', args=(comment.pk,)),
        'delete': reverse('news:delete', args=(comment.pk,)),
    }


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
        date=datetime.today(),
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
    return News.objects.bulk_create([
        News(
            title=f'{news.title} {index}',
            text=f'{news.text} {index}',
            date=datetime.today() - timedelta(days=index),
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ])


@pytest.fixture
def all_comments(news, author, comment):
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE):
        Comment.objects.create(
            news=news,
            author=author,
            text=f'{comment.text} {index}',
            created=timezone.now() - timedelta(days=index),
        )
    return Comment.objects.filter(news=news)
