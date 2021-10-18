import struct
import json

#Original code from websiteDownloader
from urllib.parse import urlparse
from pathlib import Path
import urllib.request
import urllib.error
import urllib.parse
import argparse
import sys
import os
import re

#Imports for tf-idf cosine similarity
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
stopPattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
englishWords = set(nltk.corpus.words.words())
comparitor = []

with open("reCleanedEmails.txt") as file:
    emailTexts = file.readlines()
    emailTexts = [line.rstrip() for line in emailTexts]
    file.close()
totalEmails = len(emailTexts)

#set current working directory to same directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#set the header for HTTP request
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}

#Take a site URL and count its  URL Features
def urlFeatureCounter(site):
    hostname = urlparse(site).netloc
    site = str(site)
    urlCount = []
    urlCount.append(len(site))
    urlCount.append(site.count("@"))
    urlCount.append(site.count("/"))
    #Checks for presence of "www" in url | 1 = TRUE, 0 = FALSE
    if "www" in site:
        urlCount.append(site.count("1"))
    else:
        urlCount.append(site.count("0"))
    #Hostname Counts
    urlCount.append(hostname.count("."))
    urlCount.append(hostname.count("-"))
    urlCount.append(hostname.count("_"))
    #Counts the number of digits in hostname
    digits = 0
    for character in hostname:
        if character.isdigit():
            digits += 1
    urlCount.append(digits)
    #Checks if the URL is all ascii characters 
    onlyAscii = lambda s: re.match('^[\x00-\x7F]+$', s) != None
    if onlyAscii == True:
        urlCount.append(site.count("1"))
    else:
        urlCount.append(site.count("0"))

    totalCount = ' '.join(str(e) for e in urlCount)
    return totalCount

#Take a site URL and count its Page Features
def pageFeatureCounter(site):
    #try to open url to fetch webpage 
    try:
        site = str(site)
        request = urllib.request.Request(url=site, headers=headers)
        #normalize html code to search specific keywords
        pageHTML = str(urllib.request.urlopen(request).read())
        featureCount = []

        #Page features based off of Table 1 in proposal 
        featureCount.append(pageHTML.count('</form>'))
        featureCount.append(pageHTML.count('formmethod="post"'))
        featureCount.append(pageHTML.count('formmethod="get"'))
        featureCount.append(pageHTML.count('</script>'))
        featureCount.append(pageHTML.count('.js'))
        featureCount.append(pageHTML.count('</iframe>'))
        featureCount.append(pageHTML.count('</applet>'))
        featureCount.append(pageHTML.count('</frame>'))
        featureCount.append(pageHTML.count('type="submit'))
        featureCount.append(pageHTML.count('input email'))
        featureCount.append(pageHTML.count('password'))
        featureCount.append(pageHTML.count('</button>'))
        totalCount = ' '.join(str(e) for e in featureCount)
        return totalCount

    #catches various exceptions and logs them in log file (HTTP errors, URL errors)
    except urllib.error.HTTPError  as e:
        return "Error."
    except urllib.error.URLError as e:
        return "Error."

#clean submitted texts
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

#calculate TF-IDF cosine similarity score 
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

#!/usr/bin/env python
try:
    # Python 3.x version
    # Read a message from stdin and decode it.
    def getMessage():
        rawLength = sys.stdin.buffer.read(4)
        if len(rawLength) == 0:
            sys.exit(0)
        messageLength = struct.unpack('@I', rawLength)[0]
        message = sys.stdin.buffer.read(messageLength).decode('utf-8')
        return json.loads(message)

    # Encode a message for transmission,
    # given its content.
    def encodeMessage(messageContent):
        encodedContent = json.dumps(messageContent).encode('utf-8')
        encodedLength = struct.pack('@I', len(encodedContent))
        return {'length': encodedLength, 'content': encodedContent}

    # Send an encoded message to stdout
    def sendMessage(encodedMessage):
        sys.stdout.buffer.write(encodedMessage['length'])
        sys.stdout.buffer.write(encodedMessage['content'])
        sys.stdout.buffer.flush()

    while True:
        receivedMessage = getMessage()
        try:
            receivedMessage = str(receivedMessage)

            #URL + Page Counter
            # toBeSent = urlFeatureCounter(receivedMessage)
            # toBeSent += " " + pageFeatureCounter(receivedMessage)

            ##TF-IDF Cosine Similarity Average 
            cleanedUserInput = cleanText(receivedMessage)
            comparitor.append(cleanedUserInput)
            score = 0
            for currentEmail in emailTexts:
                comparitor.append(currentEmail)
                score += cosineSimilarity(comparitor)
                comparitor.pop()
            toBeSent = str(score/totalEmails)

            sendMessage(encodeMessage(toBeSent))
        except:
            sendMessage(encodeMessage("Invalid Input"))

except AttributeError:
    # Python 2.x version (if sys.stdin.buffer is not defined)
    # Read a message from stdin and decode it.
    def getMessage():
        rawLength = sys.stdin.read(4)
        if len(rawLength) == 0:
            sys.exit(0)
        messageLength = struct.unpack('@I', rawLength)[0]
        message = sys.stdin.read(messageLength)
        return json.loads(message)

    # Encode a message for transmission,
    # given its content.
    def encodeMessage(messageContent):
        encodedContent = json.dumps(messageContent)
        encodedLength = struct.pack('@I', len(encodedContent))
        return {'length': encodedLength, 'content': encodedContent}

    # Send an encoded message to stdout
    def sendMessage(encodedMessage):
        sys.stdout.write(encodedMessage['length'])
        sys.stdout.write(encodedMessage['content'])
        sys.stdout.flush()

    while True:
        receivedMessage = getMessage()
        if receivedMessage == "ping":
            sendMessage(encodeMessage("pong2"))
