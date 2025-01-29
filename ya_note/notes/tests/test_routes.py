
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from notes.models import Note
from yanote.settings import LOGIN_URL

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.reader = User.objects.create(username='Читатель простой')
        cls.author = User.objects.create(username='Автор')
        cls.note = Note.objects.create(
            title='Заголовок', text='Текст', author=cls.author
        )

    def test_home_page(self):
        self.assertEqual(
            self.client.get(reverse('notes:home'))
            .status_code, HTTPStatus.OK
        )

    def test_pages_availability(self):
        urls = (
            ('notes:add', None),
            ('notes:list', None),
            ('notes:success', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                self.client.force_login(self.reader)
                self.assertEqual(
                    self.client.get(reverse(name, args=args))
                    .status_code, HTTPStatus.OK
                )

    def test_pages_availability_for_author_and_reader(self):
        urls = (
            ('notes:detail', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
        )
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for name, args in urls:
            for user, expected_status in users_statuses:
                with self.subTest(name=name, user=user.username):
                    self.client.force_login(user)
                    self.assertEqual(
                        self.client.get(reverse(name, args=args))
                        .status_code, expected_status
                    )

    def test_redirect_anonymous_users_to_login(self):
        urls = (
            ('notes:list', None),
            ('notes:add', None),
            ('notes:detail', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:edit', (self.note.slug,))
        )
        for name, args in urls:
            with self.subTest(name=name):
                self.assertRedirects(
                    self.client.get(reverse(name, args=args)),
                    f'{LOGIN_URL}?next={reverse(name, args=args)}'
                )

    def test_registration_page_accessible_to_all_users(self):
        urls = (
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.OK),
            (self.client, HTTPStatus.OK),
        )
        for name, args in urls:
            for user, expected_status in users_statuses:
                if user != self.client:
                    self.client.force_login(user)
                with self.subTest(
                    name=name, user=user.username
                    if user != self.client else 'Anonymous'
                ):
                    self.assertEqual(
                        self.client.get(reverse(name, args=args))
                        .status_code, expected_status
                    )
