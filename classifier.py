3# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 14:41:51 2017

@author: anbarasan.selvarasu
"""
import sys
import logging

import numpy as np
from gensim.models import LdaModel
from gensim import corpora, similarities, matutils
import nltk
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from nltk.stem.wordnet import WordNetLemmatizer
#import matplotlib.pyplot as plt

from configurations import Configurations
#from preprocessing import Preprocessing
from stopwords import stopwords_list as stop
#from feature_selection import FeatureSelection


class ClassifyTopics():
    
     topic_themes = {0:"people & service",1:"Burgers,Fried items,Sauce",2:"Mexican and Bread",3:"BEEF,Meat,Seafood"
                     ,4:"Snacks and salads",5:"Sea-food & mEAT",6:"diffused topic",7:"Ambience",8:"diffused topic"
                     ,9:"service",10:"Morning",11:"Restaurant Type",12:"Sandwich and Burgers"
                     ,13:"Facilities",14:"Veggies"}     
     
     
     def __init__(self, id2word_path, lda_path):
         self.dictionary = corpora.Dictionary.load(id2word_path)
         self.lda = LdaModel.load(lda_path)
         

#==============================================================================
#      def load_stopwords(self):
#          stopwords = {}
#          with open('stopwords.txt', 'rU') as f:
#              for line in f:
#                  stopwords[line.strip()] = 1
#  
#          return stopwords
#  
#==============================================================================
     def extract_lemmatized_nouns(self, new_review):
         stopwords = stop
         words = []
 
         sentences = (new_review.lower().split('.'))
         for sentence in sentences:
             tokens = sentence.split()
             text = [word for word in tokens if word not in stopwords]
             tagged_text = nltk.pos_tag(text)
 
             for word, tag in tagged_text:
                 words.append({"word": word, "pos": tag})
 
         lem = WordNetLemmatizer()
         nouns = []
         for word in words:
             if word["pos"] in ['NN', 'NNS']:
                 nouns.append(lem.lemmatize(word["word"]))
 
         return nouns


     def run(self, new_review):
         nouns = self.extract_lemmatized_nouns(new_review)
         new_review_bow = self.dictionary.doc2bow(nouns)
         new_review_lda = self.lda[new_review_bow]
         
         new_review_lda_sorted= sorted(new_review_lda, key=lambda x: x[1],reverse=True)
         top3_topics = new_review_lda_sorted[:3]
         print("############Topic Distribution for the review#########")
         for topic in top3_topics:
             key = topic[0]
             named_topic = self.topic_themes[key]
             
             print("Topic: %s  Probability: %0.3f" % (named_topic,topic[1]))
             print()
         return new_review_lda
         
#==============================================================================
#      def visualize_lda(self,topic_distribution):
#          # sort in-place from highest to lowest
#         topic_distribution.sort(key=lambda x: x[1], reverse=True) 
#         
#         # save the names and their respective scores separately
#         # reverse the tuples to go from most frequent to least frequent 
#         topic = [x[0] for x in topic_distribution]
#         score = [x[1] for x in topic_distribution]
#         x_pos = np.arange(len(topic)) 
#                 
#         plt.bar(x_pos, score,align='center')
#         plt.xticks(x_pos, topic) 
#         plt.ylabel('Topic Score')
#         plt.show()
#          
#==============================================================================
         
     
         


def main():
     logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
    
#==============================================================================
#     new_review = "It's like eating with a big Italian family. " \
#                  "Great, authentic Italian food, good advice when asked, and terrific service. " \
#                  "With a party of 9, last minute on a Saturday night, we were sat within 15 minutes. " \
#                  "The owner chatted with our kids, and made us feel at home. " \
#                  "They have meat-filled raviolis, which I can never find. " \
#                  "The Fettuccine Alfredo was delicious. We had just about every dessert on the menu. " \
#                  "The tiramisu had only a hint of coffee, the cannoli was not overly sweet, " \
#                  "and they had this custard with wine that was so strangely good. " \
#                  "It was an overall great experience!"
#                  "
#==============================================================================
                 
     review_list=["1.Love the deal for ice cream cones and that is what I have tried so far. I will come back to try food items.",
                 "2.Courteous service but the food is terrible. I ordered the burrito which was cold and came with no noticeable cheese. Beef stuffing was dry and the only flavour I tasted was salt. Will not go again.",
                 "3.It's Quiznos.  Yes, sticker shock, but it's the airport.  My 8 Italian on Rosemary filled me up.  The crew working this location is not super fast, but the end product was consistent with my Quiznos expectations.",
                 "4.A great place for dinner with friends. Nice ambiance, really friendly and efficient service and delicious food.",
                 "5.I loved the fact that the food came out quickly, and when it did, it was piping hot! Everything was wonderfully flavourful, crispy when it was supposed to be, and fresh fresh fresh.",
                 "6.I will definitely be returning (on another toonie tuesday.. or loonie monday!) to try everything on the menu!",
                 "7.This Chuck E Cheese is like the majority of the Chuck E Cheese's we've been to. However with one clear exception," \
                 "it has been cards instead of the tokens that you have to lug around. The staff is friendly and moderately helpful as is the case at most of these locations. All in all, and average experience.",
                 "8. Was excited to find BBQ near one of my clients. I was spoiled down in Columbus by Ray Ray's Hog Pit where I ate nearly every single day they were open (Fri-Sun)."\
                 "This place is cleaner than Hot Sauce, but the same low grade Cleveland 'hood slop. "\
                 "Shoulder sandwich was a uniform and uninspiring grey with no smoke ring or ANY visual evidence of being smoked. I requested sauce on the side, but had my sandwich covered in cold BBQ sauce and as is customary in Cleveland, served on flimsy sliced bread. "\
                 "I don't understand how people think places like this and Hot Sauce Williams are any good....",
                 "9.From San Francisco cioppino to roasted short ribs, Ed's always delivers with explosive, rich flavors and inventive pairing of ingredients and influences. Hailing originally from the San Francisco Bay area, Ed cooks American, Asian and Latin dishes with French technique in a comfortable, casual setting. Never stingy with the foie gras and truffles, Ed consistently delivers an exciting meal."\
                 "If you can manage to snag a seat at the table, you're going home satisfied.",
                 "10.Two words - moulds frites! Best mussels in Edinburgh for lunch and only £6 for a bucketful! Worth mentioning that if this place sounds good but is too far out, got to outsider - same same but different, just sister restaurant"]
                 
     for reviews in review_list:
         print(reviews)
         print()
        
     review_no = input("#####Select a review to analyse the topics..Or press 11 to enter your own review#####")
     review_no = int(review_no)
     if review_no != 11:
         new_review = review_list[review_no-1]
     else:
         new_review = input("Enter your review...")
         
         
    
      #preprocess = Preprocessing()
      #reviews_normalized = preprocess.normalize_corpus(new_review)
     
     dictionary_path = Configurations.ID2WORD_FILE
     lda_path = Configurations.LOAD_LDA
    
     classify = ClassifyTopics(dictionary_path,lda_path)
     topic_distribution = classify.run(new_review)
     #classify.visualize_lda(topic_distribution)
     
     
    

if __name__ == '__main__':
    main()


