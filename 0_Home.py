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
left_col.header("Visualise vast-tools alternative splicing analysis of exons")

st.markdown(
        """
        ### Exon-viewer
        
        **Exon-viewer** supports three species:
        
        * Homo sapiens (VastDB v. hg38)
        * Mus musculus (VastDB v. mm10)
        * Danio rerio  (VastDB v. danRer10)
        
        Data available from [VastDB, v3](https://vastdb.crg.eu/wiki/Downloads).
        
        ### How to use
        
        1. Generate input table using vast-tools compare. 
        
        ```
        vast-tools compare INCLUSION_LEVELS_FULL-root.tab \ 
        -a [SAMPLE_A] -b [SAMPLE_b] --min_dPSI [value] [...] \ 
        --print_all_events
        ```
        
        By default, the command will generate a table ```AllEvents-[parameters].tab``` for all events that pass the
        coverage filters and thresholds.
        
        2. Select exons.
        
        Run the following command to select only exons from ```AllEvents-[parameters].tab```:
        
        ```
        awk 'NR==1; {if ($1 ~ /EX/) print}' AllEvents-[parameters].tab > InputData.tab
        ```
        
        3. Navigate to Data Upload page of Exon-viewer and upload table.
        """
)

st.markdown(
    """
    ---
    Developed and maintained by Simon Bajew

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