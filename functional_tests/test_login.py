import os
import imaplib
import re
import time
import email
from django.core import mail
from .base import FunctionalTest


SUBJECT = 'Your login link for SuperLists'


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # Edith goes to the awesome superlists site
        # and notices a "Log in" section in the navbar for the first time
        # It's telling her to enter her email address, so she does
        if self.against_staging:
            test_email = 'nurek95@gmail.com'
        else:
            test_email = 'example@example.com'

        self.browser.get(self.server_url)
        self.browser.find_element_by_name('email').send_keys(
            test_email + '\n'
        )

        # A message appears telling her an email has been sent
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Check your email', body.text)

        # She checks her email and finds a message
        body = self.wait_for_email(test_email, SUBJECT)

        # It has a url link in it
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(
                'Could not find url in email body:\n{}'.format(email.body)
            )
        url = url_search.group(0)
        self.assertIn(self.server_url, url)

        # She clicks it
        self.browser.get(url)

        # She is logged in
        self.assert_logged_in(email=test_email)

        # Now she logs out
        self.browser.find_element_by_link_text('Log out').click()

        # She is logged out
        self.assert_logged_out(email=test_email)

    def wait_for_email(self, test_email, subject):
        if not self.against_staging:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, SUBJECT)
            return email.body
        else:
            email_to_delete = None
            start = time.time()
            inbox = imaplib.IMAP4_SSL("imap.gmail.com", 993)
            try:
                inbox.login(test_email, os.environ['EMAIL_PASSWORD'])
                while time.time() - start < 60:
                    for box_name in ['"[Gmail]/Spam"', '"INBOX"']:
                        inbox.select(box_name)
                        result, data = inbox.search(None, 'ALL')
                        latest_email_ids = data[0].split()[-5:]

                        for email_id in latest_email_ids:
                            print('getting messages', email_id.decode())
                            result, raw_email_data = inbox.fetch(
                                email_id,
                                "(RFC822)"
                            )
                            raw_email = raw_email_data[0][1]
                            raw_email = raw_email.decode(
                                encoding='utf8',
                                errors='ignore'
                            )
                            email_message = email.message_from_string(
                                raw_email
                            )
                            email_subject = email_message['Subject']
                            print(email_subject)
                            if subject in email_subject:
                                email_to_delete = email_id
                                body = email_message.get_payload()
                                return body

                    time.sleep(5)
            finally:
                if email_to_delete:
                    inbox.store(email_to_delete, '+FLAGS', '\\Deleted')
                    inbox.expunge()
                try:
                    inbox.close()
                except:
                    pass
                inbox.logout()
