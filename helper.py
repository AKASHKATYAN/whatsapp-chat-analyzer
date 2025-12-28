from urlextract import URLExtract
import matplotlib.pyplot as plt

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    num_messages = df.shape[0]

    #number of words
    words = []
    for message in df['messages']:
        words.extend(message.split())

    # number of media messages
    num_media_messages = df[df['messages'] == '<Media omitted>\n'].shape[0]

    #number of links shared 
    links = []
    for message in df['messages']:
        links.extend(extract.find_urls(message))


    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    x=df['users'].value_counts().head()
    df=round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','count':'percent'})
    return x,df



