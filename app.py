import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

all_df = pd.read_csv('stats.csv')
df_sel = all_df[['Div',
                 'Date',
                 'HomeTeam',
                 'AwayTeam',
                 'FTHG',
                 'FTAG',
                 'FTR',
                 'HS',
                 'AS',
                 'HST',
                 'AST',
                 'HHW',
                 'AHW',
                 'HC',
                 'AC',
                 'HF',
                 'AF',
                 'HO',
                 'AO',
                 'HY',
                 'AY',
                 'HR',
                 'AR', 'season']]
df_sel.columns = [
    'Div',
    'Date', 'HomeTeam',
    'AwayTeam',
    'Gols Local',
    'Gols Visitant',
    'Guanyador',
    'Chuts Local',
    'Chuts Visitant',
    'Chuts a porteria Local',
    'Chuts a porteria Visitant',
    'Chuts al pal Local',
    'Chuts al pal Visitant',
    'Corners Local',
    'Corners Visitant',
    'Faltes comeses Local',
    'Faltes comeses Visitant',
    'Fores de joc Local',
    'Fores de joc Visitant',
    'Targetes grogues Local',
    'Targetes grogues Visitant',
    'Targetes vermelles Local',
    'Targetes vermelles Visitant', 'season'
]

df_casa = df_sel[
    ['Div', 'Date', 'season', 'Guanyador', 'HomeTeam'] + [x for x in df_sel.columns if 'Local' in x]].rename(
    columns={x: x[:-6] for x in df_sel.columns if 'Local' in x}).rename(
    columns={'HomeTeam': 'Equip'}
)
df_casa['loc'] = 'Local'

df_vis = df_sel[
    ['Div', 'Date', 'season', 'Guanyador', 'AwayTeam'] + [x for x in df_sel.columns if 'Visitant' in x]].rename(
    columns={x: x[:-9] for x in df_sel.columns if 'Visitant' in x}).rename(
    columns={'AwayTeam': 'Equip'}
)
df_vis['loc'] = 'Visitant'
df_sel_form = df_casa.append(df_vis)

# df = df_sel.groupby(['Div', 'season'])[['FTHG', 'FTAG']].mean().stack().reset_index()
# df = df.rename(columns={'level_2': 'Indicator Name', 0: 'Value'})

available_indicators = df_sel_form.columns.drop(['Div', 'Date', 'season', 'Guanyador', 'Equip', 'loc'])

app.layout = html.Div([
    html.H1("Comparativa de les estadístiques dels equips de les lligues Espanyola, Italiana i Anglesa entre les temporades 93/94 i 20/21",
            style={'width': '80%', 'margin': 'auto'}),
    html.Plaintext("""En aquesta visutalització es presenten una sèrie d'estadístiques de tots els equips que han participat en la primera divisió d'Espanya, Itàlia i Anglaterra entre les temporades 93/94 i 20/21"""
                   ,style={'with':'60%', 'margin-left':'20%','margin-right':'20%', 'text-align':'center'}),
    html.Plaintext("""Les dades es poden visualitzar com a mitjana per partit, o valor agregats per al periode observat. """
                   ,style={'with':'60%', 'margin-left':'20%','margin-right':'20%', 'text-align':'center'}),
    html.Plaintext("""La sèrie temporal pot mostrar les dades per a tots els equipes que van jugar a primera divisió cada temporada, o es poden seleccionar equips de manera individual"""
                   ,style={'with':'60%', 'margin-left':'20%','margin-right':'20%', 'text-align':'center'}),
    html.Plaintext("""Els gràfics de la part inferior mostren, per a cada lliga, un rànking basat en l'estadístic seleccionat"""
                   ,style={'with':'60%', 'margin-left':'20%','margin-right':'20%', 'text-align':'center'}),

    html.Div([
    html.Div([
        #html.Div(children='Selecciona si vols visualitzar valors per a equips locals, visitats, o ambdós',
        #         style={
        #             'textAlign': 'left'
        #         }),
        #dcc.RadioItems(
        #    id='crossfilter-indicators-type',
        #    options=[{'label': i, 'value': i} for i in ['Local', 'Visitant', 'Tots']],
        #    value='Tots',
        #    labelStyle={'display': 'inline-block'}
        #),        html.Br(),
        # , style = {'width': '49%', 'padding': '0px 20px 20px 20px'}
    ]),
    html.Div([
        html.Div(children='Selecciona una variable a analitzar',
                 style={
                     'textAlign': 'left'
                 }),
        dcc.Dropdown(
            id='crossfilter-indicators',
            options=[{'label': i, 'value': i} for i in available_indicators],
            value='Gols'
        ),html.Br(),
        html.Div(children='Selecciona si vols visualitzar valors mitjans o valors totals (agregats)',
                 style={
                     'textAlign': 'left'
                 }),
        dcc.RadioItems(
            id='crossfilter-sum-type',
            options=[{'label': i, 'value': i} for i in ['Valors Mitjans', 'Valors Totals']],
            value='Valors Mitjans',
            labelStyle={'display': 'inline-block'}
        ),
        html.Br(),
        html.Div(children='Selecciona l\'interval d\'anys que vols visualitzar',
                 style={
                     'textAlign': 'left'
                 }),
        dcc.RangeSlider(
            id='crossfilter-year--slider',
            min=0,  # df['Year'].min(),
            max=len(df_sel_form['season'].unique()) - 1,  # df['Year'].max(),
            value=[0, len(df_sel_form['season'].unique())],  # df['Year'].max(),
            marks={num: str(season) for num, season in enumerate(
                [x for x in sorted(df_sel_form['season'].unique()) if x[0] == '9'] + [x for x in sorted(
                    df_sel_form['season'].unique()) if
                                                                                      x[0] != '9']
            )},
            step=1
        )]),
    html.Div([

        html.Div([
            html.Div(children='Lliga Espanyola',
                     style={
                         'textAlign': 'center'
                     }),
            dcc.Dropdown(
                id='crossfilter-spain',
                options=[{'label': i, 'value': i} for i in ['Tots els equips'] + sorted(
                    [x for x in all_df[all_df['Div'] == 'SP1']['HomeTeam'].unique()])],
                value='Tots els equips'
            )
        ],
            style={'width': '30%', 'display': 'inline-block'}),

        html.Div([html.Div(children='Lliga Italiana',
                           style={
                               'textAlign': 'center'
                           }),
                  dcc.Dropdown(
                      id='crossfilter-italy',
                      options=[{'label': i, 'value': i} for i in ['Tots els equips'] + sorted(
                          [x for x in all_df[all_df['Div'] == 'I1']['HomeTeam'].unique()])],
                      value='Tots els equips'
                  ),
                  ],
                 style={'width': '30%', 'float': 'center', 'display': 'inline-block'}),

        html.Div([html.Div(children='Lliga Anglesa',
                           style={
                               'textAlign': 'center'
                           }),
                  dcc.Dropdown(
                      id='crossfilter-england',
                      options=[{'label': i, 'value': i} for i in ['Tots els equips'] + sorted(
                          [x for x in all_df[all_df['Div'] == 'E0']['HomeTeam'].unique()])],
                      value='Tots els equips'
                  ),
                  ], style={'width': '30%',
                            # 'float': 'right',
                            'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),
        html.Br(),

    html.Div([
        dcc.Graph(
            id='plot-all-leagues',
            # hoverData={'points': [{'customdata': 'Japan'}]}
        )
    ], style={'width': '90%', 'display': 'inline-block', 'padding': '0 20'}
    ),
    html.Div([
        dcc.Graph(id='y-spain-series'),
    ], style={'display': 'inline-block', 'width': '30%'}),
    html.Div([
        dcc.Graph(id='y-italy-series'),
    ], style={'display': 'inline-block', 'width': '30%'}),
    html.Div([
        dcc.Graph(id='y-england-series'),
    ], style={'display': 'inline-block', 'width': '30%'}),
], style={'width': '80%', 'margin': 'auto'},)])


@app.callback(
    dash.dependencies.Output('plot-all-leagues', 'figure'),
    [dash.dependencies.Input('crossfilter-year--slider', 'value'),
     dash.dependencies.Input('crossfilter-indicators', 'value'),
     dash.dependencies.Input('crossfilter-spain', 'value'),
     dash.dependencies.Input('crossfilter-italy', 'value'),
     dash.dependencies.Input('crossfilter-england', 'value'),
     dash.dependencies.Input('crossfilter-sum-type', 'value'),

     ])
def update_graph(year_value, variable, crossfilter_spain,
                 crossfilter_italy, crossfilter_england,
                 sum_ave):
    dict_season = {
        0: '93/94',
        1: '94/95',
        2: '95/96',
        3: '96/97',
        4: '97/98',
        5: '98/99',
        6: '99/00',
        7: '00/01',
        8: '01/02',
        9: '02/03',
        10: '03/04',
        11: '04/05',
        12: '05/06',
        13: '06/07',
        14: '07/08',
        15: '08/09',
        16: '09/10',
        17: '10/11',
        18: '11/12',
        19: '12/13',
        20: '13/14',
        21: '14/15',
        22: '15/16',
        23: '16/17',
        24: '17/18',
        25: '18/19',
        26: '19/20',
        27: '20/21'
    }
    ori_year_value = year_value

    year_value[1] = min(year_value[1] + 1, len(df_sel_form['season'].unique()))

    if crossfilter_spain == 'Tots els equips':
        dff_spain = df_sel_form[
            (df_sel_form['season'].isin([dict_season[x] for x in range(*year_value)]))
            &
            (df_sel_form['Div'] == 'SP1')
            ].copy()
    elif crossfilter_spain != 'Tots els equips':
        dff_spain = df_sel_form[
            (df_sel_form['season'].isin([dict_season[x] for x in range(*year_value)]))
            &
            (df_sel_form['Div'] == 'SP1')
            &
            (df_sel_form['Equip'] == crossfilter_spain)
            ].copy()

    if crossfilter_italy == 'Tots els equips':
        dff_italy = df_sel_form[
            (df_sel_form['season'].isin([dict_season[x] for x in range(*year_value)]))
            &
            (df_sel_form['Div'] == 'I1')
            ].copy()
    elif crossfilter_italy != 'Tots els equips':
        dff_italy = df_sel_form[
            (df_sel_form['season'].isin([dict_season[x] for x in range(*year_value)]))
            &
            (df_sel_form['Div'] == 'I1')
            &
            (df_sel_form['Equip'] == crossfilter_italy)
            ].copy()

    if crossfilter_england == 'Tots els equips':
        dff_england = df_sel_form[
            (df_sel_form['season'].isin([dict_season[x] for x in range(*year_value)]))
            &
            (df_sel_form['Div'] == 'E0')
            ].copy()
    elif crossfilter_england != 'Tots els equips':
        dff_england = df_sel_form[
            (df_sel_form['season'].isin([dict_season[x] for x in range(*year_value)]))
            &
            (df_sel_form['Div'] == 'E0')
            &
            (df_sel_form['Equip'] == crossfilter_england)
            ].copy()

    dff = dff_spain.append(
        dff_italy
    ).append(
        dff_england).reset_index(drop=True)
    dff[variable] = dff[variable]

    if sum_ave == 'Valors Mitjans':
        dff = dff.groupby(['season', 'Div'], as_index=False).mean()
    else:
        dff = dff.groupby(['season', 'Div'], as_index=False).sum()

    dff['season'] = dff['season'].map({a: b for b, a in dict_season.items()})
    dff.sort_values(['season', 'Div'], inplace=True)
    dff['season'] = dff['season'].map(dict_season)
    if crossfilter_spain == 'Tots els equips':
        dff.loc[dff['Div'] == 'SP1', 'Div'] = 'Lliga Espanyola'
    else:
        dff.loc[dff['Div'] == 'SP1', 'Div'] = crossfilter_spain
    if crossfilter_italy == 'Tots els equips':
        dff.loc[dff['Div'] == 'I1', 'Div'] = 'Lliga Italiana'
    else:
        dff.loc[dff['Div'] == 'I1', 'Div'] = crossfilter_italy
    if crossfilter_england == 'Tots els equips':
        dff.loc[dff['Div'] == 'E0', 'Div'] = 'Lliga Anglesa'
    else:
        dff.loc[dff['Div'] == 'E0', 'Div'] = crossfilter_england

    fig = px.line(dff,
                  x='season',
                  y=variable,
                  color='Div')
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x")
    fig.update_layout(legend_title_text='Lliga / Equip',
                      title='Evolució de {} entre les temporades {} i {}'.format(
                          variable, dict_season[int(ori_year_value[0])], dict_season[int(ori_year_value[1] - 1)]
                      ),
                      xaxis_title='Temporada')
    y_maxs = []
    for trace_data in fig.data:
        y_maxs.append(max(trace_data.y))
    y_max = max(y_maxs) * 1.1
    fig.update_layout(yaxis=dict(range=[0, y_max]))
    if sum_ave == 'Valors Mitjans':
        fig.update_layout(yaxis_title='{} (Mitjana per partit)'.format(variable))
    else:
        fig.update_layout(yaxis_title='{} (Total)'.format(variable))
    return fig


@app.callback(
    dash.dependencies.Output('y-spain-series', 'figure'),
    [dash.dependencies.Input('crossfilter-year--slider', 'value'),
     dash.dependencies.Input('crossfilter-indicators', 'value'),
     dash.dependencies.Input('crossfilter-spain', 'value'),
     dash.dependencies.Input('crossfilter-sum-type', 'value'),
     ])
def update_graph(year_value, variable, crossfilter_spain, sum_ave):
    dict_season = {
        0: '93/94',
        1: '94/95',
        2: '95/96',
        3: '96/97',
        4: '97/98',
        5: '98/99',
        6: '99/00',
        7: '00/01',
        8: '01/02',
        9: '02/03',
        10: '03/04',
        11: '04/05',
        12: '05/06',
        13: '06/07',
        14: '07/08',
        15: '08/09',
        16: '09/10',
        17: '10/11',
        18: '11/12',
        19: '12/13',
        20: '13/14',
        21: '14/15',
        22: '15/16',
        23: '16/17',
        24: '17/18',
        25: '18/19',
        26: '19/20',
        27: '20/21'
    }

    year_value[1] = min(year_value[1] + 1, len(df_sel_form['season'].unique()))

    if sum_ave == 'Valors Mitjans':
        df = df_sel_form[
                 (df_sel_form['season'].isin([dict_season[x] for x in range(*year_value)]))
                 &
                 (df_sel_form['Div'] == 'SP1')
                 ].groupby('Equip').mean()[[variable]].dropna().sort_values(variable)
    else:
        df = df_sel_form[
                 (df_sel_form['season'].isin([dict_season[x] for x in range(*year_value)]))
                 &
                 (df_sel_form['Div'] == 'SP1')
                 ].groupby('Equip').sum()[[variable]].dropna().sort_values(variable)
    df.reset_index(inplace=True)
    if (crossfilter_spain != "Tots els equips") and (crossfilter_spain not in df.iloc[-7:]['Equip'].unique()):
            df_toplot = df.iloc[-6:].append(df[df['Equip'] == crossfilter_spain])
            afegit = True
    else:
        df_toplot = df.iloc[-7:]
        afegit=False
    fig = px.bar(df_toplot, y="Equip", x=variable, orientation='h')
    fig.update_traces(marker_color='#01c58a')

    if afegit:
        fig.update_layout(title='Top-6 + {} en {} a Espanya'.format(crossfilter_spain, variable))
    else:
        fig.update_layout(title='Top-7 en {} a Espanya'.format(variable))
    if sum_ave == 'Valors Mitjans':
        fig.update_layout(xaxis_title='{} (Mitjana per partit)'.format(variable))
    else:
        fig.update_layout(xaxis_title='{} (Total)'.format(variable))
    return fig


@app.callback(
    dash.dependencies.Output('y-italy-series', 'figure'),
    [dash.dependencies.Input('crossfilter-year--slider', 'value'),
     dash.dependencies.Input('crossfilter-indicators', 'value'),
     dash.dependencies.Input('crossfilter-italy', 'value'),
     dash.dependencies.Input('crossfilter-sum-type', 'value'),
     ])
def update_graph(year_value, variable, crossfilter_italy, sum_ave):
    dict_season = {
        0: '93/94',
        1: '94/95',
        2: '95/96',
        3: '96/97',
        4: '97/98',
        5: '98/99',
        6: '99/00',
        7: '00/01',
        8: '01/02',
        9: '02/03',
        10: '03/04',
        11: '04/05',
        12: '05/06',
        13: '06/07',
        14: '07/08',
        15: '08/09',
        16: '09/10',
        17: '10/11',
        18: '11/12',
        19: '12/13',
        20: '13/14',
        21: '14/15',
        22: '15/16',
        23: '16/17',
        24: '17/18',
        25: '18/19',
        26: '19/20',
        27: '20/21'
    }
    year_value[1] = min(year_value[1] + 1, len(df_sel_form['season'].unique()))
    if sum_ave == 'Valors Mitjans':

        df = df_sel_form[
                 (df_sel_form['season'].isin([dict_season[x] for x in range(*year_value)]))
                 &
                 (df_sel_form['Div'] == 'I1')
                 ].groupby('Equip').mean()[[variable]].dropna().sort_values(variable)
    else:
        df = df_sel_form[
                 (df_sel_form['season'].isin([dict_season[x] for x in range(*year_value)]))
                 &
                 (df_sel_form['Div'] == 'I1')
                 ].groupby('Equip').sum()[[variable]].dropna().sort_values(variable)

    df.reset_index(inplace=True)
    if (crossfilter_italy != "Tots els equips") and (crossfilter_italy not in df.iloc[-7:]['Equip'].unique()):
        df_toplot = df.iloc[-6:].append(df[df['Equip'] == crossfilter_italy])
        afegit = True
    else:
        df_toplot = df.iloc[-7:]
        afegit=False
    fig = px.bar(df_toplot, y="Equip", x=variable, orientation='h')
    fig.update_traces(marker_color='#ed4b34')
    if afegit:
        fig.update_layout(title='Top-6 + {} en {} a Italia'.format(crossfilter_italy, variable))
    else:
        fig.update_layout(title='Top-7 en {} a Italia'.format(variable))
    if sum_ave == 'Valors Mitjans':
        fig.update_layout(xaxis_title='{} (Mitjana per partit)'.format(variable))
    else:
        fig.update_layout(xaxis_title='{} (Total)'.format(variable))
    return fig


@app.callback(
    dash.dependencies.Output('y-england-series', 'figure'),
    [dash.dependencies.Input('crossfilter-year--slider', 'value'),
     dash.dependencies.Input('crossfilter-indicators', 'value'),
     dash.dependencies.Input('crossfilter-england', 'value'),
     dash.dependencies.Input('crossfilter-sum-type', 'value'),
     ])
def update_graph(year_value, variable, crossfilter_england, sum_ave):
    dict_season = {
        0: '93/94',
        1: '94/95',
        2: '95/96',
        3: '96/97',
        4: '97/98',
        5: '98/99',
        6: '99/00',
        7: '00/01',
        8: '01/02',
        9: '02/03',
        10: '03/04',
        11: '04/05',
        12: '05/06',
        13: '06/07',
        14: '07/08',
        15: '08/09',
        16: '09/10',
        17: '10/11',
        18: '11/12',
        19: '12/13',
        20: '13/14',
        21: '14/15',
        22: '15/16',
        23: '16/17',
        24: '17/18',
        25: '18/19',
        26: '19/20',
        27: '20/21'
    }
    year_value[1] = min(year_value[1] + 1, len(df_sel_form['season'].unique()))
    if sum_ave == 'Valors Mitjans':

        df = df_sel_form[
                 (df_sel_form['season'].isin([dict_season[x] for x in range(*year_value)]))
                 &
                 (df_sel_form['Div'] == 'E0')
                 ].groupby('Equip').mean()[[variable]].dropna().sort_values(variable)
    else:
        df = df_sel_form[
                 (df_sel_form['season'].isin([dict_season[x] for x in range(*year_value)]))
                 &
                 (df_sel_form['Div'] == 'E0')
                 ].groupby('Equip').sum()[[variable]].dropna().sort_values(variable)

    df.reset_index(inplace=True)
    if (crossfilter_england != "Tots els equips") and (crossfilter_england not in df.iloc[-7:]['Equip'].unique()):
        df_toplot = df.iloc[-6:].append(df[df['Equip'] == crossfilter_england])
        afegit = True
    else:
        df_toplot = df.iloc[-7:]
        afegit=False
    fig = px.bar(df_toplot, y="Equip", x=variable, orientation='h')
    if afegit:
        fig.update_layout(title='Top-6 + {} en {} a Anglaterra'.format(crossfilter_england, variable))
    else:
        fig.update_layout(title='Top-7 en {} a Anglaterra'.format(variable))
    if sum_ave == 'Valors Mitjans':
        fig.update_layout(xaxis_title='{} (Mitjana per partit)'.format(variable))
    else:
        fig.update_layout(xaxis_title='{} (Total)'.format(variable))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
