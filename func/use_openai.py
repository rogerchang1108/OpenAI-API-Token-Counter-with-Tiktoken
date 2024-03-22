import os
from openai import OpenAI

import streamlit as st

def reply_from_openai(col, openai_api_key, model_selected, prompt_messages):
    client = OpenAI(
        api_key=openai_api_key,
        # api_key=os.environ.get('OPENAI_API_KEY'),
    )

    # example token count from the OpenAI API
    chat_completion = client.chat.completions.create(
        model=model_selected,
        messages=prompt_messages,
        temperature=0,
    )

    col.write(f'{chat_completion.model}: model return by the OpenAI API.')
    col.write(f'{chat_completion.usage.prompt_tokens} prompt(input) tokens counted by the OpenAI API.')
    col.write(f'{chat_completion.usage.completion_tokens} completion(output) tokens counted by the OpenAI API.')
    col.write(chat_completion.choices[0].message.content)