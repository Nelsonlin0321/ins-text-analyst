# -*- coding: utf-8 -*-

import json 
import re
import math
import pandas as pd
from pandas import ExcelWriter
from sklearn.feature_extraction.text import TfidfVectorizer

json_path = "assignment2.json"

def term_freq(word_list):
    word_dict = {}
    for w in word_list:
        if w in word_dict:
            word_dict[w] += 1
        else:
            word_dict[w] = 1
    word_num = float(sum(word_dict.values()))
    for w in word_dict.keys():
        word_dict[w] /= word_num
    return word_dict

def inv_doc_freq(term_set, doc_word_dict):
    doc_num = len(doc_word_dict)
    idf_dict = {}
    for w in term_set:
        doc_count = 0
        for word_list in doc_word_dict.values():
            if w in word_list:
                doc_count += 1
        idf_dict[w] = math.log(float(doc_num)/float(doc_count))
    return idf_dict


with open (json_path,'r',encoding = 'utf-8') as f:
    x = json.load(f)
    doc_word_dict = {}
    doc_tf_dict = {}
    sentence_list = []
    doc_name_list = []
    term_set = set()
    i = 0
    for item in x:
        if item ["edge_media_to_caption"] is not None:
            text = item["edge_media_to_caption"]["edges"][0]["node"]["text"]
            text = re.sub(r"http\S+","",text)
            text = re.sub(r"\([^)]*\)", "", text)
            text = re.sub("[+\.\!\/_,$%^*(+\"\'@#]\S+","",text)
            text = re.sub("[^A-Za-z\s]","",text)
            text = text.lower()
            stopwords = ("a", "an", "the", "he", "she", "it")
            if stopwords is not None:
                tokens = text.split()
                tokens = [w for w in tokens if w not in stopwords]
                text = " ".join(tokens)
                
            word_list = re.split('\ +',text)
            i += 1
            doc_name = "caption" + str(i)
            doc_name_list.append(doc_name)
            doc_word_dict[doc_name] = word_list
            sentence_list.append(text)
            doc_tf_dict[doc_name] = term_freq(word_list)
            term_set = term_set | set(word_list)
#idf_dict = inv_doc_freq(term_set, doc_word_dict)
#term_list = list(term_set)
#tf_idf = pd.DataFrame(columns = doc_name_list, index = term_list)
vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')
X = vectorizer.fit_transform(sentence_list)

'''
for (doc_name, word_list) in doc_word_dict.items():
    for w in term_set:
        if w in word_list:
            tf_idf.loc[w,doc_name] = doc_tf_dict[doc_name][w] * idf_dict[w]
        else:
            tf_idf.loc[w,doc_name] = 0.0
            
'''

'''
writer = ExcelWriter('Question1_PartA_1_d..xlsx')
tf_idf.to_excel(writer,'tfidf')
writer.save()
print("File Output Success")        
'''
# Computing the tf-idf
    
###############################################################################
'''
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from sklearn.cluster import KMeans
from wordcloud import WordCloud
import matplotlib.pyplot as plt

k = 20
vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')
X = vectorizer.fit_transform(sentence_list)
        
# perform clustering
km = KMeans(n_clusters=k, max_iter=100, n_init=1)
km.fit_transform(X)
        
print('Silhouette Coefficient: %0.5f\n' % metrics.silhouette_score(X, km.labels_, metric='euclidean'))    

###############################################################################

# generating the wordcloud for each cluster   
print('Top terms per cluster:')
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for a in range(k):
    content = ""
    print('Cluster %d:' % a, end='')
    for ind in order_centroids[a, :15]:
        content += "%s " % terms[ind]
        wordcloud = WordCloud().generate(content)
        print(' %s' % terms[ind], end='')
    print()
    wordcloud.to_file('wordcloud'+ str(a) +'.png')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
'''
