import pandas as pd
import re
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:am|pm)\s-\s'

    messages = re.split(pattern, data)[1:]
    dates=re.findall(pattern,data)
    df=pd.DataFrame({'user_messages':messages,'message_date':dates})
#convert message data type
    df['message_date'] = pd.to_datetime(
    df['message_date']
      .str.replace('\u202f', ' ', regex=False)
      .str.replace(' -', '', regex=False)
      .str.strip(),
    format='%d/%m/%y, %I:%M %p')

    df.rename(columns={'message_date':'date'},inplace=True)
    users = []
    messages = []

    for message in df['user_messages']:
     entry = re.split(r'([\w\W]+?):\s', message)
     if entry[1:]:
        users.append(entry[1])
        messages.append(entry[2])
     else:
        users.append('group_notification')
        messages.append(entry[0])

    df['users'] = users
    df['messages'] = messages
    df.drop(columns='user_messages', inplace=True)
    df['year']=df['date'].dt.year
    df['month']=df['date'].dt.month_name() 
    df['day']=df['date'].dt.day
    df['hour']=df['date'].dt.hour
    df['hour']=df['date'].dt.hour
     
    return df 