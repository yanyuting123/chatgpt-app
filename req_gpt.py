import openai
import os

debug = False

def ask_gpt(prompt):
    res = openai.ChatCompletion.create(
        model= "gpt-3.5-turbo",
        messages= [{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.3
    )
    content = res['choices'][0]['message']['content']
    total_tokens = res['usage']['total_tokens']
    print(f'total_tokens: {total_tokens}')
    if debug:
        print(res)
    return content

def word_info(word):
    prompt = f'''give an overall explanation of meanings of '{word}', with 3 example sentences, output like following, NO other outputs.
Meaning Overall: xxx
Example1: xxx
Example2: xxx'''
    content = ask_gpt(prompt)
    meaning, examples = content.split('Example', maxsplit=1)
    examples = (examples + 'Example').split('\n')
    return meaning, examples


def choice_ques(word):
    prompt = f"ask a four-choice question on usage of the word '{word}' with only one correct choice, and provide the answer and explanation. The key is to make sure student understand the usage of the word instead of the grammar."
    content = ask_gpt(prompt)
    ques, ans = content.split('\n\nAnswer')
    ans = 'Answer' + ans
    return ques, ans

def article(words):
    prompt = f'''generate an article no more than 400 words using the words below. Use **word** to highlight the words. DONT use the words as a name:
    {' '.join(words)}
    '''
    content = ask_gpt(prompt)
    return content

def check_sentence(s):
    prompt = f'''You are a strict teacher. Are the sentences below conforming to the native speakers' habits and consistent with the context? If yes, reply OK. Otherwise EXPLAIN the REASON why it's incorrect. Sentences:
    {s}'''
    content = ask_gpt(prompt)
    return content

if __name__ == '__main__':
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if "http_proxy" not in os.environ and "https_proxy" not in os.environ:
        os.environ["http_proxy"] = "http://127.0.0.1:7890"
        os.environ["https_proxy"] = "http://127.0.0.1:7890"
    print(word_info('consort'))
    print(choice_ques('consort'))
    print(article(['abandon', 'comment', 'sentence', 'explanation', 'authentic', 'overwhelming']))
    print(check_sentence('I have an apple, I have a pen, errr, apple pen'))
