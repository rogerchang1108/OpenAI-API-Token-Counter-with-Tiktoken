import os

import streamlit as st

from func.use_openai import reply_from_openai
from func.use_tiktoken import num_tokens_from_messages

def cs_body(example_messages):
    if 'num_tokens' not in st.session_state:
        st.session_state.num_tokens = 0
    
    # Header Part:
    colh1, colh2 = st.columns(2)
    
    ## Column header 1: Tiktoken Header
    colh1.header('Count Input Tokens by Tiktoken 🧮')
    
    ## Column header 2: OpenAI Header
    colh2.header('Verify Tokens by OpenAI API 🤖')
    
    # OpenAI API Key Part
    if 'disabled' not in st.session_state:
        st.session_state.disabled = True

    openai_api_key = st.text_input(label = '🔑 OpenAI API Key: ', 
                                   max_chars = 60,
                                   type = 'password',
                                   placeholder = 'Enter your OpenAI API Key here...')
    
    # Body Part: 
    col1, col2 = st.columns(2)
    
    ## Column 1: Tiktoken Part   
    with col1.form(key='tiktoken_form'):
        st.subheader('Messages: ')
        
        for i, msg in enumerate(example_messages):
            role = st.selectbox(label = f'Role for Message {i+1}: ', 
                                options = ['system', 'user'], 
                                index = 0 if msg['role'] == 'system' else 1)
            
            if msg.get('name', '') != '' :
                name = st.selectbox(label = f'Name for Message {i+1} (optional): ', 
                                    options = ['example_user', 'example_assistant'], 
                                    index = 0 if msg['name'] == 'example_user' else 1)
                
            content = st.text_area(label = f'Content for Message {i+1}: ', 
                                   value = msg['content'])
            
            if msg.get('name', '') != '' :
                example_messages[i] = {'role': role, 'name': name, 'content': content}
            else:
                example_messages[i] = {'role': role, 'content': content}

        model_selected = st.selectbox(
            'Model',
            [
            'gpt-3.5-turbo-0125', # GPT-3.5 Turbo
            'gpt-3.5-turbo',
            'gpt-3.5-turbo-1106', # Older models
            'gpt-3.5-turbo-16k',
            'gpt-3.5-turbo-0613', # Older models
            'gpt-3.5-turbo-16k-0613', # Older models
            'gpt-4-0125-preview', # GPT-4 Turbo
            'gpt-4-turbo-preview',
            'gpt-4-1106-preview', # GPT-4 Turbo
            'gpt-4',
            'gpt-4-0613', # Older models
            ],
        )

        submit_button1 = st.form_submit_button(
            label='Submit', 
        )
        
    if submit_button1:
        st.session_state.num_tokens = num_tokens_from_messages(col1, example_messages, model_selected)
    
    if st.session_state.num_tokens != 0:
        col1.markdown(f'<p class="markdown-custom-1">{model_selected}: model chose by user.</p>', 
                      unsafe_allow_html=True) 
        col1.markdown(f'<p class="markdown-custom-1">{st.session_state.num_tokens} prompt(input) tokens counted by Tiktoken.</p>', 
                      unsafe_allow_html=True)

    ## Column 2: OpenAI Part
    with col2.form(key='openai_form2'):
        st.subheader('Messages to OpenAI: ')
        
        if openai_api_key:
            st.success('Unlocked!', icon = '🔓')
            st.session_state.disabled = False
        else:
            st.info('Locked: Please Input Your OpenAI API Key First.', icon = '🔐')
            st.session_state.disabled = True
    
        for msg in example_messages:
            st.markdown(f'<p class="markdown-custom-1">{msg['role']} ({msg.get('name', '')}): \n\n<p class="markdown-custom-2">{msg['content']}</p></p>', 
                        unsafe_allow_html=True)
            
        submit_button2 = st.form_submit_button(
            label='Submit', 
            disabled=st.session_state.disabled
        )
            
    if submit_button2:
        reply_from_openai(col2, openai_api_key, model_selected, example_messages)