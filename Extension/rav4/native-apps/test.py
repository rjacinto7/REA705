import struct
import json
import pickle
import numpy as np
# Original code from websiteDownloader
from urllib.parse import urlparse
from pathlib import Path
import urllib.request
import urllib.error
import urllib.parse
import argparse
import sys
import os
import re

# set current working directory to same directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# set the header for HTTP request
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}

with open('model_pickle', 'rb') as f:
    mp = pickle.load(f)


def urlFeatureCounter(site):
    '''Take a site URL and count its  URL Features'''
    hostname = urlparse(site).netloc
    site = str(site)
    urlCount = []
    urlCount.append(len(site))
    urlCount.append(site.count("@"))
    urlCount.append(site.count("/"))
    # Checks for presence of "www" in url | 1 = TRUE, 0 = FALSE
    if "www" in site:
        urlCount.append(site.count("1"))
    else:
        urlCount.append(site.count("0"))
    # Hostname Counts
    urlCount.append(hostname.count("."))
    urlCount.append(hostname.count("-"))
    urlCount.append(hostname.count("_"))
    # Counts the number of digits in hostname
    digits = 0
    for character in hostname:
        if character.isdigit():
            digits += 1
    urlCount.append(digits)
    # Checks if the URL is all ascii characters
    def onlyAscii(s): return re.match('^[\x00-\x7F]+$', s) != None
    if onlyAscii == True:
        urlCount.append(site.count("1"))
    else:
        urlCount.append(site.count("0"))

    totalCount = ' '.join(str(e) for e in urlCount)
    return totalCount


def pageFeatureCounter(site):
    '''Take a site URL and count its Page Features'''
    # try to open url to fetch webpage
    try:
        site = str(site)
        request = urllib.request.Request(url=site, headers=headers)
        # normalize html code to search specific keywords
        pageHTML = str(urllib.request.urlopen(request).read())
        featureCount = []

        # Page features based off of Table 1 in proposal
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

    # catches various exceptions and logs them in log file (HTTP errors, URL errors)
    except urllib.error.HTTPError:
        return "Error."
    except urllib.error.URLError:
        return "Error."


def Convert(string):
    '''convert string to list'''
    li = list(string.split(" "))
    return li


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
            # URL + Page Counter
            countedURLFeatures = urlFeatureCounter(receivedMessage)
            countedURLFeatures = Convert(countedURLFeatures)
            countedPageFeatures = pageFeatureCounter(receivedMessage)
            countedPageFeatures = Convert(countedPageFeatures)
            data = countedPageFeatures + countedURLFeatures
            data = np.reshape(data, (-1, 21))
            prediction = mp.predict(data)
            prediction = prediction[0]

            if prediction == 0:
                sendMessage(encodeMessage("Not Phishing"))
            elif prediction == 1:  # change this to equals 1
                sendMessage(encodeMessage("Phishing"))
            else:
                sendMessage(encodeMessage("Error"))
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
