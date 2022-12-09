def map_channel(obj):
    return {
        'id': str(obj['_id']),
        'name': obj['name'],
        'total_messages': obj['total_messages'],
        'messages_by_day': obj['messages_by_day'],
    }

def map_word(obj):
    return {
        'id': str(obj['_id']),
        'word': obj['word'],
        'count': obj['count'],
    }

def map_channel_line(obj):
    return {
        'date': obj['date'],
        'count': obj['words'][0]['count']
    }
