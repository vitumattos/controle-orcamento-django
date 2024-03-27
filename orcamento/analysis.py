import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go


class Analise:
    def __init__(self, values):
        self.df = pd.DataFrame(values)

        # --Lipeza de dados--
        self.df['periodo'] = pd.to_datetime(self.df['periodo'], format="%d/%m/%Y")
        self.df['valor'] = self.df['valor'].apply(lambda x: float(x))

        self.df_ano = self.df[self.df['periodo'].dt.year == datetime.today().year]

        self.df_mes = self.df[self.df['periodo'] > datetime.today()-timedelta(datetime.today().day)]
        self.df_mes = self.df_mes.sort_values('periodo', ascending=False)
        self.df_mes['valor'] = self.df_mes['valor'].apply(lambda x: float(x))

    def DESPESA_FIXA(self):
        SUM_despesasfixa = self.df_mes[self.df_mes['fixo'] == True].groupby('ordem')['valor'].sum().iloc[0]
        SALARIO = self.df_mes['valor'][self.df_mes['categoria'] == 'Salário'].sum()
        DESPESA_FIXA = round((SUM_despesasfixa/SALARIO)*100, 2)
        return DESPESA_FIXA

    def RENDA_EXTRA(self):
        RENDA_EXTRA = round(self.df_mes[['valor']][(self.df_mes['ordem'] == 'RECEITA') &
                            (self.df_mes['categoria'] != 'Salário')].sum().iloc[0], 2)
        return RENDA_EXTRA

    def PERC_INVESTIMENTO(self):
        SALARIO = self.df_mes['valor'][self.df_mes['categoria'] == 'Salário'].sum()
        TOTAL_investido = self.df_mes[['valor']][self.df_mes['categoria'] == 'Investimento'].sum().iloc[0]
        PERC_INVESTIMENTO = round((TOTAL_investido/SALARIO)*100, 2)
        return PERC_INVESTIMENTO

    def CAIXA(self):
        SUM_receita = self.df_mes[['valor', 'periodo', 'categoria']][self.df_mes['ordem'] == 'RECEITA']
        SUM_despesa = self.df_mes[['valor', 'periodo', 'categoria']][self.df_mes['ordem'] == 'DESPESA']
        SUM_despesa['valor'] = -SUM_despesa['valor']
        CAIXA = round(SUM_receita['valor'].sum() + SUM_despesa['valor'].sum(), 2)
        return CAIXA

     # ---------GRÁFICOS

    def FIG_recebidos(self):
        FIG_recebidos = go.Figure(data=[
            go.Bar(
                x=self.df_ano[self.df_ano['ordem'] == 'RECEITA'].groupby('categoria')['valor'].sum().index,
                y=self.df_ano[self.df_ano['ordem'] == 'RECEITA'].groupby('categoria')['valor'].sum().values,
                name='Recebimentos',
                text=self.df_ano[self.df_ano['ordem'] == 'RECEITA'].groupby('categoria')['valor'].sum().values
            )])

        FIG_recebidos.update_traces(marker_color='rgb(158,202,225)',
                                    marker_line_color='rgb(8,48,107)',
                                    marker_line_width=1.5,
                                    opacity=0.6,
                                    textfont_size=14,
                                    textangle=0,
                                    textposition="outside",
                                    cliponaxis=False,
                                    texttemplate='%{text:.2s}'
                                    )
        FIG_recebidos.update_layout(title={
            'text': 'Recebimentos',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'color': 'white'}
        })
        FIG_recebidos.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=25, b=0),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),

        )
        return FIG_recebidos

    def FIG_acumulo(self):
        SUM_receita = self.df_mes[['valor', 'periodo', 'categoria']][self.df_mes['ordem'] == 'RECEITA']
        SUM_despesa = self.df_mes[['valor', 'periodo', 'categoria']][self.df_mes['ordem'] == 'DESPESA']
        SUM_despesa['valor'] = -SUM_despesa['valor']

        df_acumulo = pd.concat([SUM_despesa, SUM_receita]).sort_values('periodo')
        df_acumulo = df_acumulo.groupby('periodo').sum().cumsum()
        FIG_acumulo = go.Figure(data=[
            go.Scatter(
                x=df_acumulo.reset_index()['periodo'].dt.strftime('%d-%b'),
                y=df_acumulo['valor'],
                name='Acumulo',
                mode='lines',
                line=dict(color='rgb(158,202,225)'),
                fill='tozeroy'
            )])
        FIG_acumulo.update_layout(title={
            'text': 'Acumulado mensal',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'color': 'white'}
        })
        FIG_acumulo.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=25, b=0),
            xaxis=dict(showgrid=False, tickformat='%d-%b-%y'),
            yaxis=dict(showgrid=False),

        )
        return FIG_acumulo

    def FIG_meta(self):
        # ---------GRÁFICO META + Percentual Mensal do Salário Investido
        df_investido_por_mes = self.df_ano.copy()
        df_investido_por_mes['Ano_Mes'] = df_investido_por_mes['periodo'].dt.to_period('M')
        df_salario_por_mes = df_investido_por_mes[df_investido_por_mes['categoria'] == 'Salário'].groupby('Ano_Mes')[
            'valor'].sum()
        df_investido_por_mes = df_investido_por_mes[
            df_investido_por_mes['categoria'] == 'Investimento'].groupby('Ano_Mes')['valor'].sum()
        percentual_investido_por_mes = round((df_investido_por_mes / df_salario_por_mes) * 100, 2)

        FIG_meta = go.Figure(data=[
            go.Bar(
                x=percentual_investido_por_mes.index.strftime('%b-%y'),
                y=percentual_investido_por_mes.values,
                name='% Investido'
            ),
            go.Scatter(
                x=percentual_investido_por_mes.index.strftime('%b-%y'),
                y=[30]*12,
                name='Meta'
            )
        ])
        FIG_meta.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                               marker_line_width=1.5, opacity=0.6)
        FIG_meta.update_layout(title={
            'text': 'Percentual Mensal do Salário Investido',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'color': 'white'}
        })
        FIG_meta.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=25, b=0),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )
        return FIG_meta

    def FIG_despesas(self):
        SUM_despesa = self.df_mes[['valor', 'periodo', 'categoria']][self.df_mes['ordem'] == 'DESPESA']
        SUM_despesa['valor'] = -SUM_despesa['valor']

        FIG_despesas = go.Figure(data=[
            go.Pie(
                labels=SUM_despesa.groupby('categoria')['valor'].sum().index.to_list(),
                values=(-SUM_despesa.groupby('categoria')['valor'].sum()).to_list(),
                hole=0.5,
                showlegend=False,
            )])
        FIG_despesas.update_layout(title={
            'text': 'Total de Despesas',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'color': 'white'}
        })
        FIG_despesas.update_traces(hoverinfo='value+percent+label',
                                   textinfo='percent', textfont_size=10,
                                   textposition='inside',
                                   marker=dict(
                                       line=dict(color='rgb(158,202,225)',
                                                 width=2)))
        FIG_despesas.update_layout(uniformtext_minsize=12,
                                   uniformtext_mode='hide')
        FIG_despesas.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=25, b=5),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )
        return FIG_despesas

    def FIG_receita_despesa(self):
        SUM_receita = self.df_ano[['valor', 'periodo', 'categoria']][self.df_ano['ordem'] == 'RECEITA']
        SUM_receita['Ano_Mes'] = SUM_receita['periodo'].dt.to_period('M')
        groupby_SUM_receita = SUM_receita.groupby('Ano_Mes')['valor'].sum()

        SUM_despesa = self.df_ano[['valor', 'periodo', 'categoria']][self.df_ano['ordem'] == 'DESPESA']
        SUM_despesa['Ano_Mes'] = SUM_despesa['periodo'].dt.to_period('M')
        groupby_SUM_despesa = SUM_despesa.groupby('Ano_Mes')['valor'].sum()
        # import pdb
        # pdb.set_trace()

        # ------------GRÁFICO RECEITA x DESPESAS
        FIG_receita_despesa = go.Figure(data=[
            go.Bar(
                x=groupby_SUM_receita.index.strftime('%b-%y'),
                y=groupby_SUM_receita.values,
                name='Receita',
                marker_color='rgb(158,202,225)'
            ),
            go.Bar(
                x=groupby_SUM_despesa.index.strftime('%b-%y'),
                y=groupby_SUM_despesa.values,
                name='Despesa',
                marker_color='rgb(8,48,107)'
            ),

            go.Scatter(
                x=groupby_SUM_receita.index.strftime('%b-%y'),
                y=(groupby_SUM_despesa.values / groupby_SUM_receita.values)*2500,
                name='% Comprometido',
            )
        ]
        )
        FIG_receita_despesa.update_layout(title={
            'text': 'Receitas x Despesas',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'color': 'white'}
        })
        FIG_receita_despesa.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=25, b=0),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )

        return FIG_receita_despesa

    def FIG_despesas_mes(self):

        # Subistituir pelo df ano
        FIG_despesas_mes = go.Figure(data=[])

        SUM_despesa = self.df[['valor', 'periodo', 'categoria']][self.df['ordem'] == 'DESPESA']
        SUM_despesa['Ano_Mes'] = SUM_despesa['periodo'].dt.to_period('M').astype(str)

        groupby_SUM_despesa = SUM_despesa.groupby(['categoria', 'Ano_Mes'])['valor'].sum().reset_index()

        for categoria in groupby_SUM_despesa['categoria'].unique():
            df_categoria = groupby_SUM_despesa[groupby_SUM_despesa['categoria'] == categoria]

            FIG_despesas_mes.add_traces(
                go.Bar(
                    x=df_categoria['Ano_Mes'],
                    y=df_categoria['valor'],
                    name=categoria
                )
            )

        FIG_despesas_mes.update_layout(title={
            'text': 'Despesa Mês a Mês',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'color': 'white'}
        },
            barmode='stack')
        FIG_despesas_mes.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=25, b=0),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )

        # import pdb
        # pdb.set_trace()

        return FIG_despesas_mes
