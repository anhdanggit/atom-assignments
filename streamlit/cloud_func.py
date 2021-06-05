
import streamlit as st
import requests # -> Để call API
import json # -> Xử lý file JSON
import pandas as pd # -> Thư viện xử lý dữ liệu dạng bảng
import numpy as np
import re # -> Thư viện xử lý text: regular expressions
from datetime import datetime as dt # -> Thư viện xử lý dữ liệu thời 


st.title('Tương tác với Cloud Function - UI')
passcode = st.sidebar.text_input('Passcode', '')
message = st.sidebar.text_input('Message', '')

#st.text('Token: {}'.format(token))
    
endpoint1 = 'https://asia-southeast2-quickstart-313303.cloudfunctions.net/function-1'
data = {"passcode":passcode, "message":message}
st.markdown('## Input')
st.write(data)
if st.sidebar.button('Call API'):
    # Ref: https://medium.com/google-cloud/setup-and-invoke-cloud-functions-using-python-e801a8633096
    response = requests.post(endpoint1, json=data)
    response_json = json.loads(response.content)
    st.markdown('## Output')
    try:
        st.markdown('**Status**: {}'.format(response_json['status']))
        st.markdown('**Message**: {}'.format(response_json['message']))
    except:
        st.markdown('**Status**: {}'.format('ERROR'))
    #st.write(response_json)
    
## Run: streamlit run streamlit/datacracy_slack.py