from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def transcriber_func(path: str):
    with open(path, 'rb') as audio_file:
        transcription = client.audio.transcriptions.create(
            model='gpt-4o-mini-transcribe',
            file=audio_file,
            prompt=(
                "The speaker is addressing Jarvis, a polite personal AI assistant. "
                "The user may give commands related to opening applications, "
                "starting work, or asking questions. "
                "The assistant's name is Jarvis."
            ),
            # extra_body={
            #     'keywords': ['jarvis'],
            #     'languages': ['en']
            # }
        )

    return transcription.text

    