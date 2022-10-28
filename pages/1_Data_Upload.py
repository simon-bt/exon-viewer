# TODO: add processing of vast-meta and merge
# TODO: get intronic sequences for exons


import streamlit as st
import pandas


st.set_page_config(layout="wide", page_title="Data Upload")
st.header("Data Upload and Processing")
st.markdown("""
Describe.

""")


# Page 2 Callbacks
def process_data(df: pandas.DataFrame, col_a: str, col_b: str):
    """

    :param df:
    :param col_a:
    :param col_b:
    :return:
    """
    # rename conditions
    data = df.copy().set_index('EventID'). \
        filter(regex='HsaEX', axis=0). \
        rename(columns={'PSI_A': col_a, 'PSI_B': col_b}). \
        reset_index()
    # append to session state
    st.success('Uploaded dataframe!')
    st.balloons()
    st.session_state.vastdiff_output.append(data)

# Page 2 Content
page1_container = st.container()
with page1_container:
    left_col, right_col = st.columns(2)
    if not st.session_state.vastdiff_output:
        with left_col:
            dataframe_path = st.file_uploader('Choose vast-tools diff file',
                                              type=['tab'], )
            rename_psiA = st.text_input(label='Specify Condition A name',
                                        value='Control',
                                        placeholder='Control condition')
            rename_psiB = st.text_input(label='Specify Condition B',
                                        placeholder='Experimental  condition name')
            # min_dpsi = st.number_input(label='Select minimum +/- dPSI threshold',
            #                            min_value=10, max_value=90, )
        if dataframe_path:
            data_in = pandas. \
                read_csv(dataframe_path, sep='\t')
            st.write(data_in.head(10))
            # drop('TYPE', axis=1)
            # meta_in = pandas.\
            #     read_csv('', sep='\t')
            # data_final = pandas.merge([data_in, meta_in], on='EventID', how='left')
            with right_col:
                load = st.button('Load dataframe', on_click=process_data,
                                 args=(data_in, rename_psiA, rename_psiB))
    else:
        with page1_container:
            st.header('Uploaded dataframe:')
            st.write(st.session_state.vastdiff_output[0])
