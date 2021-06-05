
import streamlit as st
import json
import requests
import sys
import os
import pandas as pd ## python3.7 -m pip install pandas==0.24.0rc1
import numpy as np

st.title('DataCracy ATOM Tiến Độ Lớp Học')
with open('./env_variable.json','r') as j:
    json_data = json.load(j)

#SLACK_BEARER_TOKEN = os.environ.get('SLACK_BEARER_TOKEN') ## Get in setting of Streamlit Share
SLACK_BEARER_TOKEN = json_data['SLACK_BEARER_TOKEN']
#st.write(json_data['SLACK_BEARER_TOKEN'])

@st.cache
def load_users_df():
    # Slack API User Data
    endpoint = "https://slack.com/api/users.list"
    headers = {"Authorization": "Bearer {}".format(json_data['SLACK_BEARER_TOKEN'])}
    response_json = requests.post(endpoint, headers=headers).json() 
    user_dat = response_json['members']

    ## Convert to CSV
    user_dict = {'user_id':[],'name':[],'display_name':[],'real_name':[],'title':[],'is_bot':[]}
    for i in range(len(user_dat)):
      user_dict['user_id'].append(user_dat[i]['id'])
      user_dict['name'].append(user_dat[i]['name'])
      user_dict['display_name'].append(user_dat[i]['profile']['display_name'])
      user_dict['real_name'].append(user_dat[i]['profile']['real_name_normalized'])
      user_dict['title'].append(user_dat[i]['profile']['title'])
      user_dict['is_bot'].append(int(user_dat[i]['is_bot']))

    user_df = pd.DataFrame(user_dict) 
    return user_df

def load_channel_df():
    endpoint2 = "https://slack.com/api/conversations.list"
    data = {'types': 'public_channel,private_channel'} # -> CHECK: API Docs https://api.slack.com/methods/conversations.list/test
    headers = {"Authorization": "Bearer {}".format(SLACK_BEARER_TOKEN)}
    response_json = requests.post(endpoint2, headers=headers, data=data).json() 
    channel_dat = response_json['channels']
    channel_dict = {'channel_id':[], 'channel_name':[], 'is_channel':[],'creator':[],'created_at':[],'topics':[],'purpose':[],'num_members':[]}
    for i in range(len(channel_dat)):
      channel_dict['channel_id'].append(channel_dat[i]['id'])
      channel_dict['channel_name'].append(channel_dat[i]['name'])
      channel_dict['is_channel'].append(channel_dat[i]['is_channel'])
      channel_dict['creator'].append(channel_dat[i]['creator'])
      channel_dict['created_at'].append(dt.fromtimestamp(float(channel_dat[i]['created'])))
      channel_dict['topics'].append(channel_dat[i]['topic']['value'])
      channel_dict['purpose'].append(channel_dat[i]['purpose']['value'])
      channel_dict['num_members'].append(channel_dat[i]['num_members'])
    channel_df = pd.DataFrame(channel_dict) 
    channel_df = channel_df.replace('', None) # -> replace khoảng trắng bằng giá trị NULL (nan)


# Table data
user_df = load_users_df()

# Input
st.sidebar.markdown('## Tuỳ chỉnh')
all_user = st.sidebar.checkbox('Xem tất cả học viên')
user_id = st.text_input("Nhập Mã Số Người Dùng", 'U01xxxx')

valid_user_id = user_df['user_id'].str.contains(user_id).any()
if valid_user_id:
    if all_user:
        st.write(user_df)
    else:
        display_user_df = user_df[user_df.user_id == user_id]
        st.write(display_user_df)
else:
    st.markdown('Không tìm thấy Mã Số {}'.format(user_id))

## Run: streamlit run streamlit/datacracy_slack.py