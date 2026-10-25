import os
import tempfile
import unittest
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient
try:
    from .content import router, load_profile
except ImportError:
    from content import router, load_profile


class ContentTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.env = patch.dict(os.environ, {'CONTENT_DATA_DIR': self.directory.name, 'ADMIN_TOKEN': 'a' * 40})
        self.env.start()
        app = FastAPI()
        app.include_router(router)
        self.client = TestClient(app)
        self.headers = {'Authorization': 'Bearer ' + 'a' * 40}

    def tearDown(self):
        self.client.close()
        self.env.stop()
        self.directory.cleanup()

    def test_authentication_required_for_all_mutations(self):
        self.assertEqual(self.client.get('/admin/content').status_code, 401)
        self.assertEqual(self.client.put('/admin/experience', json={'experience': []}).status_code, 401)
        self.assertEqual(self.client.post('/admin/cv', files={'file': ('cv.pdf', b'%PDF-1.4\n%%EOF')}).status_code, 401)
        with patch.dict(os.environ, {'ADMIN_TOKEN': ''}):
            self.assertEqual(self.client.get('/admin/content', headers=self.headers).status_code, 503)

    def test_experience_is_shared_and_persistent(self):
        entries = [{'company': 'Firma', 'role': 'Ingeniør', 'period': '2026 – nå', 'country': 'Norge', 'tasks': ['PLS']}]
        self.assertEqual(self.client.put('/admin/experience', headers=self.headers, json={'experience': entries}).status_code, 200)
        self.assertEqual(self.client.get('/content').json()['experience'], entries)
        self.assertEqual(load_profile()['work_experience'], entries)
        self.assertEqual(self.client.put('/admin/experience', headers=self.headers, json={'experience': [{'company': ''}]}).status_code, 422)
        self.assertEqual(load_profile()['work_experience'], entries)
        self.client.put('/admin/experience', headers=self.headers, json={'experience': []})
        self.assertEqual(load_profile()['work_experience'], [])

    def test_pdf_upload_download_and_rejected_replacement(self):
        self.assertEqual(self.client.get('/cv').status_code, 404)
        pdf = b'%PDF-1.4\nexample\n%%EOF'
        self.assertEqual(self.client.post('/admin/cv', headers=self.headers, files={'file': ('cv.pdf', pdf)}).status_code, 200)
        self.assertEqual(self.client.get('/cv').content, pdf)
        self.assertIsNotNone(self.client.get('/content').json()['cv'])
        for name, data, status in [('bad.pdf', b'not pdf', 422), ('cv.pdf', b'x' * (10 * 1024 * 1024 + 1), 413)]:
            self.assertEqual(self.client.post('/admin/cv', headers=self.headers, files={'file': (name, data)}).status_code, status)
            self.assertEqual(self.client.get('/cv').content, pdf)


if __name__ == '__main__':
    unittest.main()
