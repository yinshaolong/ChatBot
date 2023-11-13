from openai import OpenAI
from dotenv import dotenv_values
from prompt import prompt as messages

config = dotenv_values(".env")['OPENAI_KEY']

client = OpenAI(api_key = config)

models = {1:"gpt-3.5-turbo", 2:"gpt-4-1106-preview",}

def get_reply(model):
    return client.chat.completions.create(
    model=model,
    messages = messages,
    max_tokens = 20
    ).choices[0].message.content

print(get_reply(models[1]))
