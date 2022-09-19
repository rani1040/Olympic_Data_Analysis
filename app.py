import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import Preprocessor
import Helper
import plotly.express as px
import plotly.figure_factory as ff

import  seaborn as sns

df = pd.read_csv("C:/Users/rani/Downloads/archive (12)/athlete_events.csv")
region = pd.read_csv(r"C:\Users\rani\Downloads\archive (12)\noc_regions.csv")

df = Preprocessor.preprocess(df, region)
st.sidebar.image("img.png")


user_menu = st.sidebar.radio(
    'Select an Option ',
    ('Overall Analysis', 'Medal Tally', 'Country_Wise_Analysis', 'Athlete wise Analysis')

)


st.dataframe(df)
st.sidebar.title("Olympics Analysis")


if user_menu == 'Medal Tally':
    st.header("Medal Tally ")

    years, country = Helper.country_year_list(df)
    Selected_years = st.sidebar.selectbox("Selected  Year", years)
    Selected_country = st.sidebar.selectbox("Selected Country", country)
    medal_tally = Helper.fetch_Medal_Tally(df, Selected_years, Selected_country)

    if (Selected_years == "Overall") and (Selected_country == 'Overall'):
        st.title("Overall Tally ")

    if  (Selected_years != "Overall") and (Selected_country=='Overall'):
         st.title(Selected_country + "Overall Performance ")

    if Selected_years != "Overall" and  Selected_country== "Overall":
        st.title("Medal Tally in  " + str(Selected_years) + "Olympics")

    if Selected_years != "Overall" and  Selected_country != "Overall":
        st.title(Selected_country+"Performance in "+str(Selected_years))

    st.table(medal_tally)

if user_menu=='Overall Analysis':

    edition = len(df['Year'].unique())-1
    cities =  df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    althletes = df['Name'].unique().shape[0]
    nations = df['Sport'].unique().shape[0]

    st.title("Top Statistics ")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions ")
        st.title(edition)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col1:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nation")
        st.title(nations)
    with col1:
        st.header("Atheletes")
        st.title(althletes)

    nation_overtime = Helper.data_over_time(df,'region')
    fig = px.line(nation_overtime, x='index', y='Year')
    st.title("Participating Nations Over the year ")
    st.plotly_chart(fig)


    events_overtime = Helper.data_over_time(df, 'Event')
    fig = px.line(events_overtime, x='index', y='Year')
    st.title("Events Over the year ")
    st.plotly_chart(fig)

    althletes_overtime = Helper.data_over_time(df, 'Name')
    fig = px.line(althletes_overtime, x='index', y='Year')
    st.title("Athletes  Over the year ")
    st.plotly_chart(fig)

    st.title("Number of Events Over time (Every Sport)")
    fig, ax = plt.subplots(figsize =(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("Most Succesfull Athletes ")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sports = st.selectbox("Select a Sports ",sport_list)
    x = Helper.most_succesfull(df,selected_sports)
    st.table(x)

if user_menu=='Country_Wise_Analysis':

    st.sidebar.title("Country Wise Analysis")
    country_list = df['region'].dropna().unique().tolist()


    selected_country = st.sidebar.selectbox("Select a country ",country_list)
    country_df = Helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + "Medal Tally Over the Years . ")
    st.plotly_chart(fig)


    st.title(selected_country + "Excel in  the following Sport ")
    pt = Helper.country_event_heatmap(df,selected_country)
    fig,ax = plt.subplots(figsize =(20,20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)


    st.title("Top 10 Athletes of "+selected_country)
    top_temp_df = Helper.most_succesfull_athelte_of_country(df,selected_country)
    st.table(top_temp_df)


if user_menu== 'Athlete wise Analysis':

    st.title("Distribution of Age")
    athelet_df = df.drop_duplicates(subset=['Name', 'region'])
    athelet_df['Age'].isnull().sum()
    x1 = athelet_df['Age'].dropna()
    x2 = athelet_df[athelet_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athelet_df[athelet_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athelet_df[athelet_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['overall_age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_rug=False, show_hist=False)
    fig.update_layout(autosize =False,width=1000,height =600)
    st.plotly_chart(fig)


    st.title("Distribution of Age with respect to Gold Medalist ")
    age = []
    sport_name = []
    famous_sports = df['Sport'].value_counts().nlargest(25).reset_index().sort_values('Sport', ascending=False)[
        'index'].tolist()
    for sport in famous_sports:
        temp_df = athelet_df[athelet_df['Sport'] == sport]
        age.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        sport_name.append(sport)

    fig = ff.create_distplot(age,sport_name,show_rug=False, show_hist=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sports = st.selectbox("Select a Sports ", sport_list)
    temp_df = Helper.weight_vs_heigth(df,selected_sports)

    plt.title("Height bs Weight in wining Medals ")
    fig,ax = plt.subplots()
    ax=sns.scatterplot(x= temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=df['Sex'])
    st.pyplot(fig)

    st.title("Men vs Women")
    final = Helper.meb_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    st.plotly_chart(fig)
