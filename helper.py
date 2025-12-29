import pandas as pd
from collections import Counter
from wordcloud import WordCloud
from urlextract import URLExtract
import emoji

extract = URLExtract()

# ----------------- BASIC STATISTICS -----------------
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['messages']:
        words.extend(str(message).split())

    num_media = df[df['messages'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['messages']:
        links.extend(extract.find_urls(str(message)))

    return num_messages, len(words), num_media, len(links)

# ----------------- MOST BUSY USERS -----------------
def most_busy_users(df):
    x = df['users'].value_counts().head()
    df_percent = round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','users':'percent'})
    return x, df_percent

# ----------------- WORDCLOUD -----------------
def create_wordcloud(selected_user, df):
    stop_words = open('stop_hinglish.txt', 'r', encoding='utf-8').read()

    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y=[]
        for word in str(message).lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    temp['messages'] = temp['messages'].apply(remove_stop_words)
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc

# ----------------- MOST COMMON WORDS -----------------
def most_common_words(selected_user, df):
    stop_words = open('stop_hinglish.txt', 'r', encoding='utf-8').read()

    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    words=[]
    for message in temp['messages']:
        for word in str(message).lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

# ----------------- EMOJI ANALYSIS -----------------
def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    emojis_list=[]
    for message in df['messages']:
        emojis_list.extend([c for c in str(message) if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis_list).most_common(10), columns=['emoji','count'])
    return emoji_df

# ----------------- TIMELINES -----------------
def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['messages'].reset_index()
    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    daily = df.groupby('only_date').count()['messages'].reset_index()
    return daily

# ----------------- ACTIVITY MAPS -----------------
def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    return df['month'].value_counts()

def hourly_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    return df.groupby('hour').count()['messages'].reset_index()

# ----------------- SMART INSIGHTS -----------------
def smart_insights(selected_user, df):
    num_messages, words, num_media, num_links = fetch_stats(selected_user, df)
    busy_day = week_activity_map(selected_user, df).idxmax()
    busy_month = month_activity_map(selected_user, df).idxmax()
    peak_hour = hourly_activity(selected_user, df).sort_values(by='messages', ascending=False).iloc[0]['hour']

    insights = [
        f"User: {selected_user}",
        f"Total Messages: {num_messages}",
        f"Total Words: {words}",
        f"Media Shared: {num_media}",
        f"Links Shared: {num_links}",
        f"Most Active Day: {busy_day}",
        f"Most Active Month: {busy_month}",
        f"Peak Chatting Hour: {peak_hour}:00",
        "Tip: Engage more during off-peak hours to avoid message overload!",
        "Insight: Check emojis and frequently used words to understand your chat tone."
    ]
    return insights


