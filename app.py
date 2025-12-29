import streamlit as st
import pandas as pd
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.markdown("""
    <div style="background-color:#6C63FF;padding:20px;border-radius:10px">
        <h1 style="color:white;text-align:center;font-family:Arial, Helvetica, sans-serif;">
            📱 WhatsApp Chat Analyzer
        </h1>
    </div>
""", unsafe_allow_html=True)

# Set Seaborn color palette
colors = sns.color_palette("pastel")  # try "bright", "muted", "deep" for variation

st.sidebar.title('WHATSAPP CHAT ANALYZER')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8", errors='ignore')  # Safe decoding
    df = preprocessor.preprocess(data)

    # Fetch users
    user_list = df['users'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt:", user_list)

    # Show Stats
    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        st.title("TOP STATISTICS")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # Monthly Timeline
        st.markdown("<h3 style='color: #FF5733;'>MONTHLY TIMELINE</h3>", unsafe_allow_html=True)
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'], color="#FF6F61", marker='o')
        plt.xticks(rotation=45)
        sns.despine()
        st.pyplot(fig)

        # Daily Timeline
        st.markdown("<h3 style='color: #33C1FF;'>DAILY TIMELINE</h3>", unsafe_allow_html=True)
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color="#6B5B95", marker='o')
        plt.xticks(rotation=45)
        sns.despine()
        st.pyplot(fig)

        # Activity Map
        st.markdown("<h3 style='color: #FFB347;'>Activity Map</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.header('Most Busy Day')
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color=sns.color_palette("Set2", len(busy_day)))
            plt.xticks(rotation=45)
            sns.despine()
            st.pyplot(fig)
        with col2:
            st.header('Most Busy Month')
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color=sns.color_palette("Set3", len(busy_month)))
            plt.xticks(rotation=45)
            sns.despine()
            st.pyplot(fig)

        # Most Active Users
        if selected_user == 'Overall':
            st.markdown("<h3 style='color: #FF5733;'>Most Active Users</h3>", unsafe_allow_html=True)
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color=sns.color_palette("pastel", len(x)))
                plt.xticks(rotation=45)
                sns.despine()
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.markdown("<h3 style='color: #33C1FF;'>WordCloud</h3>", unsafe_allow_html=True)
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(fig)

        # Most Common Words
        st.markdown("<h3 style='color: #FFB347;'>Most Common Words</h3>", unsafe_allow_html=True)
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color=sns.color_palette("Set2", len(most_common_df)))
        plt.xticks(rotation=45)
        sns.despine()
        st.pyplot(fig)

        # Emoji Analysis
        st.markdown("<h3 style='color: #FF6F61;'>Emoji Analysis</h3>", unsafe_allow_html=True)
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(
                emoji_df['count'],
                labels=emoji_df['emoji'],
                autopct='%0.1f%%',
                colors=sns.color_palette("Set3", len(emoji_df)),
                startangle=140,
                shadow=True
            )
            st.pyplot(fig)

        # Peak Chatting Hours
        st.markdown("<h3 style='color: #33C1FF;'>Peak Chatting Hours</h3>", unsafe_allow_html=True)
        hourly_df = helper.hourly_activity(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(hourly_df['hour'], hourly_df['messages'], color=sns.color_palette("pastel", len(hourly_df)))
        ax.set_xlabel("Hour of Day (0–23)")
        ax.set_ylabel("Number of Messages")
        plt.xticks(range(0, 24))
        sns.despine()
        st.pyplot(fig)

        # Smart Insights
        st.markdown("<h3 style='color: #FF5733;'>🧠 Smart Insights</h3>", unsafe_allow_html=True)
        insights = helper.smart_insights(selected_user, df)
        for insight in insights:
            st.write(insight)

