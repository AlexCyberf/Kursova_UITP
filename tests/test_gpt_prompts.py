import unittest
import re
from gpt_prompts import get_answer_from_gpt


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
