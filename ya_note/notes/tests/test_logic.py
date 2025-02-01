from pytils.translit import slugify

from notes.models import Note
from notes.tests.constants import BaseTest


class TestLogic(BaseTest):

    def add_post(self, author=None):
        if author is None:
            author = self.author_client
        return author.post(
            self.NOTES_ADD_URL, data=self.note_form_data
        )

    def edit_post(self, author=None):
        if author is None:
            author = self.author_client
        return author.post(
            self.NOTES_EDIT_URL, data=self.note_form_data
        )

    def delete_post(self, author=None):
        if author is None:
            author = self.author_client
        return author.post(
            self.NOTES_DELETE_URL, data=self.note_form_data
        )

    def assert_note_details(self, note):
        self.assertIsNotNone(note)
        self.assertEqual(note.slug, self.note_form_data['slug'])
        self.assertEqual(note.title, self.note_form_data['title'])
        self.assertEqual(note.text, self.note_form_data['text'])
        self.assertEqual(note.author, self.author)

    def test_note_creation_for_author(self):
        self.add_post()
        created_note = Note.objects.get(slug=self.note_form_data['slug'])
        self.assert_note_details(created_note)

    def test_note_creation_for_client(self):
        self.add_post(self.client)
        self.assertFalse(
            Note.objects.filter(slug=self.note_form_data['slug']).exists()
        )

    def test_cannot_create_duplicate_slug_note(self):
        slug = self.note_form_data['slug']
        self.add_post()
        slug_objects_count = Note.objects.filter(slug=slug).count()
        self.add_post()
        self.assertEqual(
            Note.objects.filter(slug=slug).count(), slug_objects_count
        )

    def test_auto_creates_slug_if_empty(self):
        self.note_form_data.pop('slug')
        self.add_post()
        self.assertEqual(
            Note.objects.get(
                title=self.note_form_data['title'], author=self.author
            ).slug, slugify(self.note_form_data['title'])
        )

    def test_user_can_edit_own_notes(self):
        note_id = self.note.id
        self.edit_post()
        updated_note = Note.objects.get(id=note_id)
        self.assert_note_details(updated_note)

    def test_user_can_delete_own_notes(self):
        note_id = self.note.id
        self.delete_post()
        self.assertFalse(Note.objects.filter(id=note_id).exists())

    def test_other_user_cant_edit_notes(self):
        note_id = self.note.id
        self.edit_post(self.other_author_client)
        updated_note = Note.objects.get(id=note_id)
        self.assertNotEqual(updated_note.title, self.note_form_data['title'])
        self.assertNotEqual(updated_note.text, self.note_form_data['text'])
        self.assertNotEqual(updated_note.slug, self.note_form_data['slug'])
        self.assertEqual(updated_note.author, self.author)

    def test_other_user_cant_delete_notes(self):
        note_id = self.note.id
        self.delete_post(self.other_author_client)
        self.assertIsNotNone(Note.objects.filter(id=note_id))
