from django.test import TestCase

# Create your tests here.
from django.core.urlresolvers import resolve
from .views import indexview
from django.http import HttpRequest
from django.template.loader import render_to_string


class IndexPageTest(TestCase):

    def test_root_url_to_index_view(self):
        found = resolve('/')
        self.assertEqual(found.func, indexview)

    # def test_index_view_return_corrent_html(self):
    #     request = HttpRequest()
    #     response = indexview(request)
    #     expected_html = render_to_string('index.html')
    #     self.assertEqual(response.content.decode(), expected_html)
