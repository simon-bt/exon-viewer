import streamlit as st
import pandas


def process_data(df: pandas.DataFrame):
    df_temp = df.copy()
    df_temp.drop(remove_columns, axis=1, inplace=True)

    df_wt = data_temp.query('TYPE == \'WT\'').\
        rename(columns={'PSI': 'PSI_WT'}). \
        set_index(['EVENT', 'VARIANT', 'CONDITION', 'SENSITIVITY']).filter(regex='PSI_'). \
        reset_index()
    df_wt_temp = data_temp.query('TYPE == \'WT\'')
    df_wt_temp['dPSI_REL'] = 0
    df_wt_temp['PSI_WT'] = df_wt_temp['PSI']

    df_vars = data_temp.query('TYPE == \'VAR\'')
    df_vars_dpsi = df_vars. \
        merge(df_wt.drop('VARIANT', axis=1), on=['EVENT', 'CONDITION', 'SENSITIVITY'])
    df_vars_dpsi['dPSI_REL'] = round(df_vars_dpsi['PSI'] - df_vars_dpsi['PSI_WT'], 2)
    df_final = pandas.concat([df_wt_temp.query('TYPE == \'WT\''), df_vars_dpsi])

    st.success('Uploaded dataframe!')
    st.session_state.inclusion_table.append(df_final)