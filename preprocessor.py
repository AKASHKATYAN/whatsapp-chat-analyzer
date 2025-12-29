import pandas as pd
import re

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?(?:am|pm))?\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({
        'user_messages': messages,
        'message_date': dates
    })

    # Ensure messages are strings
    df['user_messages'] = df['user_messages'].astype(str)

    # Safely convert message_date to string only if not null
    df['message_date'] = df['message_date'].apply(lambda x: str(x) if isinstance(x, str) else '')

    # Now it's safe to use .str methods
    df['message_date'] = pd.to_datetime(
        df['message_date'].str.replace('\u202f', ' ', regex=False)
                       .str.replace(' -', '', regex=False)
                       .str.strip(),
        dayfirst=True,
        errors='coerce'
    )

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages_list = []

    for message in df['user_messages']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages_list.append(entry[2])
        else:
            users.append('group_notification')
            messages_list.append(entry[0])

    df['users'] = users
    df['messages'] = messages_list

    # Ensure all messages are strings
    df['messages'] = df['messages'].astype(str)

    # Extract datetime features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['only_date'] = df['date'].dt.date

    return df
