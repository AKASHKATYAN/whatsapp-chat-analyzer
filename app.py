import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import preprocessor, helper

st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")

# Set Seaborn palette
sns.set_palette("pastel")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Analysis", "Insights & Report"])

# ----------------- HOME PAGE -----------------
if page == "Home":
    st.markdown("""
        <div style="background-color:#6C63FF;padding:25px;border-radius:15px">
            <h1 style="color:white;text-align:center;font-family:Arial, Helvetica, sans-serif;">
                📱 WhatsApp Chat Analyzer
            </h1>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### Welcome to WhatsApp Chat Analyzer!")
    st.write("""
    Analyze your WhatsApp chats with beautiful visualizations and insights.
    
    **Features include:**
    - Top statistics: total messages, words, media shared, links shared
    - Monthly and daily timelines
    - Activity maps: busiest days and months
    - WordClouds and emoji analysis
    - Peak chatting hours
    - AI-style smart insights
    - Downloadable summary report
    """)

    st.markdown("### Quick Guide")
    st.write("""
    1. Export your WhatsApp chat (.txt) file from your phone.
    2. Go to the 'Analysis' page and upload the file.
    3. Select a user (or 'Overall') to analyze.
    4. Click 'Show Analysis' to view charts and statistics.
    5. Visit 'Insights & Report' page to get smart insights and download a summary report.
    """)

# ----------------- ANALYSIS PAGE -----------------
elif page == "Analysis":
    uploaded_file = st.file_uploader("Choose a WhatsApp chat file (.txt)", type=["txt"], key="analysis")
    if uploaded_file is not None:
        data = uploaded_file.getvalue().decode("utf-8", errors='ignore')
        df = preprocessor.preprocess(data)

        # User selection
        user_list = df['users'].unique().tolist()
        if 'group_notification' in user_list:
            user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "Overall")
        selected_user = st.selectbox("Select User", user_list)

        if st.button("Show Analysis"):

            # -------- Top Stats --------
            num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)
            st.markdown("<h3 style='color:#FF5733;'>📊 Top Statistics</h3>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Messages", num_messages)
            col2.metric("Total Words", words)
            col3.metric("Media Shared", num_media)
            col4.metric("Links Shared", num_links)

            # -------- Monthly Timeline --------
            st.markdown("<h3 style='color:#33C1FF;'>📅 Monthly Timeline</h3>", unsafe_allow_html=True)
            timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['messages'], color="#FF6F61", marker='o')
            plt.xticks(rotation=45)
            sns.despine()
            st.pyplot(fig)

            # -------- Daily Timeline --------
            st.markdown("<h3 style='color:#FFB347;'>🗓 Daily Timeline</h3>", unsafe_allow_html=True)
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color="#6B5B95", marker='o')
            plt.xticks(rotation=45)
            sns.despine()
            st.pyplot(fig)

            # -------- Activity Maps --------
            st.markdown("<h3 style='color:#6C63FF;'>📈 Activity Map</h3>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Most Busy Day")
                busy_day = helper.week_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color=sns.color_palette("Set2", len(busy_day)))
                plt.xticks(rotation=45)
                sns.despine()
                st.pyplot(fig)
            with col2:
                st.subheader("Most Busy Month")
                busy_month = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color=sns.color_palette("Set3", len(busy_month)))
                plt.xticks(rotation=45)
                sns.despine()
                st.pyplot(fig)

            # -------- WordCloud --------
            st.markdown("<h3 style='color:#33C1FF;'>💬 WordCloud</h3>", unsafe_allow_html=True)
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            plt.imshow(df_wc, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(fig)

            # -------- Peak Chatting Hours --------
            st.markdown("<h3 style='color:#FF6F61;'>🕒 Peak Chatting Hours</h3>", unsafe_allow_html=True)
            hourly_df = helper.hourly_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(hourly_df['hour'], hourly_df['messages'], color=sns.color_palette("pastel", len(hourly_df)))
            ax.set_xlabel("Hour of Day (0–23)")
            ax.set_ylabel("Number of Messages")
            plt.xticks(range(0, 24))
            sns.despine()
            st.pyplot(fig)

            # -------- Most Common Words --------
            st.markdown("<h3 style='color:#FFB347;'>📄 Most Common Words</h3>", unsafe_allow_html=True)
            most_common_df = helper.most_common_words(selected_user, df)
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1], color=sns.color_palette("Set2", len(most_common_df)))
            plt.xticks(rotation=45)
            sns.despine()
            st.pyplot(fig)

            # -------- Emoji Analysis --------
            st.markdown("<h3 style='color:#6C63FF;'>😊 Emoji Analysis</h3>", unsafe_allow_html=True)
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

# ----------------- INSIGHTS & REPORT PAGE -----------------
elif page == "Insights & Report":
    uploaded_file = st.file_uploader("Upload your WhatsApp chat file (.txt)", type=["txt"], key="insights")
    if uploaded_file is not None:
        data = uploaded_file.getvalue().decode("utf-8", errors='ignore')
        df = preprocessor.preprocess(data)

        # User selection
        user_list = df['users'].unique().tolist()
        if 'group_notification' in user_list:
            user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "Overall")
        selected_user = st.selectbox("Select User", user_list)

        if st.button("Show Insights"):
            # Smart insights
            st.markdown("<h3 style='color:#FF5733;'>🧠 Smart Insights</h3>", unsafe_allow_html=True)
            insights = helper.smart_insights(selected_user, df)
            for insight in insights:
                st.write(insight)

            # Downloadable summary report
            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
            busy_day = helper.week_activity_map(selected_user, df).idxmax()
            busy_month = helper.month_activity_map(selected_user, df).idxmax()
            peak_hour = helper.hourly_activity(selected_user, df).sort_values(
                by='messages', ascending=False
            ).iloc[0]['hour']

            report_df = pd.DataFrame({
                'Metric': [
                    'User',
                    'Total Messages',
                    'Total Words',
                    'Media Shared',
                    'Links Shared',
                    'Most Active Day',
                    'Most Active Month',
                    'Peak Chatting Hour'
                ],
                'Value': [
                    selected_user,
                    num_messages,
                    words,
                    num_media_messages,
                    num_links,
                    busy_day,
                    busy_month,
                    peak_hour
                ]
            })

            csv = report_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Summary Report (CSV)",
                data=csv,
                file_name="whatsapp_chat_report.csv",
                mime="text/csv"
            )



