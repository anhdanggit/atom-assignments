
# Ref: https://github.com/tirthajyoti/ML-apps-with-Streamlit/blob/master/scripts/gauss2d.py

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys


# Settings
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("3D Gaussian Distribution x Sigma, Mu, Density")
#st.text(sys.executable) ## -> To solve the python interpret, python3.7 -m pip install seaborn
#st.set_page_config(layout="wide")

# To show to the UI
code = """
data_density = st.slider("Data density",
                    min_value= 25,
                    max_value=200,
                    value=75,
                    step=25)
sigma = st.slider("Sigma",
                    min_value= 0.1,
                    max_value=2.0,
                    value=1.0,
                    step=0.1)
mu = st.slider("Sigma",
                    min_value= -1.0,
                    max_value=1.0,
                    value=0.0,
                    step=0.1)
x, y = np.meshgrid(np.linspace(-2,2,data_density), np.linspace(-2,2,data_density))
d = np.sqrt(x*x+y*y)
sigma, mu = sigma, mu
g = np.exp(-( (d-mu)**2 / ( 2.0 * sigma**2 ) ) )
sns.heatmap(g)
"""

# Layout
#st.beta_set_page_config(layout="wide")
col1, col2 = st.beta_columns((1, 1))

col1.markdown("## Code")
col1.code(code)

st.sidebar.markdown("## Controls")
data_density = st.sidebar.slider("Data density",
                    min_value= 25,
                    max_value=200,
                    value=75,
                    step=25)

sigma = st.sidebar.slider("Sigma",
                    min_value= 0.1,
                    max_value=2.0,
                    value=1.0,
                    step=0.1)

mu = st.sidebar.slider("Mu",
                    min_value= -1.0,
                    max_value=1.0,
                    value=0.0,
                    step=0.1)

x, y = np.meshgrid(np.linspace(-2,2,data_density), np.linspace(-2,2,data_density))
d = np.sqrt(x*x+y*y)
sigma, mu = sigma, mu
g = np.exp(-( (d-mu)**2 / ( 2.0 * sigma**2 ) ) )
#sns.heatmap(g)

fig = plt.figure(figsize=(7, 7))
ax = plt.axes(projection='3d')
w = ax.plot_wireframe(x, y, g)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('PDF')
ax.set_title('3D plot of Gaussian Distribution')

col2.markdown("## Plot")
col2.pyplot()

# Run: streamlit run streamlit/gauss2d.py