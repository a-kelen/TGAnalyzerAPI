import database
from pymongo import UpdateOne
from bson.objectid import ObjectId

def insert_words_by_days(channel_id, counts, collection):
    channel_obj = database.channels.find_one({"name": ObjectId(channel_id)})
    rows = [{
        "channel": channel_obj["_id"],
        "date": key,
        "words": list(map(lambda x: {"word": x.word, "count": x.count}, counts[key])) 
    }  for key in counts]
     
    collection.insert_many(rows)

def additional_processing():
    db_channels = [x for x in database.channels.find()]

    words_arr = [x for x in database.words_by_day.find()]
    for ch in db_channels:
        channel_total_words = dict()
        channel_history = list(filter(lambda x: x['channel'] == ch['_id'], words_arr))
        splash_words = [x['words'] for x in channel_history]

        for arr in splash_words:
            for x in arr:
                w = x['word']
                if channel_total_words.get(w) == None:
                    channel_total_words[w] = x['count']
                else:
                    channel_total_words[w] += x['count'] 

        total_words_list = [{'word': x, 'count': channel_total_words[x]} for x in channel_total_words]
        sorted_list = sorted(total_words_list, reverse=True, key=lambda d: d['count']) 
        filtred_list = [x for x in sorted_list if x['count'] > 50]
        word_insertions = [UpdateOne({'word': wc['word']}, {'$inc': {'count': wc['count']}}, upsert=True) for wc in filtred_list]
        database.words.bulk_write(word_insertions)
        calculated_list = calculate_dispersion(channel_history, filtred_list)
        database.channel_words.insert_one({ 'channel': ch['_id'], 'words': calculated_list })

def calculate_dispersion(channel_history, lst):
    for wc in lst:
        line = get_line(channel_history, wc['word'])
        nums = [x['count'] for x in line]
        d = get_dispertion(nums)
        wc['dispersion'] = d
    return lst

def get_point(word_row, word):
    co = [x for x in word_row['words'] if x['word'] == word]
    _count = 0
    if len(co) > 0:
        _count = co[0]['count']
    
    return {'date': word_row['date'], 'count': _count }

def get_line(history, word):
    return list(map(lambda x: get_point(x, word), history))

def get_dispertion(nums):
    len_count = len(nums)
    sum_count = sum(nums)
    avg_count = sum_count / len_count 

    acc = 0
    for i in range(len_count):
        acc += abs(avg_count - nums[i])

    return acc / len_count