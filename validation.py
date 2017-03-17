# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 07:22:32 2017

@author: anbarasan.selvarasu
"""
"""
This class is used to validate and understand the results of the LDA Model built
It prints the list of all topics and the most probable words belonging to that topic.

"""



from configurations import Configurations

import logging
import numpy as np
from gensim.models import LdaModel
from gensim import corpora, similarities, matutils




class ValidateLDA(object):
    
    def __init__(self,lda_path):
        self.lda = LdaModel.load(lda_path)
        
    
    def model_analysis(self):
         print()
         print()
         print("LDA Topics and the weights of words associated with that topic")
         print(self.lda.show_topics())
         print()
         
    def print_topics_gensim(self, total_topics=5,
                            weight_threshold=0.0001,
                            display_weights=False,
                            num_terms=None):
        
        for index in range(total_topics):
            topic = self.lda.show_topic(index,num_terms)
            topic = [(word, round(wt,2)) 
                     for word, wt in topic 
                     if abs(wt) >= weight_threshold]
            if display_weights:
                print('Topic #'+str(index+1)+' with weights')
                print(topic[:num_terms] if num_terms else topic)
            else:
                print('Topic #'+str(index+1)+' without weights')
                tw = [term for term, wt in topic]
                print( tw[:num_terms] if num_terms else tw)
                
            print()
            
def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    print("LDA Validation")
    lda_path = Configurations.LOAD_LDA
    validate = ValidateLDA(lda_path)
    ## Miscellaneous Analysis
    validate.model_analysis()
     
    print()
    print("Analysing the top words in each topic ..........")
    validate.print_topics_gensim(15,0.0001,False,50)
    
    
if __name__ == "__main__":
    main()