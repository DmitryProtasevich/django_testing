from news.forms import CommentForm
from yanews import settings


def test_news_qty_on_page(author_client, all_news, news_urls):
    assert (
        len(author_client.get(news_urls['home'])
            .context['object_list']) == settings.NEWS_COUNT_ON_HOME_PAGE
    )


def test_sort_date(author_client, news_urls):
    all_dates = [
        news.date for news in author_client
        .get(news_urls['home']).context['object_list']
    ]
    assert all_dates == sorted(all_dates, reverse=True)


def test_sort_comment(author_client, all_comments, news_urls):
    author_client.get(news_urls['detail']).context['news']
    all_timestamps = [comment.created for comment in all_comments]
    assert all_timestamps == sorted(all_timestamps)


def test_author_client_has_form_for_comment(author_client, news_urls):
    response = author_client.get(news_urls['detail'])
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


def test_anonymous_client_has_no_form_for_comment(client, news_urls):
    assert 'form' not in client.get(news_urls['detail']).context
