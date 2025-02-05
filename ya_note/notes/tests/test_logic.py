from http import HTTPStatus

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
        notes = set(Note.objects.all())
        self.author_client.post(
            NOTES_ADD_URL, data=self.form_data
        )
        notes = set(Note.objects.all()) - notes
        self.assertEqual(len(notes), 1)
        note = notes.pop()
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, self.author)

    def test_anonymous_user_cannot_create_note(self):
        notes = set(Note.objects.all())
        self.assertEqual(self.client.post(
            NOTES_ADD_URL, data=self.form_data
        ).status_code, HTTPStatus.FOUND)
        self.assertEqual(set(Note.objects.all()), notes)

    def test_cannot_create_duplicate_slug_note(self):
        self.form_data['slug'] = self.note.slug
        notes = set(Note.objects.all())
        self.assertFormError(
            self.author_client.post(
                NOTES_ADD_URL, data=self.form_data
            ),
            'form',
            'slug',
            errors=self.note.slug + WARNING
        )
        self.assertEqual(set(Note.objects.all()), notes)

    def test_auto_creates_slug_if_empty(self):
        self.form_data.pop('slug')
        notes = set(Note.objects.all())
        self.author_client.post(
            NOTES_ADD_URL, data=self.form_data
        )
        notes = set(Note.objects.all()) - notes
        self.assertEqual(len(notes), 1)
        note = notes.pop()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(
            note.slug, slugify(self.form_data['title'])
        )
        self.assertEqual(note.author, self.author)

    def test_user_can_edit_own_notes(self):
        self.author_client.post(NOTES_EDIT_URL, data=self.form_data)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, self.note.author)

    def test_user_can_delete_own_notes(self):
        notes = set(Note.objects.all())
        self.author_client.post(
            NOTES_DELETE_URL, data=self.form_data
        )
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())
        self.assertEqual(len(notes - set(Note.objects.all())), 1)

    def test_other_user_cant_edit_notes(self):
        self.other_author_client.post(NOTES_EDIT_URL, data=self.form_data)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_other_user_cant_delete_notes(self):
        self.assertEqual(self.other_author_client.post(
            NOTES_DELETE_URL, data=self.form_data
        ).status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(Note.objects.filter(id=self.note.id).exists())
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)
