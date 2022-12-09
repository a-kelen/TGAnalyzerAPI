import os
import pandas as pd
from nltk.tokenize import word_tokenize
import string
import stop_words

en_stop_words = stop_words.get_stop_words('en')
ua_stop_words = stop_words.get_stop_words('uk')
ru_stop_words = stop_words.get_stop_words('ru')

def get_files_for_channel(target_folder):
    files = os.listdir(target_folder)
    files = list(filter(lambda x: x.startswith('message'), files))

    return [os.path.join(target_folder, x) for x in files]

def get_messages(message_path):
    messages = pd.read_csv(message_path)
    messages = messages[pd.notna(messages.message)]
    messages = messages[['id', 'message', 'date', 'views', 'forwards']]

    return messages

def tokenize(text):
    tokens = word_tokenize(text)
    tokens = [token for token in tokens if token not in string.punctuation]
    tokens = [token.lower() for token in tokens if token.isalpha()]
    tokens = [token for token in tokens if token not in en_stop_words]
    tokens = [token for token in tokens if token not in ua_stop_words]
    tokens = [token for token in tokens if token not in ru_stop_words]
    
    return tokens

def get_channel_df_with_tokens(channel_name):
    target_folder = os.path.join('messages', channel_name)
    files = get_files_for_channel(target_folder)

    df = pd.concat(map(get_messages, files))
    token_list = df.message.apply(lambda x: tokenize(x))
    df['tokens'] = token_list
    df.date = pd.to_datetime(df.date)
    df.date = df.date.apply(lambda x: x.date())

    return df

