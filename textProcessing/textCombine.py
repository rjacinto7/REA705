#emailTestingData.txt
#   Text is all Spam / SE text
#   Clear '    "Text": "Subject:' on every text

#spamHamTrain.txt
#   "classes":["ham"], "text":
#   Count how many have spam 

#emailTrainingData20k.csv
#   Classified as Ham / Spam in the 2nd column
#   Clear "Subject: "

import json
import csv
import os
import sys
import re
from typing import final

os.chdir(os.path.dirname(os.path.abspath(__file__)))

totalMessages = 0
finalTexts = []

with open ("emailTestingData.txt", "r") as targetFile:
    for x in targetFile:
        if 'Text' in x:
            x = x.removeprefix('   "Text": "Subject: ')
            x = x.removesuffix('",\n')
            finalTexts.append(x)
            totalMessages += 1
    targetFile.close()

print ("Total spam messages gathered from emailTestingData.txt: ", totalMessages)

totalMessages = 0
with open ("spamHamTrain.txt", "r") as targetFile:
    for x in targetFile:
        if '{"classes":["spam"], "text":"' in x:
            x = x.removeprefix('{"classes":["spam"], "text":"')
            x = x.removesuffix('"},\n')
            finalTexts.append(x)
            totalMessages += 1
    targetFile.close()
print ("Total spam messages gathered from emailTestingData.txt: ", totalMessages)

totalMessages = 0
with open ("emailTrainingData20k.csv") as targetFile:
    csvReader = csv.reader(targetFile)
    csvRows = list(csvReader)
    for x in range (1, len(csvRows)):
        if csvRows[x][1] == "spam":
            spamMessage = csvRows[x][0].removeprefix("Subject: ")
            finalTexts.append(spamMessage)
            totalMessages += 1
    targetFile.close()

print ("Total spam messages gathered from emailTrainingData20k.csv: ", totalMessages)

with open ("finalTexts.txt", "w") as targetFile:
    for item in finalTexts:
        targetFile.write("%s\n" % item)