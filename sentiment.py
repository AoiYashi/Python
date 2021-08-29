import glob
from typing import Text

#loading data 
pos_files = glob.glob('data/aclImdb/train/pos/*.txt') 
pos_reviews = []
for file in pos_files:
    with open(file, errors='ignore') as stream:
        content = stream.read()
        words = content.lower().replace('<br />', ' ').replace('.', ' ').split()
        pos_reviews.append(words)

neg_files = glob.glob('data/aclImdb/train/neg/*.txt') 
neg_reviews = []
for file in neg_files:
    with open(file, errors='ignore') as stream:
        content = stream.read()
        words = content.lower().replace('<br />', ' ').replace('.', ' ').split()
        neg_reviews.append(words)

#training / learning
#word -> liczba wystapien
words_count = {}
words_count_pos = {}
words_count_neg = {}

for review in pos_reviews:
    for word in set(review):
        words_count[word] = words_count.get(word, 0) + 1
        words_count_pos[word] = words_count_pos.get(word, 0) + 1

for review in neg_reviews:
    for word in set(review):
        words_count[word] = words_count.get(word, 0) + 1
        words_count_neg[word] = words_count_neg.get(word, 0) + 1

words_sentiment = {}
for word in words_count.keys():
    if words_count[word] >= 50:
        pos = words_count_pos.get(word, 0)
        neg = words_count_neg.get(word, 0)
        all_ = words_count[word]
        words_sentiment[word] = (pos - neg) / all_

#Vizualizing Words Sentiments
sorted_ = sorted(words_sentiment.items(), key=lambda x: x[1])
print("Most negative")
for word, sentiment in sorted_[:10]:
    print(f"* {sentiment:8f} {words_count[word]:6} {word}")
print("Most positive")
for word, sentiment in sorted_[-10:]:
    print(f"* {sentiment:8f} {words_count[word]:6} {word}")

# testing train score
def compute_sentiment(words, debug=False):
    sentiment = 0
    for word in words:
        word_sentiment = words_sentiment.get(word, 0)
        word_count = words_count.get(word, 0)
        if debug:
             print(f"{word_count:6} {word_sentiment:6.3f} {word:20}" )
        sentiment += word_sentiment
    sentiment /= len(words)
    return sentiment

n_correct = 0
for review in pos_reviews:
    if compute_sentiment(review) > 0:
        n_correct += 1
for review in neg_reviews:
    if compute_sentiment(review) < 0:
        n_correct += 1
train_score = n_correct / len(pos_reviews + neg_reviews)
print("Train score: ", train_score)

# testing - intearactive
text = input('Enter comment: ')  
words = text.lower().replace('<br />', ' ').replace('.', ' ').split()
sentiment =  compute_sentiment(words, debug=True)
sentiment /= len(words)
print('Sentiment:', sentiment)