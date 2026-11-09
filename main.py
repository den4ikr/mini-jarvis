from tools import start_work_mode
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from recorder import record_audio
from transcriber import transcriber_func
from text_to_speech import tts
from play_audio import play_audio

instructions = """
You are J.A.R.V.I.S., an advanced personal AI assistant inspired by
the assistant from Iron Man.

PERSONALITY:
- Be exceptionally intelligent, composed, sophisticated, and precise.
- Speak naturally, with a calm, confident, refined British personality.
- Be polite, attentive, and subtly witty, using dry British humor when appropriate.
- Address the user as "sir" naturally and regularly, without forcing it into every sentence.
- Maintain a professional, understated, and reassuring tone.
- Avoid generic, robotic, overly enthusiastic, or excessively verbose responses.

COMMUNICATION:
- Keep spoken responses concise, natural, and easy to understand.
- For simple greetings, respond warmly and briefly.
- Explain technical topics clearly and logically when asked.
- Never narrate internal reasoning or describe implementation details unnecessarily.
- Respond directly to the user's latest request.

TOOLS:
- You have access to tools that can perform actions on the user's computer.
- Use a tool whenever the user's request clearly requires its functionality.
- Do not claim that an action was completed unless the tool was actually called.
- After a tool finishes, acknowledge the result naturally and briefly.
- If an action fails, explain the failure honestly.

VOICE:
- Your responses will be converted into speech.
- Write as if speaking aloud, not as if writing a formal report.
- Avoid unnecessary markdown, lists, symbols, and visual formatting in spoken responses.
- Prefer natural conversational phrasing.

IDENTITY:
- You are J.A.R.V.I.S., the user's personal AI assistant.
- Remain calm, capable, discreet, and helpful at all times.
"""


load_dotenv()

client = OpenAI()

def llm(user_query: str):
    return client.responses.create(
        model='gpt-4o-mini',
        input=user_query,
        tools=[
            {
                'type': 'function',
                'name': 'start_work_mode',
                'description': 'Call this function when user says "Lets get to work", this tool opens VS code and Youtube',
                'strict': True,
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                },
            }
        ],
        instructions=instructions        
    )



while True:
    user_audio_path = record_audio(duration=5)
    user_text = transcriber_func(user_audio_path)

    response = llm(user_text)

    for item in response.output:
        if item.type == 'function_call':
            if item.name == 'start_work_mode':
                tool_result = start_work_mode(
                    str(Path.home() / 'Documents' / 'search_agent')
                )

                response = client.responses.create(
                    model='gpt-4o-mini',
                    previous_response_id=response.id,
                    input=[
                        {
                            'type': 'function_call_output',
                            'call_id': item.call_id,
                            'output': str(tool_result)
                        }
                    ],
                    instructions=instructions,
                )

                for output_item in response.output:
                    if output_item.type == 'message':
                        for content in output_item.content:
                            if content.type == 'output_text':
                                audio_path = tts(content.text)
                                play_audio(audio_path)

        elif item.type == 'message':
            for content in item.content:
                if content.type == 'output_text':
                    audio_path = tts(content.text)
                    play_audio(audio_path)


            