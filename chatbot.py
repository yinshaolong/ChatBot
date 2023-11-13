from openai import OpenAI
from dotenv import dotenv_values

config = dotenv_values(".env")['OPENAI_KEY']
client = OpenAI(api_key = config)
models = {1:"gpt-3.5-turbo", 2:"gpt-4-1106-preview",}

conversation = []

def get_reply(model):
    return client.chat.completions.create(
    model=model,
    messages=conversation,
    max_tokens = 20
    ).choices[0].message.content

def chatbot(messages:list)->None:
    while True:
        try:
            conversation.append( {'role': 'user', 'content':input("Enter your message: ")})
            response = get_reply(models[1])
            #appends gpt assistant response to conversation
            conversation.append({'role': 'assistant', 'content':response})

            print(conversation)
            print("response", response)    
            print(response)    

            
        except KeyboardInterrupt:
            print("Exiting....")
            break

chatbot(conversation)


# conversation.append( {'role': 'user', 'content':input("Enter your message: ")})
# #__dict__ allows for dict conversion
#     #cant use to_dict()
# print(get_reply(models[1]).choices[0].message.__dict__)