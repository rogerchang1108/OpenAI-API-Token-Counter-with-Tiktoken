import os
import tiktoken
from pathlib import Path
import base64
from openai import OpenAI

import streamlit as st

st.set_page_config(
    page_title='Streamlit token counter',
    layout='wide',
    initial_sidebar_state='expanded',
)

def main():
    cs_sidebar()
    cs_body()

    return None

example_messages = [
    {
        'role': 'system',
        'content': 'Identify words in the following passage that are too difficult for intermediate (CEFR: B2) students and replace these words with easier words (B2 or lower), so the results are more accessible for the intermediate students:',
    },
    {
        'role': 'system',
        'name': 'example_user',
        'content': 'The hottest day of the summer so far was drawing to a close and a drowsy silence lay over the large, square houses of Privet Drive.',
    },
    {
        'role': 'system',
        'name': 'example_assistant',
        'content': 'The hottest day of the summer so far was coming to an end and a sleepy silence cover the large, square houses of Privet Road.',
    },
    {
        'role': 'user',
        'content': 'April 9, 1940. It was a breakfast like any other until the dishes started to rattle. Then an all-alert siren pierced the morning calm and the sky above Odense, Denmark, thundered with sound. The Pedersen family pushed back their chairs, raced outside, and looked up. Suspended above them in close formation was a squadron of dark airplanes. They were flying ominously low, no more than three hundred meters above the ground. The black marks on each wing tagged them as German warplanes. Scraps of green paper fluttered down.',
    },
]

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def cs_sidebar():
    st.sidebar.markdown('''[<img src='data:image/png;base64,{}' class='img-fluid' width=32 height=32>](https://streamlit.io/)'''.format(img_to_bytes('img/logomark_website.png')), unsafe_allow_html=True)
    st.sidebar.header('Streamlit token counter')

def cs_body():
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
        col1.write(f'{model_selected}: model chose by user.') 
        col1.write(f'{st.session_state.num_tokens} prompt(input) tokens counted by Tiktoken.')

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
            st.write(f'{msg['role']} ({msg.get('name', '')}): \n\n{msg['content']}')
            
        submit_button2 = st.form_submit_button(
            label='Submit', 
            disabled=st.session_state.disabled
        )
            
    if submit_button2:
        call_openaiapi(col2, openai_api_key, model_selected, example_messages)
     
def num_tokens_from_messages(col, messages, model='gpt-3.5-turbo-0125'):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        col.write('Warning: model not found. Using cl100k_base encoding.')
        encoding = tiktoken.get_encoding('cl100k_base')
    if model in {
        'gpt-4-0125-preview', # GPT-4 Turbo
        'gpt-4-1106-preview', # GPT-4 Turbo
        'gpt-4-0613', # Older models
        'gpt-3.5-turbo-0125', # GPT-3.5 Turbo
        'gpt-3.5-turbo-1106', # Older models
        'gpt-3.5-turbo-0613', # Older models
        'gpt-3.5-turbo-16k-0613', # Older models
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif 'gpt-4-turbo-preview' in model:
        col.write('Warning: gpt-4-turbo-preview may update over time. Returning num tokens assuming gpt-4-0125-preview.')
        return num_tokens_from_messages(messages, model='gpt-4-0125-preview')
    elif 'gpt-4' in model:
        col.write('Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.')
        return num_tokens_from_messages(messages, model='gpt-4-0613')
    elif 'gpt-3.5-turbo-16k' in model:
        col.write('Warning: gpt-3.5-turbo-16k may update over time. Returning num tokens assuming gpt-3.5-turbo-16k-0613')
        return num_tokens_from_messages(messages, model='gpt-3.5-turbo-16k-0613')
    elif 'gpt-3.5-turbo' in model:
        col.write('Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0125')
        return num_tokens_from_messages(messages, model='gpt-3.5-turbo-0125')
    else:
        raise NotImplementedError(
            f'''num_tokens_from_messages() is not implemented for model {model}.'''
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == 'name':
                num_tokens += tokens_per_name
    num_tokens += 3
    
    return num_tokens
    
def call_openaiapi(col, openai_api_key, model_selected, prompt_messages):
    client = OpenAI(
        api_key=os.environ.get('OPENAI_API_KEY', openai_api_key),
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

contents_font_css = """<style>
    div[class*="stTextInput"] label p {
        font-size: 24px;
    }
    div[class*="stSelectbox"] label p, div[class*="stTextArea"] label p {
        font-size: 22px;
    }
  
    input, textarea {
        font-size: 20px !important;
    }
</style>"""

st.markdown(contents_font_css, unsafe_allow_html=True)

if __name__ == '__main__':
    main()