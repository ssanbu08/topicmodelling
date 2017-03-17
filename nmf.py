# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 13:28:48 2017

@author: anbarasan.selvarasu
"""
from configurations import Configurations
from time import time

import logging
import pandas as pd
import re

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

class MatrixFactorization(object):
    
    def __init__(self):
        print("Matrix Factorization instantiated succesfully.....")

    def print_top_words(self,model, feature_names, n_top_words):
        for topic_idx, topic in enumerate(model.components_):
            print("Topic #%d:" % topic_idx)
            print(" ".join([feature_names[i]
                            for i in topic.argsort()[:-n_top_words - 1:-1]]))
        print()

    ### First Cut model
    ### Using the text as such and allowing tf_idf vectorizer to construct features
    ### setting min_df and max_df plays a crucial role here
    def calculate_tfidf(self,corpus,mindf,maxdf,nfeatures):
    # Use tf-idf features for NMF.
        corpus_tf_input = []
        for corp in corpus:
            rev = ' '.join(corp)
            corpus_tf_input.append(rev)
            
        print("Extracting tf-idf features for NMF...")
        tfidf_vectorizer = TfidfVectorizer(max_df=maxdf, min_df=mindf,
                                           #max_features=nfeatures,
                                           ngram_range = (1,1))
        t0 = time()
        feature_matrix = tfidf_vectorizer.fit_transform(corpus_tf_input)
        print("done in %0.3fs." % (time() - t0))
        print("Shape of feature matrix",feature_matrix.shape)
        return tfidf_vectorizer,feature_matrix

    # Fit the NMF model
    def fit_nmf(self,num_topics,num_words,tfidf_matrix):
            
        print("Fitting the NMF model with tf-idf features, "
              "n_samples=%d and n_features=%d..."
              % (tfidf_matrix.shape[0], tfidf_matrix.shape[1]))
        t0 = time()
        nmf = NMF(n_components=num_topics, random_state=1,
                  alpha=.1, l1_ratio=.5).fit(tfidf_matrix)
        print("done in %0.3fs." % (time() - t0))
        
        print("\nTopics in NMF model:")
        return nmf
        

def main():
    print("Matrix Factorization.......")
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
    processed_file = Configurations.PROCESSED_FILE
    print(processed_file)
    data = pd.read_table(processed_file,encoding = "ISO-8859-1",sep = ",")
    print(type(data['text']))
    corpus = data['text'].values.tolist()
    
    corpus = [re.sub(r'[\[\]\']','',char) for char in corpus]    
    corpus = [i.split(",") for i in corpus]
    print(type(corpus[0][1]))
    sentences = [] 
    for sent in corpus:
        words=[]
        for word in sent:
            words.append(word.strip())
        
        sentences.append(words)
    

    ##params
    num_topics = 15
    min_df = 40
    max_df = 0.05 
    num_features = 10000
    num_words = 30
    
    factorizer = MatrixFactorization()
    
    vectorizer,feature_matrix = factorizer.calculate_tfidf(sentences,min_df,max_df,num_features)
    nmf = factorizer.fit_nmf(num_topics,num_words,feature_matrix)
    tfidf_feature_names = vectorizer.get_feature_names()
    factorizer.print_top_words(nmf, tfidf_feature_names, num_words)
    
    
    
    

if __name__ == "__main__":
    main()