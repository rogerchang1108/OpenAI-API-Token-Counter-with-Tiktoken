import os
import tiktoken
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0125"):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
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
        print("Warning: gpt-4-turbo-preview may update over time. Returning num tokens assuming gpt-4-0125-preview.")
        return num_tokens_from_messages(messages, model="gpt-4-0125-preview")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    elif "gpt-3.5-turbo-16k" in model:
        print("Warning: gpt-3.5-turbo-16k may update over time. Returning num tokens assuming gpt-3.5-turbo-16k-0613")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-16k-0613")
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0125")
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
    return num_tokens

example_messages = [
    {
        "role": "system",
        "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English.",
    },
    {
        "role": "system",
        "name": "example_user",
        "content": "New synergies will help drive top-line growth.",
    },
    {
        "role": "system",
        "name": "example_assistant",
        "content": "Things working well together will increase revenue.",
    },
    {
        "role": "user",
        "content": "Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage.",
    },
]

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

for model in [
    "gpt-4-0125-preview", # GPT-4 Turbo
    "gpt-4-turbo-preview",
    "gpt-4-1106-preview", # GPT-4 Turbo
    "gpt-4",
    "gpt-4-0613", # Older models
    "gpt-3.5-turbo-0125", # GPT-3.5 Turbo
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-1106", # Older models
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-0613", # Older models
    "gpt-3.5-turbo-16k-0613", # Older models
    ]:
    print(f'{model}: model chose by user.')
    # example token count from the function defined above
    print(f"{num_tokens_from_messages(example_messages, model)} prompt tokens counted by num_tokens_from_messages().")
    
    # example token count from the OpenAI API
    chat_completion = client.chat.completions.create(
        model=model,
        messages=example_messages,
        temperature=0,
        max_tokens=1,
    )
    print()
    
    print(f'{chat_completion.model}: model return by the OpenAI API.')
    print(f'{chat_completion.usage.prompt_tokens} prompt(input) tokens counted by the OpenAI API.')
    print(f'{chat_completion.usage.completion_tokens} completion(output) tokens counted by the OpenAI API.')
    print()
    
    print(chat_completion.choices[0].message.content or "", end="")
    print()
    print()