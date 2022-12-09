from pymongo import MongoClient
import settings

client = MongoClient(settings.mongodb_uri, settings.port)
db = client[settings.db_name]

words_by_day = db["words_by_day"]
channels = db["Channels"]
words = db["words"]
channel_words = db["channel_words"]