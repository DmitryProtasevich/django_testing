from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()

NOTES_ADD_URL = reverse('notes:add')
NOTES_LIST_URL = reverse('notes:list')
NOTES_HOME_URL = reverse('notes:home')
NOTES_SUCCESS_URL = reverse('notes:success')
USERS_LOGIN_URL = reverse('users:login')
USERS_LOGOUT_URL = reverse('users:logout')
USERS_SIGNUP_URL = reverse('users:signup')
NOTES_EDIT_URL = reverse('notes:edit', args=['slug_of_note'])
NOTES_DELETE_URL = reverse('notes:delete', args=['slug_of_note'])
NOTES_DETAIL_URL = reverse('notes:detail', args=['slug_of_note'])
REDIRECT_LIST_URL = USERS_LOGIN_URL + '?next=' + NOTES_LIST_URL
REDIRECT_ADD_URL = USERS_LOGIN_URL + '?next=' + NOTES_ADD_URL
REDIRECT_DETAIL_URL = USERS_LOGIN_URL + '?next=' + NOTES_DETAIL_URL
REDIRECT_DELETE_URL = USERS_LOGIN_URL + '?next=' + NOTES_DELETE_URL
REDIRECT_EDIT_URL = USERS_LOGIN_URL + '?next=' + NOTES_EDIT_URL


class BaseTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.other_author = User.objects.create(username='Второй автор')
        cls.note = Note.objects.create(
            title='Название',
            text='Текст',
            slug='slug_of_note',
            author=cls.author,
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
