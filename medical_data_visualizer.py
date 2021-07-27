import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
df['overweight'] = [1 if imc > 25 else 0 for imc in df['weight'] / (df['height'] / 100) ** 2]
# print(df['overweight'])

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
#! todo: investigate best way for filter and replace. easy way in single line
df['cholesterol'] = [0 if it == 1 else 1 for it in df['cholesterol']]
df['gluc'] = [0 if it == 1 else 1 for it in df['gluc']]


# print(df['cholesterol'], df['gluc'])


# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    cols = ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    df_cat = pd.melt(df, id_vars='cardio', value_vars=cols)
    # print(df_cat.head())
    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'])['value'].count().reset_index(name='total')
    # print(df_cat.head())
    # Draw the catplot with 'sns.catplot()'
    # todo: investigate seaborn
    fig = sns.catplot(
        x='variable', y='total', col='cardio', hue='value', data=df_cat, kind='bar').fig
    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    #? todo: check df.loc https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi'])  # 1
        &
        (df['height'] >= df['height'].quantile(0.025))  # 2
        &
        (df['height'] <= df['height'].quantile(0.975))  # 3
        &
        (df['weight'] >= df['weight'].quantile(0.025))  # 4
        &
        (df['weight'] <= df['weight'].quantile(0.975))  # 5
        ]

    # print(df_heat.head())
    # Calculate the correlation matrix
    corr = df_heat.corr()
    #print(corr)
    # Generate a mask for the upper triangle
    mask = np.triu(corr, 0)
    print(mask)
    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(14, 14))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr,
                annot=True,  # todo: no idea, just work with true, check reason
                fmt='.1f',  #* agggggghhhhhh todo: never ever forget check decimal points
                mask=mask)
    #! todo: fig colors are not the same, fixit?? how?
    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
