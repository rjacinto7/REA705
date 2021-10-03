import requests
from bs4 import BeautifulSoup
import csv
import time
import os.path
from os import path
import argparse
import numpy as np


databaseResultsKnown = []
databaseResultsKnownFiltered = []
databaseResultsAll = []


currentPageBaseUrl = "https://phishtank.org/phish_detail.php?phish_id="
myParser = argparse.ArgumentParser(description='To scan webpages from PhishTank.')

#Arguments
myParser.add_argument('-pages', type=int,
    action='store',
    help = 'The number of pages to scan.',
    required=True)    
myParser.add_argument('-path',  type=str, 
    action="store",
    help = 'The path to the directory.',
    required=True)
myParser.add_argument('-name',  type=str,
    action="store",
    help = 'The name of the saved file.',
    required=True)
myParser.add_argument('-url',  type=str,
    action="store",
    help = 'The URL to be scanned.',
    required=True)
myParser.add_argument('-sleep',  type=int,
    action="store",
    help = 'The time to sleep between each request.',
    required=True)

args = myParser.parse_args()

baseUrl = args.url
print("The website ", baseUrl, "will be scanned.")

# Asks for number of pages to scan and checks if the input is an integer or not.
pagesToScan  = args.pages
try: 
    int(pagesToScan)
    print("You have opted scan ", pagesToScan, "pages. ")
except ValueError:
    print("The value you have entered is either not an integer or lower than zero. Please try again. \n")
    exit()

fileLocation = args.path
if not os.path.isdir(fileLocation):
    print("You have entered an invalid directory (Does not exist or path is invalid). Please try again.")
    exit()
    
else:
    print ("You have chosen to save at: ", fileLocation)


fileName = args.name
fileComplete = fileLocation + fileName + ".csv"


for x in range (0, int(pagesToScan)):
    currentPageScan = baseUrl + str(x)
    
    # Requested HTML PAGE
    currentPageScan = requests.get(currentPageScan)
    if currentPageScan.status_code == 200:
        print("Page ", x , "retrieved successfully. Proceeding... \n")
    else:
        print("WARNING!:  Page ", x , "did not respond or failed to be retreived. Results may vary.. \n")

    #Beautiful soup create object and select the table from Phistank
    currentPageParsed = BeautifulSoup(currentPageScan.content, "html.parser")
    currentPageParsed = currentPageParsed.find("table", attrs={'class':'data'})

    currentPageResults = currentPageParsed.find_all('tr', style="background: #ffffcc;")

    for currentRow in currentPageResults:
        column = currentRow.find_all('td')
        column = [ele.text.strip(" ") for ele in column]
        del column[2]
 #      del column[0]
        column[1] = column[1].split("added",1)[0]
        databaseResultsKnown.append(column)
    time.sleep(args.sleep)



for i in range(0, len(databaseResultsKnown)):
    # Sets the variable j to the URL.
    j = databaseResultsKnown[i][1]
    #Open the phishtank detailed url analysis page if the last 3 characters are "..."
    if j[-3:] == "...":
        #Requested Html Page
        filteredPageFullUrl = currentPageBaseUrl + databaseResultsKnown[i][0]
        currentPageFullUrlScan = requests.get(filteredPageFullUrl)
        
        # Check if the detailed web page is retrievable. 
        if currentPageFullUrlScan.status_code == 200:
            print("-------------------------------------------------------------------------")
            print("WARNING: Incomplete URL found... (",j ,")" "\nDetailed Phishing URL:", filteredPageFullUrl, "Retreived successfully.")
            print("-------------------------------------------------------------------------")
        else:
            print("WARNING!:  Page ", i , "did not respond or failed to be retreived. Results may vary.. \n")
        #Creates a beautiful soup object for HTML parsing.
        detailedPageParsed = BeautifulSoup(currentPageFullUrlScan.content, "html.parser")
        detailedPageParsed = detailedPageParsed.find("div", {"id":"main"})

        detailedPageResults = detailedPageParsed.find_all('span', style="word-wrap:break-word;")
        
        # Find the Full URL and change the value of the array to it.
        for currentRow in detailedPageResults:
            detailedColumn = currentRow.find_all('b')
            detailedColumn = [ele.text.strip(" ") for ele in detailedColumn]
            databaseResultsKnown[i][1] = detailedColumn[0]
        
    else:
        print(j, "is a complete URL.")
       
print(databaseResultsKnown)
rowDetails = ["SITE", "VALID?", "STATUS"]
with open (fileComplete, "w") as currentFile:
    write = csv.writer(currentFile)
    write.writerows(databaseResultsKnown)
    currentFile.close()


