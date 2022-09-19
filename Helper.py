import pandas as pd

def medal_tally(df):
    Medal_Tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'City', 'Sport', 'Event', 'Medal'])
    Medal_Tally = Medal_Tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values(by='Gold',
                                                                                                ascending=False).reset_index()
    Medal_Tally['total'] = Medal_Tally['Gold'] + Medal_Tally['Silver'] + Medal_Tally['Bronze']

    Medal_Tally['Gold'] = Medal_Tally['Gold'].astype("int")
    Medal_Tally['Silver'] = Medal_Tally['Silver'].astype("int")
    Medal_Tally['Bronze'] = Medal_Tally['Bronze'].astype("int")
    Medal_Tally['total'] = Medal_Tally['total'].astype("int")

def fetch_Medal_Tally(df, year, country):

    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if (year == "Overall") and (country == 'Overall'):
        temp_df = medal_df

    if year == "Overall" and country != "Overall":
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != "Overall" and country == "Overall":
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != "Overall" and country != "Overall":
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == int(year))]


    if (flag == 1):
        x = temp_df.groupby('year').sum()[['Gold', 'Silver', 'Bronze']].sort_values(by='Gold',
                                                                                    ascending=False).reset_index()
        x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values(by='Gold',
                                                                                      ascending=False).reset_index()
        x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

        x['Gold'] = x['Gold'].astype("int")
        x['Silver'] = x['Silver'].astype("int")
        x['Bronze'] = x['Bronze'].astype("int")
        x['total'] = x['total'].astype("int")


    return x



def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values(
        by='index')
    return nations_over_time


def most_succesfull(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head().merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df


def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])  # inly those rows which are having some value of medals
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == 'India']
    pivot_table = pd.crosstab(new_df['Sport'],new_df['Year'])
    return pivot_table


def most_succesfull_athelte_of_country(df, country):
    temp_df = df.dropna(subset=['Medal'])

    if country != 'Overall':
        temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().head(10).reset_index().merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x


def weight_vs_heigth(df,sport):
    athelet_df = df.drop_duplicates(subset=['Name', 'region'])
    athelet_df['Medal'].fillna('No Medal', inplace=True)
    if sport!='Overall':
        temp_df = athelet_df[athelet_df['Sport'] == sport]
        return temp_df
    else:
        return athelet_df

def meb_vs_women(df):
    athelet_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athelet_df[athelet_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    female = athelet_df[athelet_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(female, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)
    return final

