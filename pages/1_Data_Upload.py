# TODO: Add description

import streamlit as st
import pandas
import sqlite3

st.set_page_config(layout='wide', page_title='Data Upload')
st.header('1. Upload and Process Data')

SPECIES = {
    'Homo_sapiens': 'Hsa',
    'Mus_musculus': 'Mmu',
    'Danio_rerio': 'Dre'
}


# Page 2 Callbacks
def process_data(df: pandas.DataFrame, col_a: str, col_b: str):
    """

    :param df: output from vast-out diff module
    :param col_a: new name for PSI_A column, usually a Control condition
    :param col_b: new name for PSI_A column, usually an Experimental condition
    :return: processed dataframe merged with metadata
    """
    # rename conditions
    data = df.copy().set_index('EventID'). \
        filter(regex=f'{species_code}EX', axis=0). \
        rename(columns={'PSI_A': col_a, 'PSI_B': col_b}). \
        reset_index()
    # define microexons and long exons
    data['ExonType'] = data['Length'].apply(lambda x: 'MIC' if x <= 27 else 'LONG')
    # append to session state
    st.success('Uploaded dataframe!')
    st.balloons()
    st.session_state.vastdiff_output.append(data)


# Page 2 Content
page1_container = st.container()
with page1_container:
    if not st.session_state.vastdiff_output:
        dataframe_path = st.file_uploader('Choose vast-tools diff file',
                                          type=['tab'], )
        selected_species = st.selectbox('Select species',
                                        options=['Homo_sapiens',
                                                 'Mus_musculus',
                                                 'Danio_rerio'])
        species_code = SPECIES[selected_species]
        rename_psiA = st.text_input(label='Specify Condition A name',
                                    value='Control',
                                    placeholder='Control condition')
        rename_psiB = st.text_input(label='Specify Condition B',
                                    placeholder='Experimental  condition name')

        st.session_state.rename_psiA = rename_psiA
        st.session_state.rename_psiB = rename_psiB

        if dataframe_path:
            data_in = pandas. \
                read_csv(dataframe_path, sep='\t'). \
                drop('TYPE', axis=1)

            con = sqlite3.connect("./data/meta.db")
            cur = con.cursor()
            meta_in = pandas.read_sql(f"SELECT * FROM meta WHERE Species = \'{selected_species}\'", con). \
                drop(['index', 'Species'], axis=1)

            data_final = data_in.merge(meta_in, on='EventID', how='left')
            con.close()
            load = st.button('Load dataframe', on_click=process_data,
                             args=(data_final, rename_psiA, rename_psiB))
    else:
        with page1_container:
            st.header('Uploaded dataframe:')
            st.write(st.session_state.vastdiff_output[0])
