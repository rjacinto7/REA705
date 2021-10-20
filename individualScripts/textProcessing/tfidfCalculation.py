import csv
import sys
import os
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('reCleanedEmails.txt') as f:
    fileContent = f.read().splitlines()

cv = CountVectorizer()
cv_fit=cv.fit_transform(fileContent)
# print(cv.get_feature_names())
# print(cv_fit.toarray())
doc_term_matrix = cv_fit.todense()
df = pd.DataFrame(doc_term_matrix, 
                  columns= cv.get_feature_names(), 
                  index=(list(range(0,8845))))
df

cosineSimilarityScore = cosine_similarity(df, df)

file = open('test.csv', 'w+', newline ='')
with file:
    write = csv.writer(file)
    write.writerows(cosineSimilarityScore)
