import streamlit as st
import zipfile
import preprocessor, helper

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
            helper.display_analysis(selected_user, df)

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
            helper.display_insights(selected_user, df)





