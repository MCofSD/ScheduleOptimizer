''' 
This is a Schedule Optimizer Python Script that Musicians' Club uses to minimize the "total wait time" of our members. 
Instead of one set group of performers on each instrument, Musicians' Club has historically swapped out members given 
their abilities and availability on each song, and intentionally chose not to create distinct "subgroups" as a way to
encourage a healthy community among all participants. This does however, lead to some difficult scheduling challenges,
and that's what this program is here to help with.

Calling this script should be as easy as "python so.py yourfile.csv", (it used to be called ScheduleOptimizer.py but
that became cumbersome to type out everytime) where "yourfile.csv" is a csv file with the first row as
"Song Title, Instrument1, Instrument2, etc" and each row after being "Song Name, Performer1, Performer 2, etc".
Ensure that each performer has a unique name (if there are multiple Daniels in your group, make sure you can
differentiate them in the .csv), and that you're not having multiple unique strings for the same person (don't call him
Johnny in one song and John in another, even though it's the same person).

This script will output a new .csv that gives you all of the permutations of the set to rehearse (unless you have 9 or 
more songs to rehearse, in which case it will give you as many random permutations as your computer could handle in ~15
seconds), and the "Score", which is the sum of each person's "wait time" (how many slots inbetween a person's first song
and last song). The file name is just "yourfile Output.csv", where it will append "Output" to your file name.

From here, you can open the output file in Excel or your preferred spreadsheet editor, and sort by minimum score, or even
filter certain slots out of certain songs, if you're trying to accommodate people's schedule (someone trying to leave
early or show up late).

Happy Scheduling!

'''
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