# IplAnalysis
Hello, This is a simple code written in python Language which read the data in csv Format with pandas as then
perform some function upon it and then give result


Basic Idea
1. We Read the data and then make sure we have all columns required, if that happens an error will be raised
2. Then we Grouped our data based on match_id and then we created a scoreboard with that subData which.
3. After Getting the scoreboard, we will simply add our scoreboard to File in Tabular Form.

Function Used :-
1. get_scoreboard -- To get scoreboard from data. after getting the scoreboard we can simply print it
2. create_scoreboard -- To create a scoreboard of a particular match.
3. preprocessData -- To preprocess out given data. [Filling None Value]
$ - python app.py

How to Run Code?
1. Open terminal in the directory you download the code
2. Write the Following Command [Make sure you have python installed]
$ make
$ python app.py

Then it will automatically create Result Folder and std.log which are basically used to store the output and log of your code

Input and Output
1. I took a single file named all_matches.csv which contains large data from all Ipl held till now and i just run my code, you can choose some other files by just copy pasting it inside the Data Directory
2. My output is Not printed on screen but saved in a text file name after the filename of input just so it can be unique
3. Total Time Taken for input of size [3834333 * 20] is  52.054842710494995 sec.

Output --> [check Result directory for all output]
![1](https://user-images.githubusercontent.com/63579929/134809593-f1f3a9ba-31ac-4834-ba05-0993694a11ae.png)
![2](https://user-images.githubusercontent.com/63579929/134809607-2a327573-0e19-4c27-a239-bcfe425fb1e5.png)