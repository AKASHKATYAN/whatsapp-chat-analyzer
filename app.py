import streamlit as st
import zipfile
import io
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import preprocessor, helper

sns.set_palette("pastel")

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")

# ----------------- SIDEBAR NAVIGATION -----------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Analysis", "Insights & Report"])

# ----------------- FILE UPLOAD FUNCTION -----------------
def load_chat(uploaded_file):
    if uploaded_file.name.endswith(".zip"):
        z = zipfile.ZipFile(uploaded_file)
        txt_files = [f for f in z.namelist() if f.endswith(".txt")]
        if txt_files:
            data = z.read(txt_files[0]).decode("utf-8", errors="ignore")
        else:
            st.error("No .txt file found in ZIP")
            st.stop()
    else:
        data = uploaded_file.getvalue().decode("utf-8", errors="ignore")
    df = preprocessor.preprocess(data)
    return df

# ----------------- HOME PAGE -----------------
if page == "Home":
    st.markdown("""
        <div style="background-color:#6C63FF;padding:25px;border-radius:15px">
            <h1 style="color:white;text-align:center;">📱 WhatsApp Chat Analyzer</h1>
        </div>
    """, unsafe_allow_html=True)
    st.write("Welcome! This app can help you:")
    st.write("""
        - View top stats of your chat  
        - Monthly & daily timelines  
        - Activity maps  
        - WordCloud & emoji analysis  
        - Peak chatting hours  
        - Download summary report  
    """)
    st.markdown("### Quick Guide")
    st.write("""
        1. Export your WhatsApp chat (.txt or .zip)  
        2. Go to the Analysis page and upload your chat  
        3. Select user or Overall  
        4. Click 'Show Analysis' to view charts  
        5. Go to Insights & Report page for smart insights & downloadable summary
    """)

# ----------------- ANALYSIS PAGE -----------------
elif page == "Analysis":
    uploaded_file = st.file_uploader("Upload chat (.txt or .zip)", type=["txt","zip"], key="analysis")
    if uploaded_file:
        df = load_chat(uploaded_file)

        # User selection
        user_list = df['users'].unique().tolist()
        if 'group_notification' in user_list:
            user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "Overall")
        selected_user = st.selectbox("Select User", user_list)

        if st.button("Show Analysis"):
            # Top Statistics
            num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)
            st.markdown("### 📊 Top Statistics")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Messages", num_messages)
            col2.metric("Total Words", words)
            col3.metric("Media Shared", num_media)
            col4.metric("Links Shared", num_links)

            # Monthly Timeline
            st.markdown("### 📅 Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['messages'], color="#FF6F61", marker='o')
            plt.xticks(rotation=45)
            sns.despine()
            st.pyplot(fig)

            # Daily Timeline
            st.markdown("### 🗓 Daily Timeline")
            daily = helper.daily_timeline(selected_user, df)
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

            # WordCloud
            st.markdown("### 💬 WordCloud")
            wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            plt.imshow(wc, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(fig)

            # Peak Chatting Hours
            st.markdown("### 🕒 Peak Chatting Hours")
            hourly = helper.hourly_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(hourly['hour'], hourly['messages'], color=sns.color_palette("pastel", len(hourly)))
            ax.set_xlabel("Hour (0–23)")
            ax.set_ylabel("Messages")
            plt.xticks(range(0,24))
            sns.despine()
            st.pyplot(fig)

            # Most Common Words
            st.markdown("### 📄 Most Common Words")
            common_words = helper.most_common_words(selected_user, df)
            fig, ax = plt.subplots()
            ax.barh(common_words[0], common_words[1], color=sns.color_palette("Set2", len(common_words)))
            plt.xticks(rotation=45)
            sns.despine()
            st.pyplot(fig)

            # Emoji Analysis
            st.markdown("### 😊 Emoji Analysis")
            emoji_df = helper.emoji_helper(selected_user, df)
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df['count'], labels=emoji_df['emoji'], autopct='%0.1f%%',
                       colors=sns.color_palette("Set3", len(emoji_df)), startangle=140, shadow=True)
                st.pyplot(fig)

# ----------------- INSIGHTS & REPORT PAGE -----------------
elif page == "Insights & Report":
    uploaded_file = st.file_uploader("Upload chat (.txt or .zip)", type=["txt","zip"], key="insights")
    if uploaded_file:
        df = load_chat(uploaded_file)

        # User selection
        user_list = df['users'].unique().tolist()
        if 'group_notification' in user_list:
            user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "Overall")
        selected_user = st.selectbox("Select User", user_list)

        if st.button("Show Insights"):
            # Smart Insights
            st.markdown("### 🧠 Smart Insights")
            insights = helper.smart_insights(selected_user, df)
            for insight in insights:
                st.write(insight)

            # Download Summary Report
            num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)
            busy_day = helper.week_activity_map(selected_user, df).idxmax()
            busy_month = helper.month_activity_map(selected_user, df).idxmax()
            peak_hour = helper.hourly_activity(selected_user, df).sort_values(by='messages', ascending=False).iloc[0]['hour']

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





