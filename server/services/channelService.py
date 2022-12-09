from bson.objectid import ObjectId

from server import database
from server.mappers import map_channel, map_channel_line
from server.tg_utils import fill_gaps

def get_channels():
    return [map_channel(x) for x in database.channels.find()]

def get_channel_top(channel_id, page, page_size, type):
    _skip = (page - 1) * page_size
    data = database.channel_words.find_one({'channel': ObjectId(channel_id)})
    return {
        'words': data['words'][_skip:_skip+page_size],
        'total': len(data['words'])
    }

def get_channel_word_line(channel_id, word):
    history = list(database.words_by_day.find({'channel': ObjectId(channel_id), 'words.word': word}, {'date': '$date', 'words.$': 1}))
    res = [map_channel_line(x) for x in history]
    return fill_gaps(res)

def channel_vocabular_compare(channel_left_id, channel_right_id):
    cw_left = database.channel_words.find_one({'channel': ObjectId(channel_left_id)})
    cw_right = database.channel_words.find_one({'channel': ObjectId(channel_right_id)})
    arr_left = cw_left['words']
    arr_right = cw_right['words']
    set_left = set([x['word'] for x in arr_left])
    set_right =set([x['word'] for x in arr_right])
    all_words = set_left | set_right
    common_words = set_left & set_right
    return len(common_words) / len(all_words) * 100

def compare_channels_by_word(channel_left_id, channel_right_id, word):
    history_left = list(database.words_by_day.find({'channel': ObjectId(channel_left_id), 'words.word': word}, {'date': '$date', 'words.$': 1}))
    history_right = list(database.words_by_day.find({'channel': ObjectId(channel_right_id), 'words.word': word}, {'date': '$date', 'words.$': 1}))
    
    return {
        'left_line': [map_channel_line(x) for x in history_left],
        'right_line': [map_channel_line(x) for x in history_right],
    }

def get_channel_word_stats(channel_id, word):
    ch = database.channel_words.find_one({'channel': ObjectId(channel_id), 'words.word': word}, {'words.$': 1})
    target_word = ch['words'][0]
    return target_word