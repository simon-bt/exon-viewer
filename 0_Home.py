# TODO: improve table rendering with aggrid
# TODO: Add description

import streamlit as st
import pandas
import plotly
import numpy
import os
import sys

project_dir = os.getcwd()
sys.path.append(f'/{project_dir}')


st.set_page_config(layout="wide", page_title="Home", initial_sidebar_state="collapsed")

# Set session states
if 'vastdiff_output' not in st.session_state:
    st.session_state.vastdiff_output = []
if 'num' not in st.session_state:
    st.session_state.num = 1
if 'rename_psiA' and 'rename_psiB' not in st.session_state:
    st.session_state.rename_psiA, st.session_state.rename_psiB = '', ''

left_col, right_col = st.columns(2)
left_col.title("VAST-viewer")
left_col.header("A tool for visualising vast-tools alternative splicing analysis and sequence querying.")

st.markdown(
        """
        ## Summary
        Impact on open reading frame is available from [VastDB, v3](ttps://vastdb.crg.eu/wiki/Downloads) and generated 
        as described in [Irimia et al, 2014]().

        """
)

_, center, _ = st.columns((2, 1, 2))
with center:
    reset_button = st.button(label='Restart')
    if reset_button:
        var = [
            st.session_state[key] for key in st.session_state.keys()
        ]


st.markdown(
    """
    ---
    Developed and Maintained by Simon Bajew

    Copyright (c) 2022 Simon Bajew
    """
)

st.markdown(
    """
    ---
    Session Info:
    """
)

# Session Info
st.text(f"Streamlit v.{st.__version__}\n"
        f"Pandas v.{pandas.__version__}\n"
        f"Numpy v.{numpy.__version__}\n"
        f"Plotly v.{plotly.__version__}\n")