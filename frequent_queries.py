#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 15:03:25 2018

@author: anbarasan
"""

import imageio
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud

from configurations import Configurations
from nmf import *
from preprocessing import *

enquiries_df = pd.read_csv(Configurations.INPUT_FILE)
# Columns expected from file "enquiries", "type"
# print(enquiries_df.head())
# Ignore this Line : enquiries_df.rename(columns = {'text':'enquiries'}, inplace = 1)

enquiries_df_1 = enquiries_df[['text','type']] # Pick only the enquiries and type columns
    
## Step 1: Preprocessing - Tokenization and stop word removal
##         Only tokens with pos tags as NN and NNS is retained 
## Reference: P   
preprocess = Preprocessing()
    
processed_df =  preprocess.normalize_corpus(enquiries_df_1) 
    
corpus = processed_df['text'].values.tolist()
corpus_2 = [' '.join(char) for char in corpus]
    #corpus = [' '.join(char) for char in corpus]    
    #corpus = [i.split(",") for i in corpus]
print(type(corpus[0][1]))
     
   ## Approach 1: GENSIM LDA ###    word2vec.py
#featuregen = FeatureGeneration()
#dictionary = featuregen.build_dictionary(corpus,num_below,num_above)
#    print("Features :",len(dictionary.keys()))
#    mapped_corpus = featuregen.build_mapped_corpus(corpus, dictionary)
#    
#    model_lda = featuregen.model_lda(mapped_corpus, dictionary,num_topics)
#    
#    ## Check for unicode decod eerrors
#    for t in range(num_topics):
#        print('Topic #'+str(t+1)+' with weights')
#        print(model_lda.show_topic(t, 30))
#        print()
    
        
    ##Approach 2: NMF ### nmf.py
factorizer = MatrixFactorization()
    
vectorizer,feature_matrix = factorizer.calculate_tfidf(corpus,Configurations.NUM_BELOW, Configurations.NUM_ABOVE, Configurations.NUM_FEATURES)
nmf = factorizer.fit_nmf(Configurations.NUM_TOPICS,Configurations.NUM_WORDS,feature_matrix)
tfidf_feature_names = vectorizer.get_feature_names()
factorizer.print_top_words(nmf, tfidf_feature_names, Configurations.NUM_WORDS)
    
### Validation ## validation.py
topic_df = factorizer.topic_table(nmf, tfidf_feature_names, Configurations.NUM_WORDS)
print(topic_df.head())
# print(topic_df.columns)

#encoded pic
# file = open(Configurations.ENCODED_IMAGE_FILE, "rb")
# picture_64 = file.read()
# # Generate the Mask for EAP
# f1 = open(Configurations.WORDCLOUD_IMAGE_FILE, "wb")
# f1.write(codecs.decode(picture_64,'base64'))
# f1.close()
img1 = imageio.imread(Configurations.WORDCLOUD_IMAGE_FILE)
# img = img.resize((980,1080))
hcmask = img1

### Show wordcloud ###
plt.figure(figsize=(16,13))
wc = WordCloud(background_color="black", max_words=10000,
               mask=hcmask, max_font_size= 40)
for i in range(Configurations.NUM_TOPICS):
    wc.generate(" ".join(topic_df["topic_"+str(i)+":"]))
    plt.title("Topic"+str(i), fontsize=20)

    plt.imshow(wc.recolor(colormap= 'Pastel2', random_state=17), alpha=0.98)
    plt.axis('off')
    plt.show()

### Count document distribution by Topics ###    
docweights = nmf.transform(vectorizer.transform(corpus_2))
    
queries_with_topics = pd.DataFrame({'actual sentence': np.array(enquiries_df['text'].values),
                                   'enquiries': np.array(corpus_2),
                       'topic':docweights.argmax(axis=1)},
                      )
print("Most Frequent Topics and the document counts......")
print(queries_with_topics['topic'].value_counts())    

print("Sample Questions and Topics")
df_topics = factorizer.showdocs(queries_with_topics, range(Configurations.NUM_TOPICS))
print(df_topics)


queries_with_topics.to_csv(Configurations.OUTPUT_FILE, index = False)
