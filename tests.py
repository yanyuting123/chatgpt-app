import unittest, os, json
import openai
from myapp import app

class TestMyApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        openai.api_key = os.getenv("OPENAI_API_KEY")

        if "http_proxy" not in os.environ and "https_proxy" not in os.environ:
            os.environ["http_proxy"] = "http://127.0.0.1:7890"
            os.environ["https_proxy"] = "http://127.0.0.1:7890"

    def test_get_sources(self):
        response = self.client.post('/data/get_sources')
        self.assertEqual(response.status_code, 200)
        print(response.data)

    def test_get_source_data(self):
        response = self.client.post('/data/get_source_data', json={'id': 1, 'name': 'test'})
        self.assertEqual(response.status_code, 200)
        print(response.data)

    def test_get_new_words(self):
        response = self.client.post('/data/get_new_words', json={'id': 2, 'name': 'TOEFL', 'number': 10})
        self.assertEqual(response.status_code, 200)
        print(response.data)

    def test_get_word_info(self):
        response = self.client.post('/data/get_word_info', data='test')
        self.assertEqual(response.status_code, 200)
        print(response.data)

    def test_get_choice_question(self):
        response = self.client.post('/data/get_choice_question', data='test')
        self.assertEqual(response.status_code, 200)
        print(response.data)

    def test_get_article(self):
        response = self.client.post('/data/get_article')
        self.assertEqual(response.status_code, 200)
        print(response.data)

    def test_check_sentence(self):
        response = self.client.post('/data/check_answer', data='test')
        self.assertEqual(response.status_code, 200)
        print(response.data)


if __name__ == '__main__':

    unittest.main()
