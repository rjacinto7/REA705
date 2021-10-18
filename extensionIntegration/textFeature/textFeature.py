import sys
import os
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

#Set current working directory to path of this file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

submittedText="Hello how are you today are you well?"
comparitor = []
# comparitor.append("test ay lmao")

stopPattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
englishWords = set(nltk.corpus.words.words())

def cleanText(submittedText):
    #Remove special characters from phishing emails/text (Regex)
    submittedText = re.sub(r"([^a-zA-Z\s]+?)", "", submittedText)
    #Not a task but noticed that some emails have spaced out words to evade spam filters
    #Join single space letters
    submittedText = re.sub(r"\b(\w) (?=\w\b)", r"\1", submittedText)
    #Remove Multiple Spaces
    submittedText = re.sub('\s+',' ',submittedText)
    #Join single spaces again
    submittedText = re.sub(r"\b(\w) (?=\w\b)", r"\1", submittedText)
    #Remove all non-English words (Dictionary - Enchant/Other)
    submittedText = " ".join(w for w in nltk.wordpunct_tokenize(submittedText) if w.lower() in englishWords or not w.isalpha())
    #Remove stopwords + words smaller than 2
    submittedText = stopPattern.sub('', submittedText)
    submittedText = re.sub(r'\b\w{1,2}\b', '', submittedText)
    return submittedText

def cosineSimilarity(currentScore):
    cv = CountVectorizer()
    cv_fit=cv.fit_transform(currentScore)
    doc_term_matrix = cv_fit.todense()
    df = pd.DataFrame(doc_term_matrix, 
                      columns= cv.get_feature_names(), 
                      index=(list(range(0,2))))
    df

    cosineSimilarityScore = cosine_similarity(df, df)
    return cosineSimilarityScore[0][1]

submittedText = cleanText(submittedText)
comparitor.append(submittedText)
score = 0

with open("reCleanedEmails.txt") as file:
    emailTexts = file.readlines()
    emailTexts = [line.rstrip() for line in emailTexts]
    file.close()

totalEmails = len(emailTexts)

for currentEmail in emailTexts:
    comparitor.append(currentEmail)
    x = cosineSimilarity(comparitor)
    score += x
    comparitor.pop()

print (score/totalEmails)
    