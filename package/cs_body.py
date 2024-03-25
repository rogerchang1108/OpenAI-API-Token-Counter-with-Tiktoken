import os
import streamlit as st

def cs_body(example_messages):
    from package import reply_from_openai, num_tokens_from_messages
    
    if 'num_tokens' not in st.session_state:
        st.session_state.num_tokens = 0
    if 'response' not in st.session_state:
        st.session_state.response = ''
    
    # Header Part:
    colh1, colh2 = st.columns(2)
    
    ## Column header 1: Tiktoken Header
    colh1.subheader('Count Input Tokens by Tiktoken 🧮')
    
    ## Column header 2: OpenAI Header
    colh2.subheader('Verify Tokens by OpenAI API 🤖')
    
    # OpenAI API Key Part
    if 'disabled' not in st.session_state:
        st.session_state.disabled = True

    openai_api_key = st.text_input(label = 'OpenAI API Key 🔑:', 
                                   max_chars = 60,
                                   type = 'password',
                                   placeholder = 'Enter your OpenAI API Key here...')
    
    # OpenAI API Price Setting
    colp1, colp2 = st.columns(2)
    
    input_price_per_M = colp1.number_input(label = 'Input Price ($ / 1M tokens)',
                                        min_value = 0.01,
                                        max_value = 1000.00,
                                        value = 0.50,
                                        step = 0.10,)
    
    output_price_per_M = colp2.number_input(label = 'Output Price ($ / 1M tokens)',
                                        min_value = 0.01,
                                        max_value = 1000.00,
                                        value = 1.50,
                                        step = 0.10,)
    
    # Body Part: 
    col1, col2 = st.columns(2)
    
    ## Column 1: Tiktoken Part
    with col1:
        with st.form(key='tiktoken_form'):
            st.markdown(f'<p class="markdown-custom-1">Messages: </p>', 
                        unsafe_allow_html=True) 
            
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
            st.session_state.num_tokens = num_tokens_from_messages(st, example_messages, model_selected)
            st.session_state.response = ''
        
        if st.session_state.num_tokens != 0:
            with st.container(border=True):
                st.markdown(f'<p class="markdown-custom-1">{model_selected} model chose by user</p>', 
                            unsafe_allow_html=True) 
                
                st.markdown(f'<p class="markdown-custom-1">📥 {st.session_state.num_tokens} input tokens counted by Tiktoken</p>', 
                            unsafe_allow_html=True)
                estimated_input_price = st.session_state.num_tokens * input_price_per_M / 1000000
                formatted_estimated_input_price = f"{estimated_input_price:.8f}"
                st.markdown(f'<p class="markdown-custom-1">💳 {formatted_estimated_input_price}$ Estimated Input Price</p>', 
                        unsafe_allow_html=True)

    ## Column 2: OpenAI Part
    with col2:
        with st.form(key='openai_form2'):
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
           st.session_state.response = reply_from_openai(st, openai_api_key, model_selected, example_messages)
        
        if st.session_state.response != '':
            with st.container(border=True):
                st.markdown(f'<p class="markdown-custom-2">OpenAI Output:</p>',
                            unsafe_allow_html=True)
                st.markdown(f'<p class="markdown-custom-1">{st.session_state.response.choices[0].message.content}</p>',
                            unsafe_allow_html=True)
            
            with st.container(border=True):           
                st.markdown(f'<p class="markdown-custom-1">{st.session_state.response.model} model return by OpenAI API.</p>', 
                            unsafe_allow_html=True)
                
                st.markdown(f'<p class="markdown-custom-1">📥 {st.session_state.response.usage.prompt_tokens} input tokens counted by OpenAI API.</p>', 
                            unsafe_allow_html=True)
                input_price = st.session_state.response.usage.prompt_tokens * input_price_per_M / 1000000
                formatted_input_price = f"{input_price:.8f}"
                st.markdown(f'<p class="markdown-custom-1">💸 {formatted_input_price}$ Input Price</p>', 
                            unsafe_allow_html=True)
                
                st.markdown(f'<p class="markdown-custom-1">📤 {st.session_state.response.usage.completion_tokens} output tokens counted by OpenAI API.</p>', 
                            unsafe_allow_html=True)
                output_price = st.session_state.response.usage.completion_tokens * output_price_per_M / 1000000
                formatted_output_price = f"{output_price:.8f}"
                st.markdown(f'<p class="markdown-custom-1">💸 {formatted_output_price}$ Output Price</p>', 
                            unsafe_allow_html=True)