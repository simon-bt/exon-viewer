# TODO: add dPSI selection and update plots
# TODO:
# TODO:

import streamlit as st
from src.modules import vis_data

st.set_page_config(layout='wide', page_title='Alternative Splicing')
st.header('Visualise')

expander = st.expander(label='Read more')
with expander:
    st.markdown(
        """
        ## 


        """
    )

page2_container = st.container()


def update_figures():
    testObject.diff_threshold = dpsi_value
    data_callback = testObject.call_diff()
    st.write(data_callback.head())


with st.sidebar:
    st.subheader('Options')
    color_a = st.color_picker(
        label='Select color for Condition A', value='#008080')
    color_b = st.color_picker(
        label='Select colour for Condition B', value='#800020')
    dpsi_value = st.number_input(label='Select dPSI threshold',
                                 min_value=10,
                                 max_value=90,
                                 value=15, on_change=update_figures)

if not st.session_state.vastdiff_output:
    st.warning('Upload Data!')

else:

    testObject = vis_data.SplicingAnalysis(
        data=st.session_state.vastdiff_output[0],
        condition_a=st.session_state.rename_psiA,
        condition_b=st.session_state.rename_psiB,
        color_a=color_a,
        color_b=color_b)
    data_diff = testObject.call_diff()

    with page2_container:
        with st.container():
            st.subheader('Alternative splicing profile')
            left, right = st.columns([1, 1])
            with left:
                st.plotly_chart(testObject.plot_scatter(data_diff))
            with right:
                st.plotly_chart(testObject.plot_violin(data_diff))

        with st.container():
            st.subheader('Differentially spliced events')
            left, right = st.columns([1, 1])
            with left:
                st.plotly_chart(testObject.plot_pie(data_diff))
            with right:
                st.plotly_chart(testObject.plot_dist(data_diff))

        with st.container():
            st.subheader('Impact on open reading frame')
            left, _ = st.columns([1, 1])
            with left:
                st.plotly_chart(testObject.plot_orf(data_diff))