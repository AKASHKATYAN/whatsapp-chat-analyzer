from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pandas as pd

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['messages']:
        words.extend(message.split())

    num_media_messages = df[df['messages'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['messages']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    x = df['users'].value_counts().head()
    df = round(
        (df['users'].value_counts() / df.shape[0]) * 100, 2
    ).reset_index().rename(columns={'index': 'name', 'users': 'percent'})
    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color='white'
    )
    df_wc = wc.generate(df['messages'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    words = []

    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

   

