from http import HTTPStatus

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

FORM_COMMENT = {'text': 'Текст'}


def test_anonymous_user_cant_create_comment(client, news_detail_url):
    client.post(news_detail_url, data=FORM_COMMENT)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(author_client, author, news, news_detail_url):
    author_client.post(
        news_detail_url, data=FORM_COMMENT
    )
    assert Comment.objects.count() == 1
    comment = Comment.objects.last()
    assert comment.news == news
    assert comment.author == author
    assert comment.text == FORM_COMMENT['text']


def test_user_cant_use_bad_words(author_client, news_detail_url):
    for bad_word in BAD_WORDS:
        assert WARNING in author_client.post(
            news_detail_url,
            data={'text': f"{FORM_COMMENT['text']} {bad_word}"}
        ).context['form'].errors['text']
        assert Comment.objects.count() == 0


def test_author_can_update_comment(
    author_client, comment, comment_edit_url, news, author
):
    author_client.post(
        comment_edit_url, data=FORM_COMMENT
    )
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.text == FORM_COMMENT['text']
    assert updated_comment.news == news
    assert updated_comment.author == author


def test_author_can_delete_comment(author_client, comment_delete_url):
    author_client.delete(comment_delete_url)
    assert Comment.objects.count() == 0


def test_user_cant_edit_comment_of_another_user(
    not_author_client, comment, comment_edit_url
):
    original_news = comment.news
    assert (
        not_author_client.post(comment_edit_url, data=FORM_COMMENT)
        .status_code == HTTPStatus.NOT_FOUND
    )
    assert comment.text != FORM_COMMENT['text']
    assert comment.author != not_author_client
    assert comment.news == original_news


def test_user_cant_delete_comment_of_another_user(
    not_author_client, comment, comment_delete_url
):
    comment_pk = comment.pk
    assert (
        not_author_client.delete(comment_delete_url)
        .status_code == HTTPStatus.NOT_FOUND
    )
    assert Comment.objects.filter(
        pk=comment_pk,
        text=comment.text,
        author=comment.author,
        news=comment.news
    ).exists()
    assert Comment.objects.count() == 1
