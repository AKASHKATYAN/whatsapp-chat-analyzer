import pandas as pd
import re

def preprocess(data):

    # --------- PATTERN 1: OLD FORMAT ----------
    pattern_old = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?(?:am|pm))?\s-\s'

    # --------- PATTERN 2: NEW BRACKET FORMAT ----------
    pattern_new = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\u202f?(?:AM|PM)\]'

    # Detect which pattern exists
    if re.search(pattern_new, data):
        pattern = pattern_new
        messages = re.split(pattern, data)[1:]
        dates = re.findall(pattern, data)
        dates = [d.strip('[]') for d in dates]
    else:
        pattern = pattern_old
        messages = re.split(pattern, data)[1:]
        dates = re.findall(pattern, data)

    df = pd.DataFrame({
        'user_messages': messages,
        'message_date': dates
    })

    # ---------- DATE PARSING ----------
    df['message_date'] = (
        df['message_date']
        .str.replace('\u202f', ' ', regex=False)
        .str.replace(' -', '', regex=False)
        .str.strip()
    )

    df['message_date'] = pd.to_datetime(
        df['message_date'],
        dayfirst=True,
        errors='coerce'
    )

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # ---------- USER & MESSAGE SPLIT ----------
    users = []
    messages_clean = []

    for message in df['user_messages']:
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)
        if len(entry) > 2:
            users.append(entry[1])
            messages_clean.append(entry[2])
        else:
            users.append('group_notification')
            messages_clean.append(entry[0])

    df['users'] = users
    df['messages'] = messages_clean
    df.drop(columns='user_messages', inplace=True)

    # ---------- TIME FEATURES ----------
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['only_date'] = df['date'].dt.date

    return df
