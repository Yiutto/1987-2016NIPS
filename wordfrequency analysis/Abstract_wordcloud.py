import pandas as pd
import re
import nltk
# from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from pytagcloud import create_tag_image,make_tags
from pytagcloud.lang.counter import get_tag_counts
papers_data = pd.read_csv('2015Papers.csv')
# stemmer = SnowballStemmer('english')

def clean_text(text):
    list_of_cleaning_signs = ['\x0c','\n']
    for sign in list_of_cleaning_signs:
        text = text.replace(sign, ' ')
    clean_text = re.sub('[^a-zA-Z]+',' ',text)
    return clean_text.lower()

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

def wordfrequencies(data):
    # vectorizer =CountVectorizer(tokenizer=tokenize_and_stem, stop_words='english')
    vectorizer =CountVectorizer(stop_words='english')
    vectort_fit = vectorizer.fit_transform(data)
    words = vectorizer.get_feature_names()
    counts = vectort_fit.toarray().sum(axis=0)
    wordfrequencies = {}
    for key, value in zip(words, counts):
        wordfrequencies[key] = value
    return wordfrequencies

#0.导入数据
papers_data = pd.read_csv('2015Papers.csv')
#1.数据清洗，去除非英文单词
Abstact_clean = papers_data['Abstract'].apply(lambda x:clean_text(x))
#2.调用函数，生成词频字典
Abstract_wordfrequencies = wordfrequencies(Abstact_clean)
#3.提取前100个高词频
Abstract_wordfrequencies100 = sorted(Abstract_wordfrequencies.items(), key=lambda d:d[1], reverse= True)[0:100]
#4.建立词标签，生成词云图
Abstract_tags = make_tags(Abstract_wordfrequencies100)
create_tag_image(Abstract_tags, '2015Abstract_wordtags.png', size=(510, 470), fontname='Lobster')
