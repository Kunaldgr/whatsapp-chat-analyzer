import re
import pandas as pd

def preprocess(data):
    pattern = r"\[\d{2}/\d{2}/\d{2},\s*\d{1,2}:\d{2}:\d{2}(?:\s|\u202f)[AP]M\]"
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    dates = [d.strip("[]").replace("\u202f", " ") for d in dates]

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M:%S %p')

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\s]+?):\s', message, maxsplit=1)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute

    return df