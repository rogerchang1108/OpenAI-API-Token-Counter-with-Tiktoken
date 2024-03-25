import os
import streamlit as st

from cs_body import cs_body
from cs_sidebar import cs_sidebar

st.set_page_config(
    page_title='Streamlit token counter',
    layout='wide',
    initial_sidebar_state='expanded',
)

contents_font_css = """
    <style>
        /* st.text_input, st.number_input label */
        div[class*="stTextInput"] label p, div[class*="stNumberInput"] label p {
            font-size: 20px;
        }        
        /* st.text_input, st.number_input value */
        input, input[type="number"]  {
            font-size: 16px !important; 
        }
        
        /* st.selectbox, st.text_area label */
        div[class*="stSelectbox"] label p, div[class*="stTextArea"] label p {
            font-size: 20px;
        }
        /* st.selectbox options */
        div[data-baseweb="select"] div {
            font-size: 16px !important; 
        }
        /* st.text_area value */
        textarea {
            font-size: 16px !important;
        }
        
        /* st.markdown */
        .markdown-custom-1 {
            font-size:20px !important;
        }
        .markdown-custom-2 {
            font-size:16px !important;
        }
    </style>
"""

st.markdown(contents_font_css, unsafe_allow_html=True)

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

def main():
    cs_sidebar()
    cs_body(example_messages)

    return None

if __name__ == '__main__':
    main()