import unittest

from pepper.markdown.classes import MarkdownFile


class MarkdownFileMetaTestCase(unittest.TestCase):
    def setUp(self):
        self.file = MarkdownFile("tests/fixtures/test.md")

    def test_meta_instanstiates_correctly(self):
        self.assertEqual(self.file.meta.title, "Dog")
        self.assertEqual(self.file.meta.bark, "Woof")
