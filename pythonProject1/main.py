from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)


@app.route('/')
def index():
    # Ler o arquivo CSV usando pandas
    df = pd.read_csv('spotify.csv')

    # Criar o gráfico de dispersão usando Plotly
    fig = px.scatter(df, x='released_year', y='in_spotify_charts',
                     title='Correlação entre Ano de Lançamento e Presença nas Playlists do Spotify',
                     labels={'released_year': 'Ano de Lançamento', 'in_spotify_charts': 'Presença nas Playlists: '},
                     height=850, width=1950)

    fig.update_xaxes(range=[1930, 2024])
    fig.update_yaxes(range=[0, 55])

    # Converter o gráfico para HTML
    graph_html = pio.to_html(fig, full_html=False)

    # Renderizar o template com o gráfico
    return render_template('index.html', graph_html=graph_html)


if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def home():
    # Ler o arquivo CSV usando pandas
    df = pd.read_csv('spotify.csv')

    # Calcular o total de streams por artista
    total_streams_por_artista = spotify.groupby('artist(s)_name')['streams'].sum().reset_index()

    # Calcular o total de streams e o percentual de cada artista
    total_streams = total_streams_por_artista['streams'].sum()
    total_streams_por_artista['percentual'] = (total_streams_por_artista['streams'] / total_streams) * 100

    # Criar o gráfico de pizza
    fig = px.pie(data_frame=total_streams_por_artista, names='artist(s)_name', values='percentual',
                 title='Total de Execuções por Artista',
                 height=500, width=700)

    # Converter o gráfico para HTML
    graph_html = fig.to_html(full_html=False)

    # Renderizar o template com o gráfico
    return render_template('index.html', graph_html=graph_html)