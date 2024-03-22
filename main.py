import os
import tiktoken
from openai import OpenAI

import streamlit as st

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0125"):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        st.write("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-4-0125-preview", # GPT-4 Turbo
        "gpt-4-1106-preview", # GPT-4 Turbo
        "gpt-4-0613", # Older models
        "gpt-3.5-turbo-0125", # GPT-3.5 Turbo
        "gpt-3.5-turbo-1106", # Older models
        "gpt-3.5-turbo-0613", # Older models
        "gpt-3.5-turbo-16k-0613", # Older models
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif "gpt-4-turbo-preview" in model:
        st.write("Warning: gpt-4-turbo-preview may update over time. Returning num tokens assuming gpt-4-0125-preview.")
        return num_tokens_from_messages(messages, model="gpt-4-0125-preview")
    elif "gpt-4" in model:
        st.write("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    elif "gpt-3.5-turbo-16k" in model:
        st.write("Warning: gpt-3.5-turbo-16k may update over time. Returning num tokens assuming gpt-3.5-turbo-16k-0613")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-16k-0613")
    elif "gpt-3.5-turbo" in model:
        st.write("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0125")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0125")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3
    
    st.write(f'{model}: model chose by user.')
    # example token count from the function defined above
    st.write(f"{num_tokens} prompt(input) tokens counted by Tiktoken.")

def call_openaiapi(openai_api_key, model_selected, prompt_messages):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY", openai_api_key),
        # api_key=os.environ.get("OPENAI_API_KEY"),
    )

    # example token count from the OpenAI API
    chat_completion = client.chat.completions.create(
        model=model_selected,
        messages=prompt_messages,
        temperature=0,
    )

    st.write(f'{chat_completion.model}: model return by the OpenAI API.')
    st.write(f'{chat_completion.usage.prompt_tokens} prompt(input) tokens counted by the OpenAI API.')
    st.write(f'{chat_completion.usage.completion_tokens} completion(output) tokens counted by the OpenAI API.')
    st.write(chat_completion.choices[0].message.content)

example_messages = [
    {
        "role": "system",
        "content": "Identify words in the following passage that are too difficult for intermediate (CEFR: B2) students and replace these words with easier words (B2 or lower), so the results are more accessible for the intermediate students:",
    },
    {
        "role": "system",
        "name": "example_user",
        "content": "The hottest day of the summer so far was drawing to a close and a drowsy silence lay over the large, square houses of Privet Drive.",
    },
    {
        "role": "system",
        "name": "example_assistant",
        "content": "The hottest day of the summer so far was coming to an end and a sleepy silence cover the large, square houses of Privet Road.",
    },
    {
        "role": "user",
        "content": "April 9, 1940. It was a breakfast like any other until the dishes started to rattle. Then an all-alert siren pierced the morning calm and the sky above Odense, Denmark, thundered with sound. The Pedersen family pushed back their chairs, raced outside, and looked up. Suspended above them in close formation was a squadron of dark airplanes. They were flying ominously low, no more than three hundred meters above the ground. The black marks on each wing tagged them as German warplanes. Scraps of green paper fluttered down.",
    },
]

tab1, tab2 = st.tabs(["Tiktoken", "OpenAI"])

with tab1:
    st.title("Count prompt(input) tokens by Tiktoken")
        
    with st.form(key='messages_form'):
        st.write("## Messages:")
        for i, msg in enumerate(example_messages):
            role = st.selectbox(f"Role for Message {i+1}:", ["system", "user"], 
                                index = 0 if msg["role"] == "system" else 1)
            
            if msg.get("name", "") != "" :
                name = st.selectbox(f"Name for Message {i+1} (optional):", ["example_user", "example_assistant"], 
                                index = 0 if msg["name"] == "example_user" else 1)
                
            content = st.text_area(f"Content for Message {i+1}:", value=msg["content"], height=150)
            
            if msg.get("name", "") != "" :
                example_messages[i] = {"role": role, "name": name, "content": content}
            else:
                example_messages[i] = {"role": role, "content": content}

        model_selected = st.selectbox(
            'Model',
            [
            "gpt-3.5-turbo-0125", # GPT-3.5 Turbo
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-1106", # Older models
            "gpt-3.5-turbo-16k",
            "gpt-3.5-turbo-0613", # Older models
            "gpt-3.5-turbo-16k-0613", # Older models
            "gpt-4-0125-preview", # GPT-4 Turbo
            "gpt-4-turbo-preview",
            "gpt-4-1106-preview", # GPT-4 Turbo
            "gpt-4",
            "gpt-4-0613", # Older models
            ],
        )

        submit_button1 = st.form_submit_button(
            label='Submit', 
        )
        
    if submit_button1:
        num_tokens_from_messages(example_messages, model_selected)

with tab2:
    st.title("Verify the prompt(input) tokens and Check completion(output) tokens by OpenAI API")
    if 'disabled' not in st.session_state:
        st.session_state.disabled = True

    openai_api_key = st.text_input('OpenAI API Key:')
    
    with st.form(key='my_form2'):
        if openai_api_key:
            st.success('Unlocked!', icon = '🔓')
            st.session_state.disabled = False
        else:
            st.info('Locked: Please Input Your OpenAI API Key First.', icon = '🔐')
            st.session_state.disabled = True
    
    
        for msg in example_messages:
            st.write(f"{msg['role']} ({msg.get('name', '')}): \n\n{msg['content']}")
            
        submit_button2 = st.form_submit_button(
            label='Submit', 
            disabled=st.session_state.disabled
        )
            
    if submit_button2:
        call_openaiapi(openai_api_key, model_selected, example_messages)  