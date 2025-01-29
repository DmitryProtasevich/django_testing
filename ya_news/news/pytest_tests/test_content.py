
import pytest
from django.urls import reverse
from yanews import settings


def test_news_qty_on_page(author_client, all_news):
    assert (
        len(author_client.get(reverse('news:home'))
            .context['object_list']) == settings.NEWS_COUNT_ON_HOME_PAGE
    )


def test_sort_date(author_client, all_news):
    all_dates = [
        news.date for news in author_client
        .get(reverse('news:home')).context['object_list']
    ]
    assert all_dates == sorted(all_dates, reverse=True)


def test_sort_comment(author_client, all_comments, news):
    news = (
        author_client.get(reverse('news:detail', args=(news.pk,)))
        .context['news']
    )
    all_timestamps = [comment.created for comment in all_comments]
    assert all_timestamps == sorted(all_timestamps)


@pytest.mark.django_db
def test_anonymous_client_has_no_form_for_comment(author_client, client, news):
    url = reverse('news:detail', args=(news.pk,))
    response = author_client.get(url)
    assert 'form' in response.context
    response = client.get(url)
    assert 'form' not in response.context
