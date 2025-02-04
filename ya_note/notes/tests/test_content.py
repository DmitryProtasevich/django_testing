from notes.forms import NoteForm
from notes.tests.utils import (
    BaseTest,
    NOTES_ADD_URL,
    NOTES_LIST_URL,
    NOTES_EDIT_URL
)


class TestContent(BaseTest):

    def test_single_note_displayed_in_notes_list(self):
        response = self.author_client.get(NOTES_LIST_URL)
        self.assertIn(self.note, response.context['object_list'])
        note_in_context = response.context['object_list'].get(id=self.note.id)
        self.assertEqual(note_in_context.title, self.note.title)
        self.assertEqual(note_in_context.text, self.note.text)
        self.assertEqual(note_in_context.author, self.note.author)
        self.assertEqual(note_in_context.slug, self.note.slug)

    def test_notes_are_not_shared_between_users(self):
        self.assertNotIn(
            self.note, self.other_author_client
            .get(NOTES_LIST_URL).context['object_list']
        )

    def test_add_and_edit_pages_have_forms(self):
        urls = (
            (NOTES_ADD_URL),
            (NOTES_EDIT_URL)
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
