import pandas
import numpy
import plotly.express as px
import plotly.graph_objects as go

FIG_TEMPLATE = dict(
    layout=go.Layout(
        autosize=False,
        width=550,
        height=550,
        title_font=dict(family="Helvetica", size=18),
        font=dict(family='Helvetica', size=18, color='#1e2125'),
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(nticks=10),
        yaxis=dict(nticks=10),
        legend=dict(x=1.1, y=1, orientation="v", xanchor='auto', yanchor='auto')
    )
)


class SplicingAnalysis:
    """
    Description.
    """

    def __init__(self,
                 data: pandas.DataFrame,
                 condition_a: str,
                 condition_b: str,
                 color_a: str,
                 color_b: str,
                 color_mic: str,
                 color_long: str,
                 color_nonreg: str,
                 color_reg: str):
        self.data = data
        self.condition_a = condition_a
        self.condition_b = condition_b
        self.diff_threshold = 10
        self.color_a = color_a
        self.color_b = color_b
        self.color_mic = color_mic
        self.color_long = color_long
        self.color_nonreg = color_nonreg
        self.color_reg = color_reg

    @property
    def diff_threshold(self):
        return self._diff_threshold

    @diff_threshold.setter
    def diff_threshold(self, diff_threshold):
        self._diff_threshold = diff_threshold

    def call_diff(self):
        data_diff = self.data.copy()
        data_diff['DIFF'] = data_diff['dPSI']. \
            apply(lambda x: 'Yes' if abs(x) >= self.diff_threshold else 'No')
        return data_diff

    def plot_scatter(self, df: pandas.DataFrame):
        global FIG_TEMPLATE
        fig_scatter = px.scatter(df,
                                 x=self.condition_a,
                                 y=self.condition_b,
                                 color='DIFF',
                                 hover_data=df.columns,
                                 color_discrete_sequence=[self.color_nonreg, self.color_reg],
                                 labels={'DIFF': 'Regulated'})
        fig_scatter.update_layout(
            template=FIG_TEMPLATE,
            xaxis=dict(title=f'{self.condition_a} PSI [%]'),
            yaxis=dict(title=f'{self.condition_b} PSI [%]'),
            showlegend=True,
            legend=dict(x=0.5, y=1.15, orientation="h", xanchor='auto', yanchor='auto'),
            margin=dict(pad=0, l=100, r=10, b=100, t=10)
        )
        fig_scatter.update_xaxes(showgrid=False, ticks="outside", ticklen=10, tickwidth=2, showline=True,
                                 linecolor='black', tickcolor='black', mirror=True, linewidth=2,
                                 zeroline=False)
        fig_scatter.update_yaxes(ticks="outside", ticklen=10, tickwidth=2, showline=True,
                                 linecolor='black', tickcolor='black', mirror=True, linewidth=2,
                                 zeroline=False, showgrid=False)
        fig_scatter.update_traces(marker=dict(size=9,
                                              line=dict(width=2, color=True)),
                                  selector=dict(mode='markers'),
                                  opacity=0.6)
        fig_scatter.add_shape(type="line",
                              x0=0.5, y0=0, x1=100, y1=100,
                              line=dict(color="lightgrey", width=2))
        return fig_scatter


    def plot_pie(self, df: pandas.DataFrame):
        data_diff_truly = df.query('DIFF == \'Yes\'')
        counts_diff = dict(data_diff_truly['EXON_TYPE']. \
                           value_counts())
        fig_pie = go.Figure(data=[go.Pie(labels=['MIC', 'LONG'],
                                         values=[counts_diff['MIC'], counts_diff['LONG']],
                                         )])
        fig_pie.update_traces(
            hoverinfo='label+percent',
            textinfo='value',
            textfont_size=40,
            marker=dict(colors=[self.color_mic, self.color_long],
                        line=dict(color='#000000', width=4)))
        fig_pie.update_layout(
            template=FIG_TEMPLATE,
            legend=dict(x=1.3, y=0.9, orientation="v", xanchor='auto', yanchor='auto'),
            margin=dict(l=100, r=10, b=50, t=10, pad=0)
        )
        return fig_pie

    def plot_dist(self, df: pandas.DataFrame):
        __mic_data = df.query('EXON_TYPE == \'MIC\'')['dPSI']
        __long_data = df.query('EXON_TYPE == \'LONG\'')['dPSI']
        __cumsum_mic = numpy.cumsum(abs(__mic_data))
        __cumsum_long = numpy.cumsum(abs(__long_data))

        fig_cumsum = go.Figure()
        fig_cumsum.add_trace(
            go.Scatter(y=sorted(__mic_data),
                       x=1. * numpy.arange(len(__cumsum_mic)) / (len(__cumsum_mic) - 1),
                       mode='lines',
                       name='MIC',
                       line=dict(color=self.color_mic, width=5))

        )
        fig_cumsum.add_trace(
            go.Scatter(y=sorted(__long_data),
                       x=1. * numpy.arange(len(__cumsum_long)) / (len(__cumsum_long) - 1),
                       mode='lines',
                       name='LONG',
                       line=dict(color=self.color_long, width=5))

        )
        fig_cumsum.update_layout(
            template=FIG_TEMPLATE,
            yaxis=dict(title=r'Change in inclusion [dPSI]'),
            xaxis=dict(title=r'Proportion'),
            legend=dict(x=0.5, y=1.15, orientation="h", xanchor='auto', yanchor='auto'),
            margin=dict(l=100, r=10, b=60, t=0, pad=5)
        )
        fig_cumsum.update_xaxes(showgrid=False, ticks="outside", ticklen=5, tickwidth=2, showline=True,
                                linecolor='black', tickcolor='black', mirror=True, linewidth=2,
                                zeroline=False)
        fig_cumsum.update_yaxes(showgrid=False, ticks="outside", ticklen=5, tickwidth=2, showline=True,
                                linecolor='black', tickcolor='black', mirror=True, linewidth=2,
                                zeroline=False)
        return fig_cumsum

    @staticmethod
    def plot_orf(df: pandas.DataFrame):
        __orf_data = df.copy()
        __mapping = {
            'CDS_PROT': 'ORF-preserving',
            'CDS_uncertain': 'ORF-preserving',
            'CDS_DISR_uEXC': 'ORF-disrupting',
            'CDS_DISR_uINC': 'ORF-disrupting',
            'UTR_5': '5/3 UTR',
            'UTR_3': '5/3 UTR',
            'NonCoding': 'Non-coding'
        }
        __orf_data['ORF_ONTO'] = __orf_data['ORF_IMPACT']. \
            map(__mapping)
        __orf_data = __orf_data[~__orf_data['ORF_ONTO'].isna()]. \
            query('DIFF == \'Yes\'')
        __exon_info = dict(__orf_data['EXON_TYPE'].value_counts())

        __onto_counts = pandas.DataFrame(__orf_data. \
                                         groupby('EXON_TYPE')['ORF_ONTO']. \
                                         value_counts()). \
            rename(columns={'ORF_ONTO': 'COUNT'}). \
            reset_index()
        __onto_counts['N_EXONS'] = __onto_counts['EXON_TYPE'].map(__exon_info)
        __onto_counts['PCT'] = __onto_counts. \
            apply(lambda x: round(x['COUNT'] * 100 / x['N_EXONS'], 2), axis=1)

        fig_orf = px.bar(__onto_counts, x="EXON_TYPE", y="PCT", color="ORF_ONTO",
                         category_orders={'EXON_TYPE': ['LONG', 'MIC']},
                         labels={'ORF_ONTO': 'Impact on ORF'})

        fig_orf.update_layout(
            template=FIG_TEMPLATE,
            xaxis=dict(title='Exon Type'),
            yaxis=dict(title='% of Events'),
            width=600,
            height=500,
            legend=dict(x=1.6, y=1.05, orientation="v", xanchor='auto', yanchor='auto'),
            margin=dict(l=100, r=10, b=60, t=10, pad=5))

        fig_orf.update_xaxes(showgrid=False, ticks="outside", ticklen=5, tickwidth=2, showline=True,
                             linecolor='black', tickcolor='black', mirror=True, linewidth=2,
                             zeroline=False)
        fig_orf.update_yaxes(showgrid=False, ticks="outside", ticklen=5, tickwidth=2, showline=True,
                             linecolor='black', tickcolor='black', mirror=True, linewidth=2,
                             zeroline=False)
        return fig_orf


    def plot_violin(self, df: pandas.DataFrame):
        __data_melt = df. \
            query('DIFF == \'Yes\''). \
            melt(id_vars=['EventID', 'EXON_TYPE', 'dPSI', 'GENE', 'ENSEMBL_ID', 'ORF_IMPACT'],
                 value_vars=[self.condition_a, self.condition_b],
                 value_name='PSI',
                 var_name='CONDITION')

        __df_a = __data_melt.query(f'CONDITION == \'{self.condition_a}\'')
        __df_b = __data_melt.query(f'CONDITION == \'{self.condition_b}\'')

        show_legend = [True, False, False, False]
        pointpos_a = [-1.2, -0.6,
                      -0.6, -0.3]
        pointpos_b = [1.1, 0.7,
                      1, 1]

        fig_violin = go.Figure()
        for i in range(0, 2):
            fig_violin.add_trace(
                go.Violin(x=__df_a['EXON_TYPE'][(__df_a['EXON_TYPE'] == pandas.unique(__df_a['EXON_TYPE'])[i])],
                          y=__df_a['PSI'][(__df_a['EXON_TYPE'] == pandas.unique(__df_a['EXON_TYPE'])[i])],
                          legendgroup=self.condition_a, scalegroup=self.condition_a, name=self.condition_a,
                          side='negative',
                          pointpos=pointpos_a[i],
                          line_color=self.color_a,
                          showlegend=show_legend[i])
            )
            fig_violin.add_trace(
                go.Violin(x=__df_b['EXON_TYPE'][(__df_b['EXON_TYPE'] == pandas.unique(__df_b['EXON_TYPE'])[i])],
                          y=__df_b['PSI'][(__df_b['EXON_TYPE'] == pandas.unique(__df_b['EXON_TYPE'])[i])],
                          legendgroup=self.condition_b, scalegroup=self.condition_b, name=self.condition_b,
                          side='positive',
                          pointpos=pointpos_b[i],
                          line_color=self.color_b,
                          showlegend=show_legend[i])
            )

        fig_violin.update_layout(
            template=FIG_TEMPLATE,
            violingap=0,
            violingroupgap=0.3,
            violinmode='overlay',
            yaxis=dict(title='PSI [%]'),
            xaxis=dict(title='Exon Type'),
            width=600,
            height=500,
            legend=dict(x=0.5, y=1.15, orientation="h", xanchor='auto', yanchor='auto'),
            margin=dict(l=100, r=10, b=60, t=10, pad=5))
        fig_violin.update_traces(meanline_visible=True,
                                 points='all',
                                 jitter=0.1,
                                 scalemode='count')
        fig_violin.update_xaxes(showgrid=False, ticks="outside", ticklen=5, tickwidth=2, showline=True,
                                linecolor='black', tickcolor='black', mirror=True, linewidth=2,
                                zeroline=False)
        fig_violin.update_yaxes(showgrid=False, ticks="outside", ticklen=5, tickwidth=2, showline=True,
                                linecolor='black', tickcolor='black', mirror=True, linewidth=2,
                                zeroline=False, nticks=10, range=[-15, 115])
        return fig_violin
