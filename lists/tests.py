from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

import re

from lists.views import home_page


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        response = home_page(request)
        response_html = response.content.decode()
        match = re.search(
            "((.|\n)*)<input type='hidden[^\/]*\/>((.|\n)*)",
            response_html
        )
        matched_groups = match.groups()
        response_html = str(matched_groups[0]) + str(matched_groups[2])

        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'A new list item'}
        )

        self.assertEqual(response_html, expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertIn('A new list item', response.content.decode())
