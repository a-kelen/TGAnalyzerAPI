from bson.objectid import ObjectId

from server import database
from server.tg_utils import fill_gaps
from server.mappers import map_word, map_channel_line

def get_all_words():
    return [map_word(x) for x in database.words.find()]

def get_words(page, page_size, type):
    _skip = (page - 1) * page_size
    return [map_word(x) for x in database.words.find().sort('count', -1).skip(_skip).limit(page_size)]


def get_global_word_line(word):
    history = list(database.words_by_day.find({'words.word': word}, {'date': '$date', 'words.$': 1}))
    res = [map_channel_line(x) for x in history]
    return fill_gaps(res)

def get_global_word_stats(word):
    dispersion_sum = sum([x['words'][0]['dispersion'] for x in database.channel_words.find({'words.word': word}, {'date': '$date', 'words.$': 1})])
    ch_count = database.channels.count()
    return dispersion_sum / ch_count