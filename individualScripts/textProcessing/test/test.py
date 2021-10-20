import csv
import sys
import os
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

texts=[[1,2,3],[3,2,1],[2,1,3],[3,1,2]]
# cv = CountVectorizer()
# cv_fit=cv.fit_transform(texts)

# print(cv.get_feature_names())
# print(cv_fit.toarray())

os.chdir(os.path.dirname(os.path.abspath(__file__)))

fileContent = ["get get get get",
"no no no get"
]

cv = CountVectorizer()
cv_fit=cv.fit_transform(fileContent)
# print(cv.get_feature_names())
# print(cv_fit.toarray())
doc_term_matrix = cv_fit.todense()
df = pd.DataFrame(doc_term_matrix, 
                  columns= cv.get_feature_names(), 
                  index=(list(range(0,2))))
df

cosineSimilarityScore = cosine_similarity(df, df)

print (cosineSimilarityScore)