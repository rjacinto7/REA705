import csv
import sys
import os
import re
import nltk
from nltk.corpus import stopwords
#dictionary downloading
#nltk.download('stopwords')
#nltk.download('words')

os.chdir(os.path.dirname(os.path.abspath(__file__)))

targetFile = open("file.txt", "r")
fileContent = targetFile.readlines()
targetFile.close()

wordCounts = {}

for email in fileContent:
    currentEmail = email.split()
    for word in currentEmail:
        if word.lower() not in wordCounts:
            wordCounts[word.lower()] = 1
        else:
            currentCount =  wordCounts[word.lower()]
            wordCounts[word.lower()] = currentCount + 1


sortedWordCount = {k: v for k, v in sorted(wordCounts.items(), key=lambda x: x[1])}

with open('wordCounts.csv', 'w',  newline='') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in sortedWordCount.items():
       writer.writerow([key, value])
    csv_file.close()

