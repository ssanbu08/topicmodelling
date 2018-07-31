# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 08:58:47 2017

@author: anbarasan.selvarasu
"""
from stopwords import stopwords_list as stop

import pandas as pd
import nltk

nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
import re
import string
from time import time
import logging

from configurations import Configurations

class Preprocessing(object):
    
    def __init__(self):
        pass
        
    def remove_stopwords(self,text):
            stopword_list = stop
            tokens = self.tokenize_text(text)
            filtered_tokens = [token for token in tokens if token not in stopword_list]
            filtered_text = ' '.join(filtered_tokens)    
            return filtered_text
        
    def tokenize_text(self,text):
    
         #tokens = nltk.word_tokenize(text) 
         tokens = text.split()
         tokens = [token.strip() for token in tokens if len(token.strip())>3]
         return tokens
    
    def remove_special_characters(self,text):
    
         tokens = self.tokenize_text(text)
         pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
         filtered_tokens = filter(None, [pattern.sub(' ', token) for token in tokens])
         filtered_text = ' '.join(filtered_tokens)
         return filtered_text
    
    def keep_text_characters(self,text):
    
         filtered_tokens = []
         tokens = self.tokenize_text(text)
         for token in tokens:
             if re.search('[a-zA-Z]', token):
                 filtered_tokens.append(token)
         filtered_text = ' '.join(filtered_tokens)
         return filtered_text
    
    def normalize_corpus(self,master_df):
        corpus = master_df['text'].values.tolist()
        sentences = []  
        try:
            for text in corpus:
                words = []  
                text = text.lower()
                text = self.remove_special_characters(text)
                text = self.remove_stopwords(text)
                text = self.keep_text_characters(text)
                text = self.tokenize_text(text)
                tagged_text = nltk.pos_tag(text)
                for word, tag in tagged_text:
                    if tag in Configurations.POS_TAGS:
                        words.append(word)
                sentences.append(words)
            master_df['text'] = sentences 
        except :
           raise ValueError('Error in Normalize Corpus')
    
        return master_df
        
def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
    preprocess = Preprocessing()   
    
    print("Loading reviews....")
    master = pd.read_csv(Configurations.MASTER_FILE,chunksize = 1000,encoding='latin-1')
    master_df = []
    chunk_no=1
    rows_counter = 0
    for df in master:
       # process each data frame
           t0 = time()
       #if chunk_no<3:
           return_df =  preprocess.normalize_corpus(df)
           master_df.append(return_df)
           n_rows = (return_df.shape[0])
           rows_counter +=n_rows
           print ("Records Processed..", rows_counter)
           print("processed chunk %d  in %0.3fs." % (chunk_no, (time() - t0))) 
           chunk_no+=1
       #else:
       #    break
   
    master_df_2 = pd.concat(master_df,ignore_index = True)
    print ("No of rows processed Reviews %d" % (master_df_2.shape[0]))
    master_df_2.to_csv(Configurations.PROCESSED_FILE)
    
    
        


if __name__ == '__main__':
    main()