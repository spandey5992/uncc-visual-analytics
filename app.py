import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
from vega_datasets import data
import streamlit as st


read_file = pd.read_csv("../01.Dataset/Google-Playstore.csv")
df_play_store = pd.DataFrame(read_file)

# Data Cleaning
df_play_store = df_play_store.dropna()
df_play_store.drop(columns=['Developer Id', 'Developer Website', 'Developer Email',
                   'Editors Choice', 'App Id', 'Privacy Policy', 'Scraped Time', 'Ad Supported'])
df_play_store['Average Installs'] = (
    df_play_store['Minimum Installs'] + df_play_store['Maximum Installs']) / 2


# Viz 1: Highest Rated Category
def viz1():
    df1 = df_play_store.groupby(
        'Category')['Rating'].sum().to_frame().reset_index()
    df1.sort_values(by=['Rating'], inplace=True)

    # Color Scheme
    color_scheme = alt.Scale(scheme='lightmulti')

    viz_1 = alt.Chart(df1).mark_bar(opacity=0.7).encode(
        # sort=alt.SortField(field='Total Installs:Q')
        y=alt.Y('Category:O', sort='x', axis=alt.Axis(title='Category')),
        x=alt.X('Rating:Q', axis=alt.Axis(title='Rating')),
        tooltip=['Category:O', 'Rating:Q'],
        color=alt.Color('Rating:Q', scale=color_scheme)
    ).properties(
        title='app category vs rating',
        width=800,
        height=800
    )

    st.write(viz_1)

    # Second
    average_ratings = pd.DataFrame(df_play_store[df_play_store['Rating'] > 0].groupby(
        'Category')['Rating'].mean()[:25])

    average_ratings.reset_index(inplace=True)
    average_ratings['Rating'] = round(average_ratings['Rating'], 1)
    color_scheme = alt.Scale(scheme='lightmulti')

    highest_rated_category = alt.Chart(average_ratings).mark_bar(opacity=0.7).encode(
        # sort=alt.SortField(field='Total Installs:Q')
        x=alt.X('Category:O', sort='-y', axis=alt.Axis(title='Category')),
        y=alt.Y('Rating:Q', axis=alt.Axis(title='Rating')),
        tooltip=['Category:O', 'Rating:Q'],
        color=alt.Color('Rating:Q', scale=color_scheme)
    ).properties(
        title='app category vs rating',
        width=800,
        height=500
    )

    st.write(highest_rated_category)


# Viz 2: Top 10 most installed apps
def viz2():
    df2_1 = df_play_store.nlargest(10, 'Average Installs')
    df2_1[['Average Installs']] = df2_1[['Average Installs']] / 1000000000

    # Color Scheme
    color_scheme = alt.Scale(scheme='teals')

    viz_2 = alt.Chart(df2_1).mark_bar(opacity=0.7).encode(
        # sort=alt.SortField(field='Total Installs:Q')
        y=alt.Y('App Name:O', sort='x', axis=alt.Axis(title='App Name')),
        x=alt.X('Average Installs:Q', axis=alt.Axis(
            title='Average Installs (Billions)')),
        tooltip=['Average Installs:Q'],
        color=alt.Color('Average Installs:Q', scale=color_scheme)
    ).properties(
        title='Top 10 most installed Apps',
        width=800,
        height=600
    )

    st.write(viz_2)


# Viz 3: Top 10 categories in the Google Play Store with the most apps
def viz3():
    categories = df_play_store['Category'].value_counts().nlargest(10)

    # Color Scheme
    color_scheme = alt.Scale(scheme='lighttealblue')

    viz_31 = alt.Chart(categories.reset_index().rename(columns={'Category': 'Count', 'index': 'Category'})).mark_bar(opacity=0.7).encode(
        y=alt.Y('Category:O', sort='x', axis=alt.Axis(title='Category')),
        x=alt.X('Count:Q', axis=alt.Axis(title='Total Count')),
        tooltip=['Category:O', 'Count:Q'],
        color=alt.Color('Count:Q', scale=color_scheme)
    ).properties(
        title='Total Playstore Apps per Category',
        width=800,
        height=500
    )

    total_installs_per_category = df_play_store.groupby(
        'Category')['Average Installs'].sum().nlargest(10)

    # Color Scheme
    color_scheme = alt.Scale(scheme='lightgreyteal')

    viz_32 = alt.Chart(total_installs_per_category.reset_index()).mark_bar(opacity=0.7).encode(
        y=alt.Y('Category:O', sort='x', axis=alt.Axis(title='Category')),
        x=alt.X('Average Installs:Q', axis=alt.Axis(title='Average Installs')),
        tooltip=['Category:O', 'Average Installs:Q'],
        color=alt.Color('Average Installs:Q', scale=color_scheme)
    ).properties(
        title='Total installs for each category',
        width=800,
        height=500
    )

    st.write(viz_31)
    st.write(viz_32)


# What was the most installed game per category?
def viz4():
    game_cats = ['Strategy', 'Adventure', 'Word', 'Puzzle', 'Simulation', 'Role Playing',
                 'Action', 'Casual', 'Racing', 'Sports', 'Arcade', 'Card', 'Music', 'Trivia']
    df_play_store['IsGame'] = 0
    df_play_store.loc[df_play_store['Category'].isin(game_cats), 'IsGame'] = 1

    most_installed = df_play_store.loc[df_play_store[df_play_store['IsGame'] == 1].groupby(
        'Category')['Average Installs'].idxmax()]

    most_installed[['Average Installs']] = most_installed[[
        'Average Installs']] / 1000000000

    # Color Scheme
    color_scheme = alt.Scale(scheme='category10')

    bars = alt.Chart(most_installed.reset_index()).mark_bar(opacity=0.7).encode(
        y=alt.Y('Category:O', sort='x', axis=alt.Axis(title='Category')),
        x=alt.X('Average Installs:Q', axis=alt.Axis(
            title='Average Installs (Billions)')),
        tooltip=['Category:O', 'Average Installs:Q', 'App Name:O'],
        color=alt.Color('Average Installs:Q', scale=color_scheme)
    ).properties(
        title='Total installs for each category',
        width=800,
        height=800
    )

    text = bars.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='App Name:O'
    )

    st.write(bars + text)


def viz5():
    df_play_store['Free'] = df_play_store['Free'].map(
        {True: 'Free', False: 'Paid'})
    free_vs_paid = pd.DataFrame(df_play_store['Free'].value_counts())
    free_vs_paid.reset_index(inplace=True)
    free_vs_paid = free_vs_paid.rename(
        columns={'Free': 'Count', 'index': 'Category'})
    free_vs_paid['Percentage'] = round(
        (free_vs_paid['Count'] / free_vs_paid['Count'].sum()) * 100, 1)

    color_scheme = alt.Scale(scheme='category10')

    base = alt.Chart(free_vs_paid).mark_arc().encode(
        theta=alt.Theta("Count:Q", stack=True),
        color=alt.Color("Category:N", legend=None, scale=color_scheme),
        tooltip=['Category:N', 'Percentage:Q']
    ).properties(
        title='Free vs Paid Apps',
        width=500,
        height=500
    )

    pie = base.mark_arc(outerRadius=170)
    text = base.mark_text(radius=190, size=16).encode(text="Category:N")

    st.write(pie + text)


def viz6():
    content_ratings = pd.DataFrame(
        df_play_store['Content Rating'].value_counts())
    content_ratings.reset_index(inplace=True)
    content_ratings = content_ratings.rename(
        columns={'Content Rating': 'Number of Apps', 'index': 'Content Rating'})
    # content_ratings['log_value'] = np.log10(content_ratings['Number of Apps'])

    # Color Scheme
    color_scheme = alt.Scale(scheme='redyellowgreen')

    chart = alt.Chart(content_ratings).mark_bar(opacity=0.7).encode(
        x=alt.X('Content Rating:O', sort='-y',
                axis=alt.Axis(title='Content Rating')),
        y=alt.Y('Number of Apps:Q', axis=alt.Axis(title='Number of Apps')),
        tooltip=['Content Rating:O', 'Number of Apps:Q'],
        color=alt.Color('Number of Apps:Q', scale=color_scheme)
    ).properties(
        title='Content Rating',
        width=800,
        height=500
    )

    text = chart.mark_text(
        align='center',
        baseline='bottom',
        dx=0,   # Nudges text to right so it doesn't appear on top of the bar
        dy=0,
        fontSize=10,
        color='orange'

    ).encode(
        text=alt.Text('Number of Apps:Q'),
    )

    st.write(chart + text)


radio_select = st.sidebar.radio('Select Visualization:', ('Viz 1: Highest Rated Category',
                                                          'Viz 2: Top 10 most installed Apps',
                                                          'Viz 3: Total Playstore Apps per Category',
                                                          'Viz 4: Total installs for each category',
                                                          'Viz 5: Free vs Paid Apps',
                                                          'Viz 6: Content Rating'
                                                          ))

if radio_select == 'Viz 1: Highest Rated Category':
    viz1()
elif radio_select == 'Viz 2: Top 10 most installed Apps':
    viz2()
elif radio_select == 'Viz 3: Total Playstore Apps per Category':
    viz3()
elif radio_select == 'Viz 4: Total installs for each category':
    viz4()
elif radio_select == 'Viz 5: Free vs Paid Apps':
    viz5()
elif radio_select == 'Viz 6: Content Rating':
    viz6()
