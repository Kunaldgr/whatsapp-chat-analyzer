from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()
def fetch_stats(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words=[]
    for message in df['message']:
        words.extend(message.split())

    media_messages = df[df['message'].str.contains(r"<attached:", na=False)].shape[0]

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    num_links = len(links)

    return num_messages, len(words) , media_messages , num_links

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'percent', 'user': 'name'})
    return x,df

def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    import re

    df['message'] = df['message'].str.lower()
    df['message'] = df['message'].apply(lambda x: re.sub(r'[\u200e\u200f\u202a-\u202e\u00a0]', '', x))

    df['message'] = df['message'].str.strip()

    temp = df[(df['user'] != 'group_notification') &
              (df['message'] != '<media omitted>') &
              (df['message'] != '') &
              (~df['message'].str.startswith('<attached:'))]

    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    import re

    df['message'] = df['message'].str.lower()
    df['message'] = df['message'].apply(lambda x: re.sub(r'[\u200e\u200f\u202a-\u202e\u00a0]', '', x))

    df['message'] = df['message'].str.strip()

    temp = df[(df['user'] != 'group_notification') &
              (df['message'] != '<media omitted>') &
              (df['message'] != '') &
              (~df['message'].str.startswith('<attached:'))]

    words = []
    for message in temp['message']:
        for word in message.split():
            if word not in stop_words and word.strip() != '':
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_counts = Counter(emojis).most_common(10)

    emoji_df = pd.DataFrame(emoji_counts, columns=['emoji', 'count'])

    return emoji_df


