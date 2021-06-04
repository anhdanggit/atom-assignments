
# Ref: https://towardsdatascience.com/data-apps-with-pythons-streamlit-b14aaca7d083

#/app.py
import streamlit as st #pip install streamlit
import pandas as pd
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

# Initial setup
st.set_page_config(layout="wide")

def get_df(file):
  # get extension and read file
  extension = file.name.split('.')[1]
  if extension.upper() == 'CSV':
    df = pd.read_csv(file)
  elif extension.upper() == 'XLSX':
    df = pd.read_excel(file, engine='openpyxl')
  elif extension.upper() == 'PICKLE':
    df = pd.read_pickle(file)
  return df


# Function to explore the data
def summary(df, nrows):
  # DATA
  st.write('Data:')
  st.write(df.head(nrows))
  # SUMMARY
  df_types = pd.DataFrame(df.dtypes, columns=['Data Type'])
  numerical_cols = df_types[~df_types['Data Type'].isin(['object',
                   'bool'])].index.values
  df_types['Count'] = df.count()
  df_types['Unique Values'] = df.nunique()
  df_types['Min'] = df[numerical_cols].min()
  df_types['Max'] = df[numerical_cols].max()
  df_types['Average'] = df[numerical_cols].mean()
  df_types['Median'] = df[numerical_cols].median()
  df_types['q25'] = df[numerical_cols].quantile(0.25)
  df_types['q75'] = df[numerical_cols].quantile(0.75)
  df_types['q90'] = df[numerical_cols].quantile(0.90)
  st.write('Summary:')
  st.write(df_types)

def transform(df):
  # Select sample size
  frac = st.sidebar.slider('Random sample (%)', 1, 100, 100)
  if frac < 100:
    df = df.sample(frac=frac/100)
  # Select columns
  cols = st.multiselect('Columns', 
                        df.columns.tolist(),
                        df.columns.tolist())
  df = df[cols]
  return df

def explore(df):
  pr = ProfileReport(df, explorative=True)
  st_profile_report(pr)

def main():
    st.title('Glimpse a dataset')
    st.markdown('''
    Replicate a tool to automate first glimpse on a dataset. 
    Ref: [Data Apps with Python Streamlit](https://towardsdatascience.com/data-apps-with-pythons-streamlit-b14aaca7d083)''')
    
    file = st.file_uploader("Upload file", type=['csv','xlsx','pickle'])
    st.sidebar.markdown('## Controls')
    nrows = st.sidebar.slider("Displayed nrows", min_value= 3, max_value=10, value=5, step=1)
    if not file:
        st.write("Upload a .csv or .xlsx file to get started")
    else:
        df = get_df(file)
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        num_col_only = st.checkbox("Display Numeric Cols only", value=False)
        df = df.select_dtypes(include=numerics) if num_col_only == True else df
        df = transform(df)
        summary(df, nrows)
        if st.button('Generate Profiling Report'):
            explore(df)

main()

## Run: streamlit run streamlit/data_glimpse.py