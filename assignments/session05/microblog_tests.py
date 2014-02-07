import os
import tempfile
import unittest
from flask import session

import microblog

class MicroblogTestCase(unittest.TestCase):

    def setUp(self):

        # divert the db to a temporary location
        db_fd = tempfile.mkstemp()
        self.db_fd, microblog.app.config['DATABASE'] = db_fd
        microblog.app.config['TESTING'] = True

        # create a client for running tests
        self.client = microblog.app.test_client()

        # add the app
        self.app =  microblog.app
        microblog.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(microblog.app.config['DATABASE'])


    def test_database_setup(self):
        con = microblog.connect_db()
        cur = con.execute('PRAGMA table_info(entries);')
        rows = cur.fetchall()
        self.assertEquals(len(rows), 3)

    def test_write_entry(self):
        expected = ("My Title", "My Text")
        with self.app.test_request_context('/'):
            microblog.write_entry(*expected)
            con = microblog.connect_db()
            cur = con.execute("select * from entries;")
            rows = cur.fetchall()
        self.assertEquals(len(rows), 1)
        for val in expected:
            self.assertTrue(val in rows[0])

    def test_get_all_entries_empty(self):
        with self.app.test_request_context('/'):
            entries = microblog.get_all_entries()
            self.assertEquals(len(entries), 0)

    def test_get_all_entries(self):
        expected = ("My Title", "My Text")
        with self.app.test_request_context('/'):
            microblog.write_entry(*expected)
            entries = microblog.get_all_entries()
            self.assertEquals(len(entries), 1)
            for entry in entries:
                self.assertEquals(expected[0], entry['title'])
                self.assertEquals(expected[1], entry['text'])

    def test_empty_listing(self):
        actual = self.client.get('/').data
        expected = 'No entries here so far'
        self.assertTrue(expected in actual)

    def test_listing(self):
        expected = ("My Title", "My Text")
        with self.app.test_request_context('/'):
            microblog.write_entry(*expected)
        actual = self.client.get('/').data
        for value in expected:
            self.assertTrue(value in actual)

    def test_add_entries(self):
        actual = self.client.post('/add', data=dict(
                     title='Hello',
                     text='This is a post'), follow_redirects=True).data
        self.assertFalse('No entries here so far' in actual)
        self.assertTrue('Hello' in actual)
        self.assertTrue('This is a post' in actual)


    def test_login_session_passes(self):
        with self.app.test_request_context('/'):
            microblog.login_session(microblog.app.config['USERNAME'],
                                    microblog.app.config['PASSWORD'])
            self.assertTrue(session['logged_in']) 

    def test_login_session_fails(self):
        with self.app.test_request_context('/'):
            self.assertRaises(ValueError, microblog.login_session,
                              'myname', microblog.app.config['PASSWORD'])

    def test_login_logout(self):
        ans1 = self.client.post('/login',
                                data=dict(username="admin", password="default"),
                                follow_redirects=True).data
        self.assertTrue("You are logged in" in ans1)

        answer = self.client.get('/logout', follow_redirects=True).data 
        self.assertTrue("You have logged out" in answer)

        ans2 = self.client.post('/login',
                               data=dict(username="root", password="default"),
                               follow_redirects=True).data
        self.assertTrue("Invalid username" in ans2)
        ans3 = self.client.post('/login',
                               data=dict(username="admin", password="fred"),
                               follow_redirects=True).data
        self.assertTrue("Invalid password" in ans3)

        


if  __name__ == '__main__':
    unittest.main()
