# TODO: improve table rendering with aggrid
# TODO: Add description

import streamlit as st
import pandas
import plotly
import numpy


st.set_page_config(layout="wide", page_title="Home", initial_sidebar_state="collapsed")

# Set session states
if 'vastdiff_output' not in st.session_state:
    st.session_state.vastdiff_output = []
if 'num' not in st.session_state:
    st.session_state.num = 1
if 'rename_psiA' and 'rename_psiB' not in st.session_state:
    st.session_state.rename_psiA, st.session_state.rename_psiB = '', ''
if 'figures' not in st.session_state:
    st.session_state.figures = {}



left_col, right_col = st.columns(2)
left_col.title("Exon-viewer")
left_col.header("A tool for visualising vast-tools alternative splicing of exons and sequence querying.")

st.markdown(
        """
        ## Summary
        Data available from [VastDB, v3](ttps://vastdb.crg.eu/wiki/Downloads).

        """
)

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