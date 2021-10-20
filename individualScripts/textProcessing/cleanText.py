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

targetFile = open("combinedSources.txt", "r")
fileContent = targetFile.readlines()
targetFile.close()

englishWords = set(nltk.corpus.words.words())
pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')

for line in range (0, len(fileContent)):
    #Remove special characters from phishing emails/text (Regex)
    fileContent[line] = re.sub(r"([^a-zA-Z\s]+?)", "", fileContent[line])

    #Not a task but noticed that some emails have spaced out words to evade spam filters
    #Join single space letters
    fileContent[line] = re.sub(r"\b(\w) (?=\w\b)", r"\1", fileContent[line])
    #Remove Multiple Spaces
    fileContent[line] = re.sub('\s+',' ',fileContent[line])
    #Join single spaces again
    fileContent[line] = re.sub(r"\b(\w) (?=\w\b)", r"\1", fileContent[line])
    fileContent[line] += "\n"

    #Remove all non-English words (Dictionary - Enchant/Other)
    fileContent[line] = " ".join(w for w in nltk.wordpunct_tokenize(fileContent[line]) if w.lower() in englishWords or not w.isalpha())
    fileContent[line] += "\n"

    #Remove stopwords + words smaller than 2
    fileContent[line] = pattern.sub('', fileContent[line])
    fileContent[line] = re.sub(r'\b\w{1,2}\b', '', fileContent[line])

#Remove everything that was less than 5 words, not enough content    
for email in fileContent:
    if len(email.split()) < 5:
        fileContent.remove(email)

with open("cleanedEmails.txt", 'w') as output:
    for row in fileContent:
        output.write(str(row))