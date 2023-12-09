import openai
import re
api_key = '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'


def get_answer_from_gpt(style, text):
    prompt_1 = f'Напиши текст в жанрі {style} на тему {text}. Максимум 300 слів'
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompt_1}
    ],
    api_key=api_key,
    temperature = 0.7
    )

    answer = response['choices'][0]['message']['content']
    return answer
