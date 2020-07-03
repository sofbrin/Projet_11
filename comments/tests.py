from django.test import TestCase
from django.urls import reverse


class CommentsTest(TestCase):
    fixtures = ['test_data']

    def test_entry_archive_index(self):
        pass