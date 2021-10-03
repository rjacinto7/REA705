import csv
import os
import time
import re
import socket
from urllib.parse import urlparse


databaseFile = input("Please enter the name of the file: ")
urlArray = []
with open (databaseFile) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        urlArray.append(row)

urlArrayFiltered = [i for i in urlArray if i != []]


#Appends the length of each URL to the array.
for i in urlArrayFiltered:
    lastColumn =  len(i[1])
    i.append(lastColumn)
    
#Appends the number of @ in the URL.
for i in urlArrayFiltered:
    atCount = i[1].count('@')
    i.append(atCount)
#Appends the number of slashes in the URL.   
for i in urlArrayFiltered:
    slashCount = i[1].count('/')
    i.append(slashCount)
#Finds whether or not WWW is present in the URL.
for i in urlArrayFiltered:
    wwwCount = i[1].count("www")
    if wwwCount >=1:
        i.append("True")
    else:
        i.append("False")
#IP address of DOMAIN        
for i in urlArrayFiltered:
    ipDomain = urlparse(i[1]).netloc
    try:
        domainIpAddr = socket.gethostbyname(ipDomain)
        i.append(domainIpAddr)
    except socket.gaierror:
        i.append("Unresolvable hostname.")
#Appends the number of dots in the hostname
for i in urlArrayFiltered:
    dotDomain = urlparse(i[1]).netloc
    dotCountHostname = dotDomain.count(".")
    i.append(dotCountHostname)
#Appends number of hyphens in the hostname.
for i in urlArrayFiltered:
    hyphenDomain = urlparse(i[1]).netloc
    hyphenCountHostname = hyphenDomain.count("-")
    i.append(hyphenCountHostname)
#Appends number of underscores in the hostname.
for i in urlArrayFiltered:
    underscoreDomain = urlparse(i[1]).netloc
    underscoreCountHostname = underscoreDomain.count("_")
    i.append(underscoreCountHostname)
#Appends the number of digits in the hostname to the Array.
for i in urlArrayFiltered:
    digitsDomain = urlparse(i[1]).netloc
    digitCount = 0 
    for x in digitsDomain:
        if x.isdigit():
            digitCount = digitCount+1
        else:
            digitCount = digitCount
    i.append(digitCount)
# Regex for checking if string is ASCII or not.
onlyAscii = lambda s: re.match('^[\x00-\x7F]+$', s) != None
# Adds new column and adds whether or not the URL is ASCII or not.
for i in urlArrayFiltered:
    if onlyAscii(i[1]) == True:
        i.append("ASCII")
    else:
        i.append("Not ASCII")


print(urlArrayFiltered)