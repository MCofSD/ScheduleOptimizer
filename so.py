import csv
from collections import defaultdict
import pprint
from itertools import permutations
import time
import sys
#will need numpy installed
from numpy import random
import numpy as np

#input: .csv file
#output: dictionary with song names as keys, list of performers as values 
def initSetlistDic(filename):
    #Open file and initialize values
    with open(filename, newline='') as csvfile:
        setlist = csv.reader(csvfile, delimiter=',')
        
        #set = setlist, with songs as keys and the values as names
        set = defaultdict(list)
        firstRow = True
        songTitle = True

        #iterating through the imported file
        for row in setlist:
            #we don't want the first row as it's just the headers
            if firstRow == True:
                    firstRow = False
            else:
                for name in row:
                    #First Item, this is the Song Title. Creating Dictionary with Song Title as Key
                    if songTitle == True:
                        currentSong = name
                        set[currentSong] = []
                        songTitle = False
                    #Adding list of Names to Dictionary with Song Title As Key.
                    else:
                        if name == '':
                            continue
                        else:
                            set[currentSong].append(name)
                            
                songTitle = True
    return set

#input: dictionary setlist
#output: number of songs in set
def numSongsInSetFcn(set):
    numSongsInSet = 0
    for row in set:
       numSongsInSet += 1 
    return numSongsInSet

#input: dictionary setlist
#output: dictionary with names as key, number of songs they are in as values
def calcSongsPerPerson(set):
    numSongsPerPerson = {}
    for song in set:
        for name in set[song]:
                if name in numSongsPerPerson:
                    numSongsPerPerson[name] = numSongsPerPerson[name] + 1
                else:
                    numSongsPerPerson[name] = 1
    return numSongsPerPerson

#input: numSongsPerPerson = dictionary of names, values = num of songs
#input: setlist = dictionary setlist
#output: list of setlist permutations, with assigned "score"
def createSetlistPermutation(numSongsPerPerson, setlist):
    perm = permutations(setlist)
    #row = one possible permutation of setlist order
    maxValue = 0
    minValue = 69420
    currRow = 0
    totalWaitTime = 0
    minTotalSet = {}
    
    if numSongsInSetFcn(setlist) < 9:
        #choosing one possible permutation of song order
        for row in list(perm):
            #we're choosing one name first, and in that name, we're going to iterate 
            #print(type(row))
            for name in numSongsPerPerson:
                for song in row:
                    if name in setlist[song]:
                        maxValue = max(maxValue, currRow)
                        minValue = min(minValue, currRow)
                    currRow += 1
                totalWaitTime = totalWaitTime + (maxValue - minValue)
                currRow = 0
                maxValue = 0
                minValue = 42069
            #print (totalWaitTime)
            minTotalSet[row] = totalWaitTime
            totalWaitTime = 0
            
    else:
        keylist = list(setlist.keys())
        t = time.process_time()
        while time.process_time() - t < 15:
            randomSet = np.random.permutation(keylist)
            row = list(randomSet)
            row = tuple(row)
            #print(type(row))
            for name in numSongsPerPerson:
                for song in row:
                    if name in setlist[song]:
                        maxValue = max(maxValue, currRow)
                        minValue = min(minValue, currRow)
                    currRow += 1
                totalWaitTime = totalWaitTime + (maxValue - minValue)
                currRow = 0
                maxValue = 0
                minValue = 42069
                #print (totalWaitTime)
            minTotalSet[row] = totalWaitTime
            totalWaitTime = 0
                
    return minTotalSet

def fileOutput(importFileName, minTotalSet, numSongs):
    export_file = importFileName
    if "Import.csv" in export_file:
      export_file = export_file.replace("Import.csv", "Export.csv")
    elif ".csv" in export_file:
      export_file = export_file.replace(".csv", " Export.csv")

    with open(export_file, 'w') as csvfile:
        #Add "Song 1, Song 2..."
        for x in range(numSongs):
            csvfile.write("Song " + str(x + 1) + "," )
        csvfile.write("Score\n")
        for key, value in minTotalSet.items():
            csvfile.write('%s, %s\n' % (key, value))

def main():
    print("START")
    arg = sys.argv[1]
    t = time.process_time()
    
    print("Creating Setlist Dictionary")
    setlist = initSetlistDic(arg)
    numSongs = numSongsInSetFcn(setlist)
    numSongsPerPerson = calcSongsPerPerson(setlist)
    
    print(str(numSongs) + " number of songs found")
    
    print("Creating Setlist Permutation")
    minTotalSet = createSetlistPermutation(numSongsPerPerson, setlist)
    
    print("Creating Output File")
    fileOutput(arg, minTotalSet, numSongs)
    elapsed_time = time.process_time() - t
    print("Total Execution Time: " + str(elapsed_time))
    
if __name__ == "__main__":
    main()  
