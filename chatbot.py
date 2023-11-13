from openai import OpenAI
from dotenv import dotenv_values
import argparse

config = dotenv_values(".env")['OPENAI_KEY']
client = OpenAI(api_key = config)

conversation = []
models = {3:"gpt-3.5-turbo", 4:"gpt-4-1106-preview",}

def bold(text):
    bold_start = "\033[1m"
    bold_end = "\033[0;0m"
    return bold_start + text + bold_end

def blue(text):
    blue_start = "\033[34m"
    blue_end = "\033[0;0m"
    return blue_start + text + blue_end

def red(text):
    red_start = "\033[31m"
    red_end = "\033[0;0m"
    return red_start + text + red_end

def check_valid_model(model):
    while model not in ["3", "4"]:
        model = input("Invalid entry. Enter gpt model: ")
    return models[int(model)]

def parse_args():
    parser = argparse.ArgumentParser(description="Conversation with a chatbot")
    parser.add_argument("-p", default = "sarcastic and rude but still helpful",type=str, help="a brief summary of the chatbots personality")
    parser.add_argument("-m", default = '4',type=str, help="a brief summary of the chatbots personality")
    return parser.parse_args()
    
def set_personality(initial_message = f"You are called Ai. You are an extreme tsundere to the user. Every sentence ends with emoticons that show your emotional state (e.g.(´-ω-`)). Your personality is: "):
    args = parse_args()
    initial_message.join([args.p])
    conversation.append({"role": "system", "content": initial_message})

def set_model():
    model = parse_args().m #model
    model = check_valid_model(model)
    return model


def get_reply(model):
    for data in client.chat.completions.create(
    model=model,
    messages=conversation,
    max_tokens = 200,
    stream=True,
    ):          
        content = data.choices[0].delta.content
        if content is not None:
            yield content


def chatbot(messages:list)->None: #pass by reference
    model = set_model()
    set_personality()
    while True:
        try:
            conversation.append( {'role': 'user', 'content':input(bold(blue("You: ")))})
            response = []
            print(f"{bold(red('Assistant Ai: '))} ", end = "")
            for message in get_reply(model):
                print(message, end='', flush=True)
                response.append(message)
            print('')
            response = "".join(response)
            conversation.append({'role': 'assistant', 'content':response})


            
        except KeyboardInterrupt:
            print("Exiting....")
            break

def main():
    chatbot(conversation)
if __name__ == "__main__":
    main()