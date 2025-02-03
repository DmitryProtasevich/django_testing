from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.utils_for_tests import (
    BaseTest,
    NOTES_EDIT_URL,
    NOTES_DELETE_URL,
    NOTES_ADD_URL,
)


class TestLogic(BaseTest):

    def test_note_creation_for_author(self):
        self.author_client.post(
            NOTES_ADD_URL, data=self.note_form_data
        )
        notes = Note.objects.filter(
            title=self.note_form_data['title'],
            author=self.author
        )
        self.assertEqual(notes.count(), 1)
        created_note = notes.get()
        self.assertIsNotNone(created_note)
        self.assertEqual(created_note.slug, self.note_form_data['slug'])
        self.assertEqual(created_note.title, self.note_form_data['title'])
        self.assertEqual(created_note.text, self.note_form_data['text'])
        self.assertEqual(created_note.author, self.author)

    def test_note_creation_for_client(self):
        self.assertEqual(self.client.post(
            NOTES_ADD_URL, data=self.note_form_data
        ).status_code, 302)
        self.assertFalse(Note.objects.filter(
            title=self.note_form_data['title'],
            text=self.note_form_data['text'],
            slug=self.note_form_data['slug']
        ).exists())

    def test_cannot_create_duplicate_slug_note(self):
        self.note_form_data['slug'] = self.note.slug
        self.assertFormError(
            self.author_client.post(
                NOTES_ADD_URL, data=self.note_form_data
            ),
            'form',
            'slug',
            errors=self.note.slug + WARNING
        )

    def test_auto_creates_slug_if_empty(self):
        self.note_form_data.pop('slug')
        self.author_client.post(
            NOTES_ADD_URL, data=self.note_form_data
        )
        notes = Note.objects.filter(
            title=self.note_form_data['title'], author=self.author
        )
        self.assertEqual(notes.count(), 1)
        note = notes.get()
        self.assertEqual(note.title, self.note_form_data['title'])
        self.assertEqual(note.text, self.note_form_data['text'])
        self.assertEqual(note.slug, slugify(self.note_form_data['title']))
        self.assertEqual(note.author, self.author)

    def test_user_can_edit_own_notes(self):
        self.author_client.post(NOTES_EDIT_URL, data=self.note_form_data)
        updated_note = Note.objects.get(id=self.note.id)
        self.assertIsNotNone(updated_note)
        self.assertEqual(updated_note.slug, self.note_form_data['slug'])
        self.assertEqual(updated_note.title, self.note_form_data['title'])
        self.assertEqual(updated_note.text, self.note_form_data['text'])
        self.assertEqual(updated_note.author, self.author)

    def test_user_can_delete_own_notes(self):
        self.author_client.post(
            NOTES_DELETE_URL, data=self.note_form_data
        )
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_other_user_cant_edit_notes(self):
        self.other_author_client.post(NOTES_EDIT_URL, data=self.note_form_data)
        updated_note = Note.objects.get(id=self.note.id)
        self.assertEqual(updated_note.title, self.note.title)
        self.assertEqual(updated_note.text, self.note.text)
        self.assertEqual(updated_note.slug, self.note.slug)
        self.assertEqual(updated_note.author, self.note.author)

    def test_other_user_cant_delete_notes(self):
        self.assertEqual(self.other_author_client.post(
            NOTES_DELETE_URL, data=self.note_form_data
        ).status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(Note.objects.filter(
            id=self.note.id,
            title=self.note.title,
            text=self.note.text,
            slug=self.note.slug,
            author=self.note.author
        ).exists())
