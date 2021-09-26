import requests
from bs4 import BeautifulSoup
import csv
import time
import os.path
from os import path
import argparse


databaseResultsKnown = []
databaseResultsAll = []

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
        del column[0]
        column[0] = column[0].split("added",1)[0]
        databaseResultsKnown.append(column)

    rowDetails = ["SITE", "VALID?", "STATUS"]
    with open (fileComplete, "w+") as currentFile:
        write = csv.writer(currentFile)
        write.writerows(databaseResultsKnown)
        currentFile.close()
    
    time.sleep(args.sleep)