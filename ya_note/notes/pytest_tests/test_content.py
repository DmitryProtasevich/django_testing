
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestContent(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.other_author = User.objects.create(username='Второй автор')
        cls.note = Note.objects.create(
            text='Текст',
            author=cls.author
        )
        cls.other_note = Note.objects.create(
            title='Второе название',
            text='Второй Текст',
            author=cls.other_author
        )

    def test_single_note_displayed_in_notes_list(self):
        self.client.force_login(self.author)
        self.assertIn(
            self.note,
            self.client.get(reverse('notes:list'))
            .context['object_list']
        )

    def test_notes_are_not_shared_between_users(self):
        self.client.force_login(self.author)
        self.assertNotIn(
            self.other_note,
            self.client.get(reverse('notes:list'))
            .context['object_list']
        )

    def test_add_and_edit_pages_have_forms(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        )
        for name, args in urls:
            with self.subTest(name=name):
                self.client.force_login(self.author)
                self.assertIsInstance(
                    self.client.get(reverse(name, args=args))
                    .context['form'], NoteForm
                )
