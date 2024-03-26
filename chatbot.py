from openai import OpenAI
from dotenv import dotenv_values
import argparse
from pathlib import Path
from pygame import mixer #to autom
import time
from get_audio import record_audio
import uuid #used to bypass writitng to the same file

mixer.init()

RECORDING_LENGTH = 4

config = dotenv_values(".env")['OPENAI_KEY']
client = OpenAI(api_key = config)

conversation = []
models = {3:"gpt-3.5-turbo", 4:"gpt-4-1106-preview",}
available_languages = {
    "Afrikaans": "af-ZA",
    "Arabic": "ar-SA",
    "Armenian": "hy-AM",
    "Azerbaijani": "az-AZ",
    "Belarusian": "be-BY",
    "Bosnian": "bs-BA",
    "Bulgarian": "bg-BG",
    "Catalan": "ca-ES",
    "Chinese": "zh-CN",
    "Croatian": "hr-HR",
    "Czech": "cs-CZ",
    "Danish": "da-DK",
    "Dutch": "nl-NL",
    "English": "en-US",
    "Estonian": "et-EE",
    "Finnish": "fi-FI",
    "French": "fr-FR",
    "Galician": "gl-ES",
    "German": "de-DE",
    "Greek": "el-GR",
    "Hebrew": "he-IL",
    "Hindi": "hi-IN",
    "Hungarian": "hu-HU",
    "Icelandic": "is-IS",
    "Indonesian": "id-ID",
    "Italian": "it-IT",
    "Japanese": "ja-JP",
    "Kannada": "kn-IN",
    "Kazakh": "kk-KZ",
    "Korean": "ko-KR",
    "Latvian": "lv-LV",
    "Lithuanian": "lt-LT",
    "Macedonian": "mk-MK",
    "Malay": "ms-MY",
    "Marathi": "mr-IN",
    "Maori": "mi-NZ",
    "Nepali": "ne-NP",
    "Norwegian": "no-NO",
    "Persian": "fa-IR",
    "Polish": "pl-PL",
    "Portuguese": "pt-PT",
    "Romanian": "ro-RO",
    "Russian": "ru-RU",
    "Serbian": "sr-RS",
    "Slovak": "sk-SK",
    "Slovenian": "sl-SI",
    "Spanish": "es-ES",
    "Swahili": "sw-KE",
    "Swedish": "sv-SE",
    "Tagalog": "tl-PH",
    "Tamil": "ta-IN",
    "Thai": "th-TH",
    "Turkish": "tr-TR",
    "Ukrainian": "uk-UA",
    "Urdu": "ur-PK",
    "Vietnamese": "vi-VN",
    "Welsh": "cy-GB"
}



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
    parser.add_argument("-p", default = "extremely sarcastic and rude but still answers questions",type=str, help="a brief summary of the chatbots personality")
    parser.add_argument("-m", default = '4',type=str, help="a variable that determines the gpt model to use. 3 or 4. Default is 4.")
    # parser.add_argument("-l", default="en-US", type=str, help="language to use")
    return parser.parse_args()
    
def set_personality(initial_message = f"You are called Ai. End every sentence with emoticons that show your emotional state (e.g.(´-ω-`)). Your personality is "):
    args = parse_args()
    initial_message += args.p
    conversation.append({"role": "system", "content": initial_message})

def set_model():
    model = parse_args().m #model
    model = check_valid_model(model)
    return model

def get_language():
    language = parse_args().l
    while language.lower().capitalize() not in available_languages:
        language = input("Invalid entry. Enter a valid language: ")
    return language

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


def text_to_speech(ai_response:str)->None:
    # Generate a unique filename for each response
    speech_file_path = Path(__file__).parent / f"speech/speech_{uuid.uuid4()}.mp3"

    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input= ai_response,
    )

    # Save the speech to a file
    response.stream_to_file(speech_file_path)

    # Play the speech file
    mixer.music.load(str(speech_file_path))
    mixer.music.play()

    # Wait for the audio to finish playing
    while mixer.music.get_busy():
        time.sleep(1)


def speech_to_text(filename="output.wav")->str:
    audio_file = open("speech/output.wav", "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    return transcription

def chatbot(messages:list)->None: #pass by reference
    model = set_model()
    set_personality()
    while True:
        try:
            user_message = bold(blue("You: "))
            record_audio(RECORDING_LENGTH)
            recording = speech_to_text().text # object -> Transcription(text="User says stuff here")
            user_message += recording
            print(user_message)
            conversation.append( {'role': 'user', 'content':user_message})
            ai_response = []
            print(f"{bold(red('Assistant Ai: '))} ", end = "")
            for message in get_reply(model):
                print(message, end='', flush=True)
                ai_response.append(message)
            print('')
            ai_response = "".join(ai_response)
            text_to_speech(ai_response)
            conversation.append({'role': 'assistant', 'content':ai_response})

            
        except KeyboardInterrupt:
            print("Exiting....")
            break

def main():
    chatbot(conversation)
if __name__ == "__main__":
    main()