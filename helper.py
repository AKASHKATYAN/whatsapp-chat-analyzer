from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji 
 
 
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
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)       
     
    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color='white'
    )
    temp['messages']= temp['messages'].apply(remove_stop_words)
    df_wc = wc.generate(temp['messages'].str.cat(sep=" "))
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

def emoji_helper(selected_user,df):
       if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
       emojis=[]
       for message in df['messages']:
           emojis.extend([c for c in message if c in emoji.EMOJI_DATA]) 
       emoji_df=pd.DataFrame(Counter(emojis).most_common(5),  columns=['emoji', 'count']) 
       return emoji_df  

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline=df.groupby(['year','month_num','month']).count()['messages'].reset_index()  
    
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i])) 
    timeline['time']=time
    return timeline     
  
def daily_timeline(selected_user,df):
      if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

      daily_timeline=df.groupby('only_date').count()['messages'].reset_index()
      return daily_timeline

def week_activity_map(selected_user,df):
     if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
     return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    return df['month'].value_counts() 

def hourly_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    hourly_df = df.groupby('hour').count()['messages'].reset_index()
    return hourly_df

def smart_insights(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    insights = []

    # Peak hour
    peak_hour = df.groupby('hour').count()['messages'].idxmax()
    if 0 <= peak_hour <= 5:
        insights.append("🌙 Most messages are sent late at night.")
    elif 6 <= peak_hour <= 11:
        insights.append("🌅 User is more active in the morning.")
    elif 12 <= peak_hour <= 17:
        insights.append("☀️ User is active during the afternoon.")
    else:
        insights.append("🌆 User is most active in the evening.")

    # Most active day
    busy_day = df['day_name'].value_counts().idxmax()
    insights.append(f"📅 Most active day is {busy_day}.")

    # Most active month
    busy_month = df['month'].value_counts().idxmax()
    insights.append(f"📆 Highest activity seen in {busy_month}.")

    return insights
