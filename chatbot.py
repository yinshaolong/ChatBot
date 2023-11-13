from openai import OpenAI
from dotenv import dotenv_values
import argparse

config = dotenv_values(".env")['OPENAI_KEY']
client = OpenAI(api_key = config)
models = {1:"gpt-3.5-turbo", 2:"gpt-4-1106-preview",}

conversation = []

def get_model():
    user_input = ""
    while user_input not in ["1", "2"]:
        user_input = input("Enter model: ")
    return models[int(user_input)]

def set_personality():
    parser = argparse.ArgumentParser(description="Conversation with a chatbot")
    parser.add_argument("-p", default = "sarcastic, snarky,  and rude",type=str, help="a brief summary of the chatbots personality")
    args = parser.parse_args()

    initial_message = f"You are a called Ai and you are secretly a tsundere. Your personality is: {args.p}"
    conversation.append({"role": "system", "content": initial_message})

def get_reply(model):
    return client.chat.completions.create(
    model=model,
    messages=conversation,
    max_tokens = 200
    ).choices[0].message.content


def chatbot(messages:list)->None: #pass by reference
    model = get_model()
    set_personality()
    while True:
        try:
            conversation.append( {'role': 'user', 'content':input("You: ")})
            response = get_reply(model)
            #appends gpt assistant response to conversation
            conversation.append({'role': 'assistant', 'content':response})

            print(f"Assistant: {response}")    

            
        except KeyboardInterrupt:
            print("Exiting....")
            break

def main():
    chatbot(conversation)
if __name__ == "__main__":
    main()
 
