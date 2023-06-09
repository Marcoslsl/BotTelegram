import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io

def plot_bar_nps(df: pd.DataFrame) -> any:

    buf = io.BytesIO()

    df_nps_setor = df[['Setor', 'NPS interno']].groupby("Setor").mean().reset_index()
    df_nps_setor = df_nps_setor.sort_values("NPS interno", ascending=False)

    sns.barplot(data=df_nps_setor, y='Setor', x='NPS interno', orient='h', palette='Paired_r');
    plt.savefig(buf, format="png")
    plt.close()
    return buf
    

def plot_bar_cont(df: pd.DataFrame) -> any:
    buf = io.BytesIO()

    df_nps_contratacao = df[['Tipo de Contratação', 'NPS interno']].groupby("Tipo de Contratação").mean().reset_index()
    df_nps_contratacao = df_nps_contratacao.sort_values("NPS interno", ascending=False)

    sns.barplot(data=df_nps_contratacao, y='Tipo de Contratação', x='NPS interno', orient='h', palette='Paired_r');
    plt.savefig(buf, format="png")
    plt.close()
    return buf

def plot_hist_nps(df: pd.DataFrame) -> any:
    buf = io.BytesIO()
    sns.histplot(df['NPS interno'])

    plt.savefig(buf, format="png")
    plt.close()
    return buf
     
