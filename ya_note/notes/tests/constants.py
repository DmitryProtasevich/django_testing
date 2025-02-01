from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


def get_redirect_url(next_url):
    return f"{reverse('users:login')}?next={next_url}"


def notes_detail_url(slug):
    return reverse('notes:detail', args=[slug])


def notes_edit_url(slug):
    return reverse('notes:edit', args=[slug])


def notes_delete_url(slug):
    return reverse('notes:delete', args=[slug])


class BaseTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.other_author = User.objects.create(username='Второй автор')
        cls.note = Note.objects.create(
            title='Название',
            text='Текст',
            author=cls.author
        )
        cls.note_form_data = {
            'title': 'Новая заметка',
            'text': 'Текст формы',
            'slug': 'slug'
        }
        cls.author_client = Client()
        cls.other_author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.other_author_client.force_login(cls.other_author)

        cls.NOTES_DETAIL_URL = notes_detail_url(cls.note.slug)
        cls.NOTES_DELETE_URL = notes_delete_url(cls.note.slug)
        cls.NOTES_EDIT_URL = notes_edit_url(cls.note.slug)
        cls.NOTES_ADD_URL = reverse('notes:add')
        cls.NOTES_LIST_URL = reverse('notes:list')
        cls.NOTES_HOME_URL = reverse('notes:home')
        cls.NOTES_SUCCESS_URL = reverse('notes:success')
        cls.USERS_LOGIN_URL = reverse('users:login')
        cls.USERS_LOGOUT_URL = reverse('users:logout')
        cls.USERS_SIGNUP_URL = reverse('users:signup')
