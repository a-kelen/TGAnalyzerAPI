from preprocessing.tokenize import get_channel_df_with_tokens
from preprocessing.counting import count_words

def run_preprocessing(channels):
    for channel in channels:
        channel_id = channel['_id']
        df = get_channel_df_with_tokens(channel['name'])
        counted_words = count_words(df)

        

