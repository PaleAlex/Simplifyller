import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

def findNA(df):
    na = df[df.isna().any(axis=1)]
    len_na = len(na)
    if len_na > 0:
        rows_to_inspect = na.index
        return na, len_na, rows_to_inspect
    else:
        return False

def criticalColumns(df):
    mask = np.array(df.isna().sum()>0)
    df_columns = df.columns
    na_columns = [x for x in mask*df_columns if x != '']
    return na_columns

def boxpl(df, groupings, choose):
    if len(groupings)==2:
        fig, axes = plt.subplots(1,2, sharey=True)
        palettes = ["Set1", "Set2"]
        for g in range(len(groupings)):   
            sns.boxplot(y=choose, x=groupings[g], data=df, palette=palettes[g], ax = axes[g])
            axes[g].title.set_text(f'Boxplot of {choose} values by {groupings[g]}')
        return fig
    elif len(groupings)==1:
        fig, axes = plt.subplots()
        palettes = ["Set1"]   
        sns.boxplot(y=choose, x=groupings[0], data=df, palette=palettes[0])
        axes.title.set_text(f'Boxplot of {choose} values by {groupings[0]}')
        return fig  
    else:
        fig, axes = plt.subplots()
        palettes = ["Set1"] 
        sns.boxplot(y=choose, data=df, palette=palettes[0])
        axes.title.set_text(f'Boxplot of {choose} values')
        return fig      

def histpl(df, groupings, choose, row):
    if len(groupings)==2:
        fig, axes = plt.subplots(1, 2, sharey=True)
        colors =  ["maroon","seagreen"]
        for g in range(len(groupings)):   
            util = df.iloc[row][groupings[g]]
            mask1 = df[groupings[g]] == util
            masked_df = df.loc[mask1]
            sns.histplot(data = masked_df[choose].values, ax = axes[g], color=colors[g])
            axes[g].title.set_text(f'Distribution of {choose} values when {groupings[g]}={util}')
        return fig
    elif len(groupings)==1:
        fig, axes = plt.subplots()
        colors =  ["maroon"]
        util = df.iloc[row][groupings[0]]
        mask1 = df[groupings[0]] == util
        masked_df = df.loc[mask1]
        sns.histplot(data = masked_df[choose].values, color=colors[0])
        axes.title.set_text(f'Distribution of {choose} values when {groupings[0]}={util}')
        return fig
    else:
        fig, axes = plt.subplots()
        colors =  ["maroon"]
        sns.histplot(data = df[choose].values, color=colors[0])
        axes.title.set_text(f'Distribution of {choose} values')
        return fig

def q5(x):
    return x.quantile(0.05)

def q25(x):
    return x.quantile(0.25)

def q75(x):
    return x.quantile(0.75)

def q95(x):
    return x.quantile(0.95)

def stratifiedView(df, groupings, choose):
    if len(groupings)>0:
        stats = df.groupby(groupings, as_index = False)[choose].agg(['min', q5, q25, q75, q95, 'max','median','mean', 'std']).reset_index().round(1)
    else:
       stats= df[choose].describe()
    return stats