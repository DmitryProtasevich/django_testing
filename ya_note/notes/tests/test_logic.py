from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class TestLogic(TestCase):
    TEXT = 'Текст'
    NEW_TEXT = 'Новый текст'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.other_author = User.objects.create(username='Автор 2')
        cls.note_form_data_without_slug = {
            'title': 'Новая заметка',
            'text': cls.TEXT,
        }
        cls.note_new_form_data = {
            'title': 'Новая заметка',
            'text': cls.NEW_TEXT,
        }

    def test_note_creation_access(self):
        self.client.force_login(self.author)
        self.client.post(
            reverse('notes:add'), data=self.note_form_data_without_slug
        )
        self.assertEqual(Note.objects.count(), 1)
        self.client.logout()
        self.client.post(
            reverse('notes:add'), data=self.note_form_data_without_slug
        )
        self.assertEqual(Note.objects.count(), 1)

    def test_cannot_create_duplicate_slug_note(self):
        self.client.force_login(self.author)
        self.client.post(reverse('notes:add'),
                         data=self.note_form_data_without_slug)
        self.assertEqual(
            self.client.post(reverse('notes:add'), data={
                'title': 'Новая заметка',
                'text': 'Новая заметка',
                'slug': Note.objects.first().slug,
            }
            ).status_code, 200
        )
        self.assertEqual(Note.objects.count(), 1)

    def test_auto_creates_slug_if_empty(self):
        self.client.force_login(self.author)
        self.client.post(reverse('notes:add'),
                         data=self.note_form_data_without_slug)
        self.assertTrue(Note.objects.first().slug)

    def test_user_can_edit_and_delete_own_notes_and_other_user_cant(self):
        self.client.force_login(self.author)
        self.client.post(reverse('notes:add'),
                         data=self.note_form_data_without_slug)
        created_note = Note.objects.first()
        self.client.post(
            reverse('notes:edit', args=[created_note.slug]),
            self.note_new_form_data
        )
        created_note.refresh_from_db()
        self.assertEqual(created_note.text, self.NEW_TEXT)
        self.client.post(reverse('notes:delete', args=[created_note.slug]))
        self.assertEqual(Note.objects.count(), 0)
        self.client.post(reverse('notes:add'),
                         data=self.note_form_data_without_slug)
        created_note = Note.objects.first()
        self.client.force_login(self.other_author)
        created_note.refresh_from_db()
        self.assertNotEqual(
            self.client.post(reverse('notes:edit', args=[created_note.slug]),
                             self.note_new_form_data).status_code, 200
        )
        self.assertEqual(created_note.text, self.TEXT)
        self.assertNotEqual(
            self.client.post(reverse('notes:delete', args=[created_note.slug]))
            .status_code, 200
        )
        self.assertEqual(Note.objects.count(), 1)
