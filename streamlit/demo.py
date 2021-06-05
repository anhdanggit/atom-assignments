
import streamlit as st

st.title("Demo in Class")

# input
st.markdown('## Input')
is_learner = st.checkbox('Learner')
default_value_goes_here = 'Hello World'
user_input = st.text_input("Input a text", default_value_goes_here)

# output 
st.markdown('## Output')
st.write(user_input)
if is_learner:
    st.write('Hello Learner')


## streamlit run streamlit/demo.py