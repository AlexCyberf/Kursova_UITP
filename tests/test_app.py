import unittest
from app import app, db
import re
from gpt_prompts import get_answer_from_gpt


class AppTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_main_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)

    def test_login_page(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_unsuccessful_login(self):
        response = self.app.post('/login', data={'username': 'nonexistent_user', 'password': 'wrong_password'})
        self.assertIn(b'Login or password is incorrect', response.data)

    def test_register_page(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_short_password_registration(self):
        response = self.app.post('/register', data={'username': 'user_with_short_password', 'password': 'short',
                                                    'confirmPassword': 'short'})
        self.assertIn(b'Password must be at least 6 characters long', response.data)

    def test_password_confirmation_mismatch(self):
        response = self.app.post('/register',
                                 data={'username': 'user_with_mismatched_passwords', 'password': 'password',
                                       'confirmPassword': 'mismatched_password'})
        self.assertIn(b'Passwords do not match', response.data)


class GPTTests(unittest.TestCase):

    def test_get_answer_success(self):
        style = 'новини'
        text = 'глобальне потепління'
        answer = get_answer_from_gpt(style, text)
        self.assertIsNotNone(answer)
        self.assertIsInstance(answer, str)

    def test_answer_word_limit(self):
        style = 'рецензія'
        text = 'фільм "Інтерстеллар"'
        answer = get_answer_from_gpt(style, text)
        word_count = len(re.findall(r'\b\w+\b', answer))
        self.assertLessEqual(word_count, 300)


if __name__ == '__main__':
    unittest.main()