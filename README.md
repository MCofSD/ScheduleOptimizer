# ScheduleOptimizer
Python Script to handle Rehearsal Schedule Optimization for community bands
 
BACKGROUND: 
This is a Schedule Optimizer Python Script that Musicians' Club uses to minimize the "total wait time" of our members. 
Instead of one set group of performers on each instrument, Musicians' Club has historically swapped out members given 
their abilities and availability on each song, and intentionally chose not to create distinct "subgroups" as a way to
encourage a healthy community among all participants. This does however, lead to some difficult scheduling challenges,
and that's what this program is here to help with.

ACTION + INPUT:
Calling this script should be as easy as "python so.py yourfile.csv", (it used to be called ScheduleOptimizer.py but
that became cumbersome to type out everytime) where "yourfile.csv" is a csv file with the first row as
"Song Title, Instrument1, Instrument2, etc" and each row after being "Song Name, Performer1, Performer 2, etc".
Ensure that each performer has a unique name (if there are multiple Daniels in your group, make sure you can
differentiate them in the .csv), and that you're not having multiple unique strings for the same person (don't call him
Johnny in one song and John in another, even though it's the same person).

OUTPUT:
This script will output a new .csv that gives you all of the permutations of the set to rehearse (unless you have 9 or 
more songs to rehearse, in which case it will give you as many random permutations as your computer could handle in ~15
seconds), and the "Score", which is the sum of each person's "wait time" (how many slots inbetween a person's first song
and last song). The file name is just "yourfile Output.csv", where it will append "Output" to your file name.

From here, you can open the output file in Excel or your preferred spreadsheet editor, and sort by minimum score, or even
filter certain slots out of certain songs, if you're trying to accommodate people's schedule (someone trying to leave
early or show up late).

Happy Scheduling!
