import math
import warnings
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def bar_plot(df, x, xlabels, order, title='', fontsize='large', palette='PuBu_r',height=6, alpha=1):
    df_aux = df[x].value_counts(normalize=True)
    df_aux = df_aux.mul(1)
    df_aux = df_aux.rename('percent').reset_index()

    g = sns.catplot(x='index',y='percent',kind='bar',data=df_aux, order=order, palette=palette, height=height, alpha=alpha)
    
    g.ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))

    for p in g.ax.patches:
        percentage = p.get_height().round(2) * 100
        txt = str(round(percentage)) + '%'
        txt_x = p.get_x() + 0.2 
        txt_y = p.get_height() - 0.07
        g.ax.text(txt_x,txt_y,txt,fontsize=fontsize, color='white')    
    
    sns.despine(left=True)
    g.set(yticklabels=[])
    g.set_axis_labels("", "")
    g.ax.set_xlabel("",fontsize=fontsize)
    g.ax.set_ylabel("",fontsize=fontsize)
    g.ax.set_xticklabels(xlabels)
    g.ax.set_title(title,fontsize='medium', loc='left')
    
def horizontal_bar_plot(df, x, title='', palette="Blues_r"):
    df_aux = df[x].value_counts(normalize=True)
    df_aux = df_aux.mul(1)
    df_aux = df_aux.rename('percent').reset_index()
    
    g = sns.catplot(x='percent',y='index',kind='bar',data=df_aux, palette=palette, alpha=1)
    
    g.ax.xaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
    
    for p in g.ax.patches:
        if math.isnan(p.get_width().round(2)):
            percentage = txt_y = 0
        else:
            percentage = p.get_width().round(2) * 100
            txt_y = p.get_width()
        txt = str(round(percentage)) + '%'
        txt_x = p.get_y() + 0.5
        g.ax.text(txt_y,txt_x,txt)
        
    sns.despine(left=True, bottom=True)
    g.ax.set_title(title,fontsize='medium', loc='left')    
    g.set_axis_labels("", "")
    g.set(xticklabels=[])
    
def hist_plot(df, x, xlabel, fontsize='medium', title='', hue='', figsize=(10, 5), xlim=[]):
    
    fig, ax = plt.subplots(figsize=figsize)

    if hue == '':   
        ax = sns.histplot(df[x], kde=True)
    else:
        ax = sns.histplot(data=df, x=x, hue=hue, multiple="dodge", kde=True)
        ax.legend(title="", labels=['Dibético', 'Não Dibético'])
        
    if (len(xlim) != 0):
        ax.set_xlim(xlim[0], xlim[1])    
    sns.despine()
    ax.set_xlabel(xlabel,fontsize=fontsize)
    ax.set_ylabel("",fontsize=fontsize)
    ax.set_title(title,fontsize='medium', loc='left')
    
def hist_plot_annotated(df, x, xlabel, ranges, classifications, colors, fontsize='medium', title='', hue='', hight=4500):
    
    fig, ax = plt.subplots(figsize=(20, 8))
    
    if hue == '':   
        ax = sns.histplot(df[x], kde=True, color='silver')
    else:
        ax = sns.histplot(data=df, x=x, hue=hue, multiple="dodge", kde=True, fill=False)
        ax.legend(title="", labels=['Dibético', 'Não Dibético']) 
        
    for i in range(0, len(classifications)):
        ax.annotate(classifications[i], xy=((ranges[i][0] + ranges[i][1])/2, hight),
                    ha="center", color=colors[i],fontweight='bold', size=fontsize,
                    xytext=(0,70), textcoords='offset points',
                    bbox=dict(boxstyle='round', pad=0.1, fill=False))        
        
        if i < 3:
            ax.axvspan(ranges[i][0],ranges[i][1],  fill=False, ec=colors[i], alpha=0.3, linewidth=3.0)
        else:
            ax.axvspan(ranges[i][0],ranges[i][1], color=colors[i], alpha=0.3)
        
     
    sns.despine()
    ax.set_xlabel(xlabel,fontsize=fontsize)
    ax.set_ylabel("",fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)    

def order_grouped_df(grouped_df, x):
    grouped_df = grouped_df.sort_values("percent", ascending=True)
    
    df_diab = grouped_df.loc[(grouped_df['diabetes_mellitus'] == "Dibético")]
    df_ndiab = grouped_df.loc[(grouped_df['diabetes_mellitus'] == "Não Dibético")]
        
    new_df = pd.DataFrame(columns = [x, 'diabetes_mellitus', 'percent']) 
    
    for index1, row1 in df_diab.iterrows():
        new_df = new_df.append(row1, ignore_index = True)
        for index2, row2 in df_ndiab.iterrows():
            if row1[x] == row2[x]:
                new_df = new_df.append(row2, ignore_index = True)
    
    
    for index, row in df_ndiab.iterrows():
        if row[x] not in new_df.values :
            new_df.loc[-1] = [row[x], row['diabetes_mellitus'], row['percent']] 
            new_df.index = new_df.index + 1  
            new_df.sort_index(inplace=True) 
    return new_df

def grouped_bar_plot(df, x, y, hue_order, remove_legend=False, height=6, title='', fontsize=15):
    df_aux = df.groupby(x)[y].value_counts(normalize=True)
    df_aux = df_aux.mul(1)
    df_aux = df_aux.rename('percent').reset_index()
    
    df_aux = order_grouped_df(df_aux, x)

    g = sns.catplot(x='percent',y=x,hue=y,kind='bar',data=df_aux, hue_order=hue_order,
                    ci="sd", palette="dark",alpha=.6, height=height)
        
    g.ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:.0%}'.format(x))) 
    
    sns.despine(left=True, bottom=True, top=False)
    g.ax.set_xlabel("",fontsize=fontsize)
    g.ax.set_ylabel("",fontsize=fontsize)
    g.ax.tick_params(labelsize=fontsize)
    g.set_axis_labels("", "")
    g.ax.set_xlim(0,1.1)    
    g._legend.remove()
    g.ax.xaxis.tick_top()        
    g.ax.set_title(title,fontsize=fontsize, loc='left')
    g.ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), shadow=True, ncol=2)
    
def line_plot(df, x, y, xlabel='', ylabel='', fontsize='large', title=''):
    df_aux = df.groupby(y)[x].value_counts()
    df_aux = df_aux.mul(1)
    df_aux = df_aux.rename('nr_pacientes').reset_index()
    
    g = sns.catplot(x=x, y="nr_pacientes", hue=y,
                markers=["", ""], linestyles=["-", "--"], alpha=0.6, ci="sd", height=5, aspect=2, kind="point", 
                    data=df_aux, palette={0: "b", 1: "darkorange"})
    
    g.ax.annotate('Não diabéticos', xy=(0, 82000), xytext=(5, 82000), fontsize=13,
                arrowprops=dict(color='b', arrowstyle="->",connectionstyle='arc3,rad=-0.5'), color='b');
    g.ax.annotate('Diabéticos', xy=(0, 20000), xytext=(5, 20000), fontsize=13,
                    arrowprops=dict(color='darkorange', arrowstyle="->", connectionstyle='arc3,rad=-0.5'), color='darkorange');

    sns.despine()
    g._legend.remove()
    g.set_axis_labels("", "")
    g.ax.set_xlabel(ylabel,fontsize=fontsize)
    g.ax.set_ylabel(xlabel,fontsize=fontsize)
    g.ax.set_title(title,fontsize=fontsize, loc='left')
    
def bmi_classification(df):
    df_aux = df.loc[(df['weight'].notnull()) & (df['height'].notnull())]
    classfications = []
    for index, row in df_aux.iterrows():

        if row['bmi'] < 18.5:
            classfications.append('Magreza')
        elif (row['bmi'] >= 18.5 and row['bmi'] < 25):
            classfications.append('Normal')
        elif (row['bmi'] >= 25 and row['bmi'] < 30):
            classfications.append('Sobrepeso')
        elif (row['bmi'] >= 30 and row['bmi'] < 35):
            classfications.append('Obesidade Tipo I')
        elif (row['bmi'] >= 35 and row['bmi'] < 40):
            classfications.append('Obesidade Tipo II')
        else:
            classfications.append('Obesidade Tipo III')

    df_aux['imc_classification'] = classfications
    return df_aux

def glucose_classification(df):
    df_aux = df.loc[df['glucose_apache'].notnull()]
    classfications = []
    for index, row in df_aux.iterrows():

        if row['glucose_apache'] < 70:
            classfications.append('Abaixo')
        elif (row['glucose_apache'] >= 70 and row['glucose_apache'] < 100):
            classfications.append('Normal')
        elif (row['glucose_apache'] >= 100 and row['glucose_apache'] < 126):
            classfications.append('Pré-Diabetes')
        elif (row['glucose_apache'] >= 126):
            classfications.append('Diabetes')

    df_aux['glucose_classification'] = classfications
    return df_aux