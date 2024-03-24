import os
import tiktoken

import streamlit as st

def num_tokens_from_messages(col, messages, model='gpt-3.5-turbo-0125'):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # col.write('Warning: model not found. Using cl100k_base encoding.')
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
        col.info('❗ Warning: gpt-4-turbo-preview may update over time. Returning num tokens assuming gpt-4-0125-preview.')
        return num_tokens_from_messages(col, messages, model='gpt-4-0125-preview')
    elif 'gpt-4' in model:
        col.info('❗ Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.')
        return num_tokens_from_messages(col, messages, model='gpt-4-0613')
    elif 'gpt-3.5-turbo-16k' in model:
        col.info('❗ Warning: gpt-3.5-turbo-16k may update over time. Returning num tokens assuming gpt-3.5-turbo-16k-0613')
        return num_tokens_from_messages(col, messages, model='gpt-3.5-turbo-16k-0613')
    elif 'gpt-3.5-turbo' in model:
        col.info('❗ Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0125')
        return num_tokens_from_messages(col, messages, model='gpt-3.5-turbo-0125')
    else:
        col.error(f'Sorry, Token Counter is not implemented for model "{model}". Try another model!')
        return 0
        # raise NotImplementedError(
        #     f'''num_tokens_from_messages() is not implemented for model {model}.'''
        # )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == 'name':
                num_tokens += tokens_per_name
    num_tokens += 3
    
    return num_tokens