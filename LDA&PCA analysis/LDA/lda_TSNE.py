import pandas as pd
import numpy as np
import nltk
import re
from nltk.stem.snowball import SnowballStemmer
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import random

#visualization packages
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
import seaborn as sns

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()

def clean_text(text):
    list_of_cleaning_signs = ['\x0c','\n']
    for sign in list_of_cleaning_signs:
        text = text.replace(sign, ' ')
    clean_text = re.sub('[^a-zA-Z]+',' ',text)
    return clean_text.lower()

#0.读取数据，并清洗
papers_data = pd.read_csv("papers.csv")
papers_data['PaperText_clean'] = papers_data['paper_text'].apply(lambda x: clean_text(x))

#1.建立TfidfVectorizer
n_features = 1000
n_topics = 8
n_top_words = 10
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=0.05, max_features=n_features, stop_words='english')

tfidf = tfidf_vectorizer.fit_transform(papers_data['PaperText_clean'] )

#2.建立LDA模型（http://scikit-learn.org/dev/auto_examples/applications/topics_extraction_with_nmf_lda.html#sphx-glr-auto-examples-applications-topics-extraction-with-nmf-lda-py）
lda = LatentDirichletAllocation(n_topics=n_topics, learning_method='online', learning_offset=50., random_state=0).fit(tfidf)

#3输出LDA模型下的每个topic关键词
print("Topics found via LDA:")
tfidf_feature_names = tfidf_vectorizer.get_feature_names()
print_top_words(nmf, tfidf_feature_names, n_top_words)

#4输出每个topic下的论文
lda_embedding = lda.transform(tfidf)
lda_embedding = (lda_embedding - lda_embedding.mean(axis=0))/lda_embedding.std(axis=0)

top_idx = np.argsort(lda_embedding,axis=0)[-3:]

count = 0
for idxs in top_idx.T:
    print("\nTopic {}:".format(count))
    for idx in idxs:
        print(papers_data.iloc[idx]['title'])
    count += 1

#5人为自定义主题词
topics = ['optimization algorithm', 'neural network application', 'reinforcement learning', 'bayesian method', 'image recognition', 'artificial neuron design', 'graph theory', 'kernel method']

#6建立tsne矩阵
tsne = TSNE(random_state=3211)
tsne_embedding = tsne.fit_transform(lda_embedding)
tsne_embedding = pd.DataFrame(tsne_embedding,columns=['x','y'])
tsne_embedding['hue'] = lda_embedding.argmax(axis=1)

#7.自定义颜色
colors = np.array([[ 0.89411765,  0.10196079,  0.10980392,  1. ],
 [ 0.22685121,  0.51898501,  0.66574396,  1. ],
 [ 0.38731259,  0.57588621,  0.39148022,  1. ],
 [ 0.7655671 ,  0.38651289,  0.37099578,  1. ],
 [ 1.        ,  0.78937332,  0.11607843,  1. ],
 [ 0.75226453,  0.52958094,  0.16938101,  1. ],
 [ 0.92752019,  0.48406   ,  0.67238756,  1. ],
 [ 0.60000002,  0.60000002,  0.60000002,  1. ]])

legend_list = []

for i in range(len(topics)):
    color = colors[i]
    legend_list.append(mpatches.Ellipse((0, 0), 1, 1, fc=color))

#8。画出TSNE图（高维数据可视化）
matplotlib.rc('font',family='monospace')
plt.style.use('ggplot')


fig, axs = plt.subplots(3,2, figsize=(10, 15), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .1, wspace=0)

axs = axs.ravel()

count = 0
legend = []
for year, idx in zip([1991,1996,2001,2006,2011,2016], range(6)):
    data = tsne_embedding[papers_data['year']<=year]
    scatter = axs[idx].scatter(data=data,x='x',y='y',s=6,c=data['hue'],cmap="Set1")
    axs[idx].set_title('published until {}'.format(year),**{'fontsize':'10'})
    axs[idx].axis('off')

plt.suptitle("1987-2015 NIPS Papers clustered by LDA topic analysis",**{'fontsize':'14','weight':'bold'})


fig.legend(legend_list,topics,loc=(0.1,0.89),ncol=3)
plt.subplots_adjust(top=0.85)

plt.show()
