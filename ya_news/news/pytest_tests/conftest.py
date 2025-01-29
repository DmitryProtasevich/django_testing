
from datetime import datetime, timedelta

import pytest
from django.test.client import Client
from django.utils import timezone
from news.forms import BAD_WORDS
from news.models import Comment, News
from yanews import settings


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
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
        date=datetime.today(),
    )
    return news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )
    return comment


@pytest.fixture
def all_news(news):
    all_news = [
        News(
            title=f'{news.title} {index}',
            text=f'{news.text} {index}',
            date=datetime.today() - timedelta(days=index),
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)
    return all_news


@pytest.fixture
def all_comments(news, author, comment):
    all_comments = [
        Comment(
            news=news,
            author=author,
            text=f'{comment.text} {index}',
            created=timezone.now() - timedelta(days=index),
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE)
    ]
    Comment.objects.bulk_create(all_comments)
    return all_comments


@pytest.fixture
def form_comment():
    return {'text': 'Текст комментария'}


@pytest.fixture
def bad_words_form_comment():
    return {'text': f'Текст{BAD_WORDS[0]}, комментария'}


@pytest.fixture
def form_update_comment():
    return {'text': 'Обновленный комментарий'}
