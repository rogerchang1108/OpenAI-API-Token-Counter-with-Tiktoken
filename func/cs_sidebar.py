import os
from pathlib import Path
import base64

import streamlit as st

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def cs_sidebar():
    st.sidebar.markdown('''
        <div style="display: flex; flex-direction: row; align-items: center;">
            <img src='data:image/png;base64,{}' class='img-fluid' width=50 height=50 style="margin-right: 10px;">
            <img src='data:image/png;base64,{}' class='img-fluid' width=50 height=50 style="margin-right: 10px;">
        </div>
        '''.format(
            img_to_bytes('img/logomark_website.png'),
            img_to_bytes('img/openai_icon.png')
        ), 
        unsafe_allow_html=True
    )
    
    st.sidebar.header('Streamlit Token Counter')