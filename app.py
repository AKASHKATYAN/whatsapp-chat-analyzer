import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
from wordcloud import WordCloud
import preprocessor, helper

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")
sns.set_palette("pastel")

# ----------------- SESSION STATE FOR PAGE -----------------
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

def set_page(page_name):
    st.session_state.page = page_name

# ----------------- SIDEBAR NAVIGATION -----------------
st.sidebar.title("Navigation")
st.sidebar.button("Home", on_click=set_page, args=["Home"])
st.sidebar.button("Analysis", on_click=set_page, args=["Analysis"])
st.sidebar.button("Insights & Report", on_click=set_page, args=["Insights & Report"])

# ----------------- PAGE CONTAINERS -----------------
home_page = st.container()
analysis_page = st.container()
insights_page = st.container()

# ----------------- HOME PAGE -----------------
with home_page:
    if st.session_state.page == 'Home':
        st.markdown("""
            <div style="background-color:#6C63FF;padding:25px;border-radius:15px">
                <h1 style="color:white;text-align:center;">📱 WhatsApp Chat Analyzer</h1>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### Welcome!")
        st.write("""
            Analyze your WhatsApp chats with beautiful visualizations:

            - Top statistics
            - Monthly & daily timelines
            - Activity maps
            - WordCloud & emoji analysis
            - Peak chatting hours
            - Downloadable summary report
        """)
        st.markdown("### Quick Guide")
        st.write("""
            1. Export your WhatsApp chat (.txt or .zip)  
            2. Go to the Analysis page and upload your chat  
            3. Select a user (or Overall)  
            4. Click 'Show Analysis' to view charts  
            5. Go to Insights & Report page for smart insights & report download
        """)

# ----------------- ANALYSIS PAGE -----------------
with analysis_page:
    if st.session_state.page == 'Analysis':
        uploaded_file = st.file_uploader("Upload chat (.txt or .zip)", type=["txt","zip"], key="analysis")
        if uploaded_file:
            # ----------------- HANDLE FILE -----------------
            if uploaded_file.name.endswith(".zip"):
                z = zipfile.ZipFile(uploaded_file)
                txt_files = [f for f in z.namelist() if f.endswith(".txt")]
                if txt_files:
                    data = z.read(txt_files[0]).decode("utf-8", errors="ignore")
                else:
                    st.error("No .txt file in ZIP")
                    st.stop()
            else:
                data = uploaded_file.getvalue().decode("utf-8", errors="ignore")

            df = preprocessor.preprocess(data)

            # ----------------- SELECT USER -----------------
            user_list = df['users'].unique().tolist()
            if 'group_notification' in user_list:
                user_list.remove('group_notification')
            user_list.sort()
            user_list.insert(0, "Overall")
            selected_user = st.selectbox("Select User", user_list)

            if st.button("Show Analysis"):
                helper.display_analysis(selected_user, df)

# ----------------- INSIGHTS & REPORT PAGE -----------------
with insights_page:
    if st.session_state.page == 'Insights & Report':
        uploaded_file = st.file_uploader("Upload chat (.txt or .zip)", type=["txt","zip"], key="insights")
        if uploaded_file:
            # ----------------- HANDLE FILE -----------------
            if uploaded_file.name.endswith(".zip"):
                z = zipfile.ZipFile(uploaded_file)
                txt_files = [f for f in z.namelist() if f.endswith(".txt")]
                if txt_files:
                    data = z.read(txt_files[0]).decode("utf-8", errors="ignore")
                else:
                    st.error("No .txt file in ZIP")
                    st.stop()
            else:
                data = uploaded_file.getvalue().decode("utf-8", errors="ignore")

            df = preprocessor.preprocess(data)

            # ----------------- SELECT USER -----------------
            user_list = df['users'].unique().tolist()
            if 'group_notification' in user_list:
                user_list.remove('group_notification')
            user_list.sort()
            user_list.insert(0, "Overall")
            selected_user = st.selectbox("Select User", user_list)

            if st.button("Show Insights"):
                helper.display_insights(selected_user, df)




