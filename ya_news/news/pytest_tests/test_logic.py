
from http import HTTPStatus

import pytest
from django.urls import reverse
from news.forms import WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news, form_comment):
    client.post(reverse('news:detail', args=(news.pk,)), data=form_comment)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(author_client, news, form_comment):
    author_client.post(
        reverse('news:detail', args=(news.pk,)), data=form_comment
    )
    assert Comment.objects.count() == 1


def test_user_cant_use_bad_words(author_client, news, bad_words_form_comment):
    assert WARNING in author_client.post(
        reverse('news:detail', args=(news.pk,)),
        data=bad_words_form_comment
    ).context['form'].errors['text']
    assert Comment.objects.count() == 0


def test_author_can_update_and_delete_comment(
    author_client, comment, form_update_comment
):
    assert comment.text == 'Текст комментария'
    author_client.post(
        reverse('news:edit', args=(comment.pk,)), data=form_update_comment
    )
    assert (
        Comment.objects.get(pk=comment.pk).text == form_update_comment['text']
    )
    author_client.delete(reverse('news:delete', args=(comment.pk,)))
    assert Comment.objects.count() == 0


def test_user_cant_edit_comment_of_another_user(
    not_author_client, comment, form_update_comment
):
    response = not_author_client.post(
        reverse('news:edit', args=(comment.pk,)), data=form_update_comment
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    not_author_client.delete(reverse('news:delete', args=(comment.pk,)))
    assert response.status_code == HTTPStatus.NOT_FOUND
