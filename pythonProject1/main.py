from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

@app.route('/')
def index():
    # Ler o arquivo CSV usando pandas
    df = pd.read_csv('spotify.csv')

#PRIMEIRO GRÁFICO

    # Converter colunas para o tipo correto
    df['released_year'] = pd.to_numeric(df['released_year'], errors='coerce')
    df['in_spotify_charts'] = pd.to_numeric(df['in_spotify_charts'], errors='coerce')
    df['streams'] = pd.to_numeric(df['streams'], errors='coerce')
    df['bpm'] = pd.to_numeric(df['bpm'], errors='coerce')

    # Gráfico de Dispersão: Correlação entre o ano de lançamento e a presença em playlists
    fig1 = px.scatter(df, x='released_year', y='in_spotify_charts',
                      # Título no HTML
                      labels={'released_year': 'Ano de Lançamento', 'in_spotify_charts': 'Presença nas Playlists'},
                      height=830, width=1950)
    fig1.update_xaxes(range=[1930, 2024])
    fig1.update_yaxes(range=[0, 55])
    graph_html1 = pio.to_html(fig1, full_html=False)

#SEGUNDO GRÁFICO

    # Gráfico de Pizza: Total de execuções por artista - TOP 20
    total_streams_por_artista = df.groupby('artist(s)_name')['streams'].sum().reset_index()
    top_artists = total_streams_por_artista.sort_values(by='streams', ascending=False).head(20)
    total_streams = top_artists['streams'].sum()
    top_artists['percentual'] = (top_artists['streams'] / total_streams) * 100
    fig2 = px.pie(top_artists, names='artist(s)_name', values='percentual',
                 #Título no HTML title='Total de Execuções por Artista (Top 20)',
                  height=650, width=750)
    graph_html2 = pio.to_html(fig2, full_html=False)

    # Cálculo da média do BPM
    mean_bpm = df['bpm'].mean()

    # Gráfico de Histograma: Distribuição do BPM
    fig3 = px.histogram(df, x='bpm',
                        labels={'bpm': 'BPM'},
                       #Título no HTML title='Distribuição do BPM',
                        nbins=30, height=450, width=850)
    graph_html3 = pio.to_html(fig3, full_html=False)

#TERCEIRO GRÁFICO

    # Gráfico de Barras: Média de BPM para Músicas com mais de 50M de Execuções
    filtered_df = df[df['streams'] > 50000000]
    avg_bpm = filtered_df['bpm'].mean()
    avg_bpm_df = pd.DataFrame({'Category': ['Média de BPM'], 'Average BPM': [avg_bpm]})
    fig4 = px.bar(avg_bpm_df, x='Category', y='Average BPM',
                  labels={'Category': '', 'Average BPM': 'BPM Médio'},
                 #Título no HTML title='Média de BPM para Músicas com mais de 50M de Execuções',
                  height=400, width=800)
    graph_html4 = pio.to_html(fig4, full_html=False)

    # Renderizar o template com os gráficos e a estatística descritiva
    return render_template('index.html', graph_html1=graph_html1, graph_html2=graph_html2, graph_html3=graph_html3, graph_html4=graph_html4, mean_bpm=mean_bpm)

if __name__ == '__main__':
    app.run(debug=True)
