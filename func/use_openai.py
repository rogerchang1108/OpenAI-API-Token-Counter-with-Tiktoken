import os
from openai import OpenAI

import streamlit as st

def reply_from_openai(col, openai_api_key, model_selected, prompt_messages):
    client = OpenAI(
        api_key=openai_api_key,
        # api_key=os.environ.get('OPENAI_API_KEY'),
    )
    
    try:
        # example token count from the OpenAI API
        chat_completion = client.chat.completions.create(
            model=model_selected,
            messages=prompt_messages,
            temperature=0,
        )
        
        col.markdown(f'<p class="markdown-custom-1">{chat_completion.model}: model return by the OpenAI API.</p>', 
                     unsafe_allow_html=True)
        col.markdown(f'<p class="markdown-custom-1">{chat_completion.usage.prompt_tokens} prompt(input) tokens counted by the OpenAI API.</p>', 
                     unsafe_allow_html=True)
        col.markdown(f'<p class="markdown-custom-1">{chat_completion.usage.completion_tokens} completion(output) tokens counted by the OpenAI API.</p>', 
                     unsafe_allow_html=True)
        col.markdown(chat_completion.choices[0].message.content)
    
    except Exception as e:
        col.info('❗Something went wrong! Check your OpenAI API Key!!!')
        col.error(f'An error occurred: {e}')