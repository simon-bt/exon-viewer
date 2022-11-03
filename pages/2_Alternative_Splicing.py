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
    testObject = vis_data.SplicingAnalysis(
        data=st.session_state.vastdiff_output[0],
        condition_a=st.session_state.rename_psiA,
        condition_b=st.session_state.rename_psiB,
        color_a=color_a,
        color_b=color_b)

    testObject.diff_threshold = dpsi_value
    udpated_data = testObject.call_diff()

    updated_scatter_plot = testObject.plot_scatter(udpated_data)
    updated_violin_plot = testObject.plot_violin(udpated_data)
    updated_pie_chart = testObject.plot_pie(udpated_data)
    updated_dist_plot = testObject.plot_dist(udpated_data)
    updated_orf_plot = testObject.plot_orf(udpated_data)

    st.session_state.figures.update({'SCATTER_PLOT': updated_scatter_plot})
    st.session_state.figures.update({'VIOLIN_PLOT': updated_violin_plot})
    st.session_state.figures.update({'PIE_CHART': updated_pie_chart})
    st.session_state.figures.update({'DIST_PLOT': updated_dist_plot})
    st.session_state.figures.update({'ORF_PLOT': updated_orf_plot})

with st.sidebar:
    st.subheader('Options')
    color_a = st.color_picker(
        label='Select color for Condition A', value='#008080')
    color_b = st.color_picker(
        label='Select colour for Condition B', value='#800020')
    dpsi_value = st.number_input(label='Select dPSI threshold',
                                 value=0,
                                 min_value=0,
                                 max_value=100)
    button = st.button(label='Update figures', on_click=update_figures)

if not st.session_state.vastdiff_output:
    st.warning('Upload Data!')

else:
    if len(st.session_state.figures) == 0:
        testObject = vis_data.SplicingAnalysis(
            data=st.session_state.vastdiff_output[0],
            condition_a=st.session_state.rename_psiA,
            condition_b=st.session_state.rename_psiB,
            color_a=color_a,
            color_b=color_b)
        data_diff = testObject.call_diff()

        scatter_plot = testObject.plot_scatter(data_diff)
        violin_plot = testObject.plot_violin(data_diff)
        pie_chart = testObject.plot_pie(data_diff)
        dist_plot = testObject.plot_dist(data_diff)
        orf_plot = testObject.plot_orf(data_diff)

        st.session_state.figures.update({'SCATTER_PLOT': scatter_plot})
        st.session_state.figures.update({'VIOLIN_PLOT': violin_plot})
        st.session_state.figures.update({'PIE_CHART': pie_chart})
        st.session_state.figures.update({'DIST_PLOT': dist_plot})
        st.session_state.figures.update({'ORF_PLOT': orf_plot})

    else:
        with page2_container:
            with st.container():
                st.subheader('Alternative splicing profile')
                left, right = st.columns([1, 1])
                with left:
                    st.plotly_chart(st.session_state.figures['SCATTER_PLOT'])
                with right:
                    st.plotly_chart(st.session_state.figures['VIOLIN_PLOT'])

            with st.container():
                st.subheader('Differentially spliced events')
                left, right = st.columns([1, 1])
                with left:
                    st.plotly_chart(st.session_state.figures['PIE_CHART'])
                with right:
                    st.plotly_chart(st.session_state.figures['DIST_PLOT'])

            with st.container():
                st.subheader('Impact on open reading frame')
                left, _ = st.columns([1, 1])
                with left:
                    st.plotly_chart(st.session_state.figures['ORF_PLOT'])
