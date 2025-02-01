from http import HTTPStatus

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

FORM_COMMENT = {'text': 'Текст комментария'}
BAD_WORDS_FORM_COMMENT = {'text': f'Текст{BAD_WORDS}, комментария'}
FORM_UPDATE_COMMENT = {'text': 'Обновленный комментарий'}


def test_anonymous_user_cant_create_comment(client, news_urls):
    assert Comment.objects.count() == 0
    client.post(news_urls['detail'], data=FORM_COMMENT)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(author_client, author, news, news_urls):
    author_client.post(
        news_urls['detail'], data=FORM_COMMENT
    )
    assert Comment.objects.count() == 1
    assert Comment.objects.last().news == news
    assert Comment.objects.last().author == author
    assert Comment.objects.last().text == FORM_COMMENT['text']


def test_user_cant_use_bad_words(author_client, news_urls):
    assert WARNING in author_client.post(
        news_urls['detail'],
        data=BAD_WORDS_FORM_COMMENT
    ).context['form'].errors['text']
    assert Comment.objects.count() == 0


def test_author_can_update_comment(
    author_client, comment, comment_urls, news, author
):
    author_client.post(
        comment_urls['edit'], data=FORM_UPDATE_COMMENT
    )
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.text == FORM_UPDATE_COMMENT['text']
    assert updated_comment.news == news
    assert updated_comment.author == author


def test_author_can_delete_comment(author_client, comment_urls):
    assert Comment.objects.count() == 1
    author_client.delete(comment_urls['delete'])
    assert Comment.objects.count() == 0


def test_user_cant_edit_comment_of_another_user(
    not_author_client, comment, comment_urls
):
    old_text = comment.text
    assert (
        not_author_client.post(comment_urls['edit'], data=FORM_UPDATE_COMMENT)
        .status_code == HTTPStatus.NOT_FOUND
    )
    comment.refresh_from_db()
    assert comment.text == old_text


def test_user_cant_delete_comment_of_another_user(
    not_author_client, comment_urls
):
    assert (
        not_author_client.delete(comment_urls['delete'])
        .status_code == HTTPStatus.NOT_FOUND
    )


def test_user_cant_delete_comment_of_another_user(
    not_author_client, comment, comment_urls
):
    comment_pk = comment.pk
    assert (
        not_author_client.delete(comment_urls['delete'])
        .status_code == HTTPStatus.NOT_FOUND
    )
    assert Comment.objects.filter(pk=comment_pk).exists()
