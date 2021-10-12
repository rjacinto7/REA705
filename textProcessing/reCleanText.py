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

targetFile = open("cleanedEmails.txt", "r")
fileContent = targetFile.readlines()
targetFile.close()

for line in range (0, len(fileContent)):
    #Remove Multiple Spaces
    fileContent[line] = re.sub('\s+',' ',fileContent[line])
    fileContent[line] = fileContent[line].lower().strip()
    fileContent[line] += "\n"

with open("reCleanedEmails.txt", 'w') as output:
    for row in fileContent:
        output.write(str(row))