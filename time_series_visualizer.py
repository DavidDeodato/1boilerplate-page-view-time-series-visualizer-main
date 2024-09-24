import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Importar dados
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Limpar dados
df = df[(df['value'] >= df['value'].quantile(0.025)) & 
        (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Desenhar gráfico de linha
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df.index, df['value'], 'r', linewidth=1)
    
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    
    # Salvar imagem e retornar fig
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copiar e modificar dados para gráfico de barras mensal
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.strftime('%B')
    
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    
    # Reordenar as colunas dos meses
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 
              'August', 'September', 'October', 'November', 'December']
    df_bar = df_bar.reindex(columns=months)
    
    # Desenhar gráfico de barras
    fig = df_bar.plot(kind='bar', figsize=(14, 6), width=0.8).figure
    plt.legend(title='Months', loc='upper left', bbox_to_anchor=(1, 1))
    plt.title('Average Page Views per Month')
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    
    # Salvar imagem e retornar fig
    fig.savefig('bar_plot.png', bbox_inches='tight')
    return fig

def draw_box_plot():
    # Preparar dados para gráficos de caixa
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    
    # Desenhar gráficos de caixa
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))
    
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=ax2)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    
    # Salvar imagem e retornar fig
    fig.savefig('box_plot.png')
    return fig