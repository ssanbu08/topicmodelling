# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 22:47:51 2017

@author: anbarasan.selvarasu
"""
from configurations import Configurations
import logging
import pandas as pd
import re
from gensim import corpora, models, similarities, matutils

class FeatureGeneration(object):
    
    def __init__(self):
        print("FeatureGeneration Object instantiated succesfully..")
    

    def build_dictionary(self,corpus,num_below=20,num_above=0.1):
        dictionary = corpora.Dictionary(corpus)
        print(len(dictionary.keys()))
        dictionary.filter_extremes(no_below =num_below,no_above = num_above)
        print(len(dictionary.keys()))
        dictionary.compactify()
        return dictionary
        
    def build_mapped_corpus(self,corpus,dictionary):
        mapped_corpus = [dictionary.doc2bow(text) 
                         for text in corpus]
        return mapped_corpus
    
     
     
    def model_lda(self,corpus, dictionary, total_topics):
         lda = models.LdaModel(corpus, 
                               id2word=dictionary,
                               num_topics=total_topics)
         return lda                     

    
    # Method Definition to build LDA topic modeling
#==============================================================================
#     def model_lda_multicore(self,corpus, dictionary,total_topics):        
#         lda_multicore = models.LdaMulticore(corpus,
#                                             id2word= dictionary, 
#                                             num_topics= total_topics, 
#                                             workers = 3, batch = 1000 )
#         return lda_multicore
#==============================================================================
    

def main():
    print("hello")
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
    num_below = 40
    num_above = 0.05 
    
    # Best model num_topics = 15,num_below = 40,num_above = 0.05 => All yopics are meaningful
    # # num_above = 0.05,num_below = 40, num_topics = 30 ,num_features = 5152 equal to previous iterations,Topics not narrows and looks diverse
    # num_above = 0.05,num_below = 40, num_topics = 20 ,num_features = 5152 equal to previous iterations,consider increaing numbe of topics as the topisc are diverse
    # previous run num_above=0.05 ,num_below = 30,num_topics = 20-better than previous iterations = 6181 feature
    # previous run num_above= 0.075 performing comparatively better than 0.1,Features =6222
    # previous run num_above=0.1,num_topics = 20,num_below =  30,features = 6244
    print('num_topics ',num_topics)       
    print('num_below ',num_below)       
    print('num_above ',num_above)       
         
    featuregen = FeatureGeneration()
    dictionary = featuregen.build_dictionary(sentences,num_below,num_above)
    print("Features :",len(dictionary.keys()))
    mapped_corpus = featuregen.build_mapped_corpus(sentences, dictionary)
    
    model_lda = featuregen.model_lda(mapped_corpus, dictionary,num_topics)
    
    ## Check for unicode decod eerrors
    for t in range(num_topics):
        print('Topic #'+str(t+1)+' with weights')
        print(model_lda.show_topic(t, 30))
        print()
    
        
    # Save the model for fast usage
    model_name = "model_lda_" + str(num_topics) +".lda"
    model_file_path = Configurations.LDA_MODEL_FILE + model_name
    model_lda.save(model_file_path)
    

if __name__ == '__main__':
    main()