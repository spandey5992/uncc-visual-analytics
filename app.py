import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
from vega_datasets import data
import streamlit as st


read_file = pd.read_csv("Google-Playstore.csv")
df_play_store = pd.DataFrame(read_file)

# Data Cleaning
df_play_store = df_play_store.dropna()
df_play_store.drop(columns=['Developer Id', 'Developer Website', 'Developer Email',
                   'Editors Choice', 'App Id', 'Privacy Policy', 'Scraped Time', 'Ad Supported'])
df_play_store['Average Installs'] = (
    df_play_store['Minimum Installs'] + df_play_store['Maximum Installs']) / 2000000


# Viz 1: App Categories
# Top Categories based on Count and Install
def viz11():

    categories = df_play_store['Category'].value_counts().nlargest(10)

    # Color Scheme
    color_scheme = alt.Scale(scheme='lighttealblue')

    viz_31 = alt.Chart(categories.reset_index().rename(columns={'Category': 'Count', 'index': 'Category'})).mark_bar(opacity=0.7).encode(
        x=alt.X('Category:O', sort='-y', axis=alt.Axis(title='Category')),
        y=alt.Y('Count:Q', axis=alt.Axis(title='Total Count')),
        tooltip=['Category:O', 'Count:Q'],
        color=alt.Color('Count:Q', scale=color_scheme)
    ).properties(
        title='Total Playstore Apps per Category',
        width=800,
        height=500
    ).configure_axisX(
        labelAngle=320
    )

    total_installs_per_category = df_play_store.groupby(
        'Category')['Average Installs'].sum().nlargest(10)

    # Color Scheme
    color_scheme = alt.Scale(scheme='lightgreyteal')

    viz_32 = alt.Chart(total_installs_per_category.reset_index()).mark_bar(opacity=0.7).encode(
        x=alt.X('Category:O', sort='-y', axis=alt.Axis(title='Category')),
        y=alt.Y('Average Installs:Q', axis=alt.Axis(
            title='Average Installs (Million)')),
        tooltip=['Category:O', 'Average Installs:Q'],
        color=alt.Color('Average Installs:Q', scale=color_scheme)
    ).properties(
        title='Average installs for each Category',
        width=800,
        height=500
    ).configure_axisX(
        labelAngle=320
    )

    st.subheader(
        'What are the top 10 App Category with most App count?')
    st.write(viz_31)
    st.subheader(
        'Which are the top 10 Categories with most App installs?')
    st.write(viz_32)
    st.write('As we can see from the above two plots: Maximum number of apps present in google play store comes under Education, Business and Music & Audio Category but as per the installation and requirement in the market plot, scenario is not the same. Maximum installed apps comes under Tools, Communication and Productivity Category.')


# Most installed Apps in each Category
def viz12():
    game_cats = ['Strategy', 'Adventure', 'Word', 'Puzzle', 'Simulation', 'Role Playing',
                 'Action', 'Casual', 'Racing', 'Sports', 'Arcade', 'Card', 'Music', 'Trivia']
    df_play_store['IsGame'] = 0
    df_play_store.loc[df_play_store['Category'].isin(game_cats), 'IsGame'] = 1

    most_installed = df_play_store.loc[df_play_store[df_play_store['IsGame'] == 1].groupby(
        'Category')['Average Installs'].idxmax()]

    # most_installed[['Average Installs']] = most_installed[[
    #     'Average Installs']] / 1000000000

    # Color Scheme
    color_scheme = alt.Scale(scheme='category10')

    bars = alt.Chart(most_installed.reset_index()).mark_bar(opacity=0.7).encode(
        y=alt.Y('Category:O', sort='x', axis=alt.Axis(title='Category')),
        x=alt.X('Average Installs:Q', axis=alt.Axis(
            title='Average Installs (Billions)')),
        tooltip=['Category:O', 'Average Installs:Q', 'App Name:O'],
        color=alt.Color('Average Installs:Q', scale=color_scheme)
    ).properties(
        title='Average installs for each Category',
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

    st.subheader(
        'What are the top Apps with most installs in each Category?')
    st.write(bars + text)


# Viz 2: App Rating
def viz2():
    # Distribution of Rating
    genres_ratings_df = round(df_play_store.groupby(
        ['Category'])[['Rating']].mean(), 3)

    fig = plt.figure(figsize=(14, 7))
    g = sns.kdeplot(genres_ratings_df.Rating, color="Red", shade=True)
    g.set_xlabel("Rating")
    g.set_ylabel("Frequency")
    plt.title('Distribution of Rating', weight='bold', size=15)
    st.subheader('Average rating')
    st.pyplot(fig)

    # App Category vs Rating
    average_ratings = pd.DataFrame(df_play_store[df_play_store['Rating'] > 0].groupby(
        'Category')['Rating'].mean()[:25])

    average_ratings.reset_index(inplace=True)
    average_ratings['Rating'] = round(average_ratings['Rating'], 1)
    color_scheme = alt.Scale(scheme='lightmulti')

    highest_rated_category = alt.Chart(average_ratings).mark_bar(opacity=0.7).encode(
        x=alt.X('Category:O', sort='-y', axis=alt.Axis(title='Category')),
        y=alt.Y('Rating:Q', axis=alt.Axis(title='Rating')),
        tooltip=['Category:O', 'Rating:Q'],
        color=alt.Color('Rating:Q', scale=color_scheme)
    ).properties(
        title='App Category vs Rating',
        width=800,
        height=500
    ).configure_axisX(
        labelAngle=320
    )
    st.subheader('Highest and lowest Rated Category')
    st.write(highest_rated_category)


# Viz 3: Free vs Paid Apps
def viz31():
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

    st.subheader('Comparing App type: Free/Paid')
    st.write(pie + text)

    app_count = df_play_store.groupby(['Category', 'Free'])[['App Name']].count(
    ).reset_index().rename(columns={'App Name': 'Count', 'index': 'App Name', 'Free': 'Type'})
    df_app_count = app_count.pivot(
        'Category', 'Type', 'Count').fillna(0).reset_index()

    df_app_count.set_index('Category').plot(
        kind='barh', stacked=True, figsize=(23, 30), fontsize=25)
    plt.ylabel("Category", fontsize=25)
    plt.xlabel("Count", fontsize=25)
    plt.title("Count of Apps in each Category differentiated by their type",
              weight='bold', size=25)
    plt.legend(fontsize=20)
    st.subheader('Count of Apps in each Category differentiated by their type')
    st.pyplot(plt)


def viz32():
    average_ratings_by_type = pd.DataFrame(df_play_store[df_play_store['Rating'] > 0].groupby([
                                           'Category', 'Free'])['Rating'].mean()[:25])

    average_ratings_by_type.reset_index(inplace=True)
    average_ratings_by_type = average_ratings_by_type.rename(columns={
                                                             'Free': 'Type'})
    average_ratings_by_type['Rating'] = round(
        average_ratings_by_type['Rating'], 1)

    color_scheme = alt.Scale(scheme='lightmulti')

    highest_rated_type = alt.Chart(average_ratings_by_type).mark_bar(opacity=0.7).encode(
        x=alt.X('Type:O'),  # sort=alt.SortField(field='Total Installs:Q')
        y=alt.Y('Rating:Q', axis=alt.Axis(title='Rating')),
        tooltip=['Category:O', 'Rating:Q'],
        color=alt.Color('Type:O', scale=color_scheme),
        column='Category:O'
    ).properties(
        # title='Rating of Free vs Paid Apps based on Category',
        width=50,
        height=500
    )

    st.subheader('Rating of Free vs Paid Apps based on Category')
    st.write(highest_rated_type)


# Viz 4: Content Rating
def viz4():
    content_ratings = pd.DataFrame(
        df_play_store['Content Rating'].value_counts())
    content_ratings.reset_index(inplace=True)
    content_ratings = content_ratings.rename(
        columns={'Content Rating': 'Number of Apps', 'index': 'Content Rating'})

    # Color Scheme
    color_scheme = alt.Scale(scheme='redyellowgreen')

    chart = alt.Chart(content_ratings).mark_bar(opacity=0.7).encode(
        x=alt.X('Content Rating:O', sort='-y',
                axis=alt.Axis(title='Content Rating')),
        y=alt.Y('Number of Apps:Q', axis=alt.Axis(title='Number of Apps')),
        tooltip=['Content Rating:O', 'Number of Apps:Q'],
        color=alt.Color('Number of Apps:Q', scale=color_scheme)
    ).properties(
        # title='Content Rating',
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

    chart_text = alt.layer(chart, text).configure_axisX(
        labelAngle=320
    )

    st.subheader('What are the different app age categories in the PlayStore?')
    st.write(chart_text)


# Viz 5: Top 10 most installed Apps


def viz5():
    df2_1 = df_play_store.nlargest(10, 'Average Installs')

    # Color Scheme
    color_scheme = alt.Scale(scheme='teals')

    chart = alt.Chart(df2_1).mark_bar(opacity=0.7).encode(
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

    st.subheader('What are the top 10 most installed apps of Playstore?')
    st.write(chart)
    st.write('We can see from the chart that the top 10 apps consist of apps mostly from google, since these apps are pre-installed on the android devices. The only app which made to the top 10 list, and is not developed by google, is Whatsapp. Whatsapp made to the top list because of its popularity and becaue many mobile manufacturers have started providing this as a pre-installed app on android device.')


radio_select = st.sidebar.radio('Select Visualization:', ('Viz 1: App Categories',
                                                          'Viz 2: App Rating',
                                                          'Viz 3: Free vs Paid Apps',
                                                          'Viz 4: Content Rating',
                                                          'Viz 5: Top 10 Apps on Playstore',
                                                          ))

if radio_select == 'Viz 1: App Categories':
    option = st.selectbox(
        'Select:',
        ('Top Categories based on Count and Install', 'Most installed Apps in each Category'))

    if option == 'Top Categories based on Count and Install':
        viz11()
    elif option == 'Most installed Apps in each Category':
        viz12()

elif radio_select == 'Viz 2: App Rating':
    viz2()
elif radio_select == 'Viz 3: Free vs Paid Apps':
    option = st.selectbox(
        'Select:',
        ('Comparing count of Free/Paid apps', 'Comparing Rating of Free/Paid apps'))

    if option == 'Comparing count of Free/Paid apps':
        viz31()
    elif option == 'Comparing Rating of Free/Paid apps':
        viz32()

elif radio_select == 'Viz 4: Content Rating':
    viz4()
elif radio_select == 'Viz 5: Top 10 Apps on Playstore':
    viz5()
