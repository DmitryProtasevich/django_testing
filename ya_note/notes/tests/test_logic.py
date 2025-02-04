from http import HTTPStatus
from http.client import FOUND

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.utils import (
    BaseTest,
    NOTES_EDIT_URL,
    NOTES_DELETE_URL,
    NOTES_ADD_URL,
)


class TestLogic(BaseTest):

    def test_note_creation_for_author(self):
        original_notes = set(Note.objects.all())
        self.author_client.post(
            NOTES_ADD_URL, data=self.note_form_data
        )
        final_notes = set(Note.objects.all())
        created_notes = final_notes - original_notes
        self.assertEqual(len(created_notes), 1)
        created_note = created_notes.pop()
        self.assertEqual(created_note.slug, self.note_form_data['slug'])
        self.assertEqual(created_note.title, self.note_form_data['title'])
        self.assertEqual(created_note.text, self.note_form_data['text'])
        self.assertEqual(created_note.author, self.author)

    def test_anonymous_user_cannot_create_note(self):
        original_notes = set(Note.objects.all())
        self.assertEqual(self.client.post(
            NOTES_ADD_URL, data=self.note_form_data
        ).status_code, FOUND)
        final_notes = set(Note.objects.all())
        self.assertEqual(len(final_notes - original_notes), 0)

    def test_cannot_create_duplicate_slug_note(self):
        self.note_form_data['slug'] = self.note.slug
        original_notes = set(Note.objects.all())
        self.assertFormError(
            self.author_client.post(
                NOTES_ADD_URL, data=self.note_form_data
            ),
            'form',
            'slug',
            errors=self.note.slug + WARNING
        )
        final_notes = set(Note.objects.all())
        self.assertEqual(len(final_notes - original_notes), 0)

    def test_auto_creates_slug_if_empty(self):
        self.note_form_data.pop('slug')
        original_notes = set(Note.objects.all())
        self.author_client.post(
            NOTES_ADD_URL, data=self.note_form_data
        )
        final_notes = set(Note.objects.all())
        created_notes = final_notes - original_notes
        self.assertEqual(len(created_notes), 1)
        created_note = created_notes.pop()
        self.assertEqual(created_note.title, self.note_form_data['title'])
        self.assertEqual(created_note.text, self.note_form_data['text'])
        self.assertEqual(
            created_note.slug, slugify(self.note_form_data['title'])
        )
        self.assertEqual(created_note.author, self.author)

    def test_user_can_edit_own_notes(self):
        self.author_client.post(NOTES_EDIT_URL, data=self.note_form_data)
        updated_note = Note.objects.get(id=self.note.id)
        self.assertEqual(updated_note.slug, self.note_form_data['slug'])
        self.assertEqual(updated_note.title, self.note_form_data['title'])
        self.assertEqual(updated_note.text, self.note_form_data['text'])
        self.assertEqual(updated_note.author, self.note.author)

    def test_user_can_delete_own_notes(self):
        original_notes = set(Note.objects.all())
        self.author_client.post(
            NOTES_DELETE_URL, data=self.note_form_data
        )
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())
        final_notes = set(Note.objects.all())
        self.assertEqual(len(original_notes - final_notes), 1)

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
        existing_note = Note.objects.get(id=self.note.id)
        self.assertEqual(existing_note.title, self.note.title)
        self.assertEqual(existing_note.text, self.note.text)
        self.assertEqual(existing_note.slug, self.note.slug)
        self.assertEqual(existing_note.author, self.note.author)
