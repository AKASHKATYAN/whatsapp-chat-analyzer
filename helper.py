import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from urlextract import URLExtract
import emoji
import seaborn as sns

extract = URLExtract()
sns.set_palette("pastel")

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

# ----------------- DISPLAY ANALYSIS -----------------
def display_analysis(selected_user, df):
    st.markdown("### 📊 Top Statistics")
    num_messages, words, num_media, num_links = fetch_stats(selected_user, df)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Messages", num_messages)
    col2.metric("Total Words", words)
    col3.metric("Media Shared", num_media)
    col4.metric("Links Shared", num_links)

    # Monthly timeline
    st.markdown("### 📅 Monthly Timeline")
    timeline = monthly_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(timeline['time'], timeline['messages'], color="#FF6F61", marker='o')
    plt.xticks(rotation=45)
    sns.despine()
    st.pyplot(fig)

    # Daily timeline
    st.markdown("### 🗓 Daily Timeline")
    daily = daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(daily['only_date'], daily['messages'], color="#6B5B95", marker='o')
    plt.xticks(rotation=45)
    sns.despine()
    st.pyplot(fig)

    # Activity Map
    st.markdown("### 📈 Activity Map")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Most Busy Day")
        busy_day = week_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_day.index, busy_day.values, color=sns.color_palette("Set2", len(busy_day)))
        plt.xticks(rotation=45)
        sns.despine()
        st.pyplot(fig)
    with col2:
        st.subheader("Most Busy Month")
        busy_month = month_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values, color=sns.color_palette("Set3", len(busy_month)))
        plt.xticks(rotation=45)
        sns.despine()
        st.pyplot(fig)

    # WordCloud
    st.markdown("### 💬 WordCloud")
    wc = create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(fig)

    # Peak hours
    st.markdown("### 🕒 Peak Chatting Hours")
    hourly = hourly_activity(selected_user, df)
    fig, ax = plt.subplots()
    ax.bar(hourly['hour'], hourly['messages'], color=sns.color_palette("pastel", len(hourly)))
    ax.set_xlabel("Hour (0–23)")
    ax.set_ylabel("Messages")
    plt.xticks(range(0,24))
    sns.despine()
    st.pyplot(fig)

    # Most common words
    st.markdown("### 📄 Most Common Words")
    common_words = most_common_words(selected_user, df)
    fig, ax = plt.subplots()
    ax.barh(common_words[0], common_words[1], color=sns.color_palette("Set2", len(common_words)))
    plt.xticks(rotation=45)
    sns.despine()
    st.pyplot(fig)

    # Emoji analysis
    st.markdown("### 😊 Emoji Analysis")
    emoji_df = emoji_helper(selected_user, df)
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig, ax = plt.subplots()
        ax.pie(emoji_df['count'], labels=emoji_df['emoji'], autopct='%0.1f%%',
               colors=sns.color_palette("Set3", len(emoji_df)), startangle=140, shadow=True)
        st.pyplot(fig)

# ----------------- DISPLAY INSIGHTS & REPORT -----------------
def display_insights(selected_user, df):
    st.markdown("### 🧠 Smart Insights")
    insights = smart_insights(selected_user, df)
    for insight in insights:
        st.write(insight)

    # Download report
    num_messages, words, num_media, num_links = fetch_stats(selected_user, df)
    busy_day = week_activity_map(selected_user, df).idxmax()
    busy_month = month_activity_map(selected_user, df).idxmax()
    peak_hour = hourly_activity(selected_user, df).sort_values(by='messages', ascending=False).iloc[0]['hour']

    report_df = pd.DataFrame({
        'Metric': [
            'User', 'Total Messages', 'Total Words', 'Media Shared',
            'Links Shared', 'Most Active Day', 'Most Active Month', 'Peak Hour'
        ],
        'Value': [
            selected_user, num_messages, words, num_media,
            num_links, busy_day, busy_month, peak_hour
        ]
    })

    csv = report_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Summary Report (CSV)", csv, file_name="whatsapp_report.csv", mime="text/csv")

