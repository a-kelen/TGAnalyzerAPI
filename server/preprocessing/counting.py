from tg_utils import find_in_list

class CountedWord:
    def __init__(self, word, count):
        self.word = word
        self.count = count

def count_words(df_messages):
    counts = dict()
    for i, row in df_messages.iterrows():
        key = row.date.strftime("%d/%m/%Y")
        if key not in counts:
            counts[key] = []

        for word in row.tokens:
            target_word = find_in_list(counts[key], word)
            if target_word == None:
                counts[key].append(CountedWord(word, 1))
            else:
                target_word.count += 1
                
    return counts
