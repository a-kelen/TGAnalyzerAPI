from processing.tokenize import get_channel_df_with_tokens
from processing.counting import count_words
from processing.saving import insert_words_by_days, additional_processing
import database

def run_preprocessing(channels):
    for channel in channels:
        channel_id = channel['_id']
        df = get_channel_df_with_tokens(channel['name'])
        counted_words = count_words(df)
        insert_words_by_days(channel_id, counted_words, database.words_by_day)

    additional_processing()
