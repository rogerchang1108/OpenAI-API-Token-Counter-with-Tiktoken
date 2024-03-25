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
        response = client.chat.completions.create(
            model=model_selected,
            messages=prompt_messages,
            temperature=0,
        )
        
        return response
    
    except Exception as e:
        col.info('❗Something went wrong! Check your OpenAI API Key!!!')
        col.error(f'An error occurred: {e}')
        return ''