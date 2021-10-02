# IplAnalysis
Hello, This is a simple code written in python Language which read the data in csv Format with pandas as then
perform some function upon it and then give result



Basic Idea
1. We Read the data and then make sure we have all columns required, if that happens an error will be raised
2. Then we grouped our data based on match_id, and then we created a scoreboard wile looping over each match_df which basically belong to particular match_id.
3. We will create a scoreboard for each inning which give make our result more accurate.

# Please read Comment in the code for better understanding.


Naming Conventions
1. Each class has first letter as Capital.[HelloWorld]
2. Each function has all lowercase and separated by underscore(_)[hello_world]
3. Variable has first letter of word as small and from next word first letter is capital[helloWorld]


Function Used:-
1. get_scoreboard -- To get scoreboard from data. after getting the scoreboard we can simply print it
2. create_scoreboard -- To create a scoreboard of a particular inning belong to specify match.
3. is_wicket -- If someone got out we will run this function which will simply dismiss the striker or Non-Striker and add one wicket in bowler name
4. is_extra -- If there is some extra run it will add it in total score
5. declare_result -- I added this to declare result, there can be three possible, team1 win, team2 win, or tie.. so if it is a tie we will again run out loop for new inning
6. preprocess_data -- To preprocess out given data. [Filling None Value]
7. read_yaml -- To read config file
8. get_logger  - To create logger object which basically is logger object from logging module
9. log_decorator - It is decorator and is creater which will be added to some function to keep track of them.


Classes Used :-
1. Match - To store match detail
2. Teams -- It represents a single team,  a team will have maximum player as 11 if it exceeds 11 it will throw an error
3. Player -- It represents a single player which has some common attributes, like run_scored in a single match.


##  There are some common exception that can occur which I wrote in separate file named as exception.py.

How to Run Code?
1. Open terminal in the directory you download the code
2. Write the Following Command [Make sure you have python installed]

$ make

$ python app.py


Then it will automatically create Result Folder and std.log which are basically used to store the output and log of your code

Input and Output
1. I took a single file named all_matches.csv which contains large data from all Ipl held till now, and I just run my code, you can choose some other files by just copying and pasting it inside the Data Directory
2. My output is Not printed on screen but saved in a text file name after the filename of input just so it can be unique
3. Total Time Taken for input of size [3834333 * 20] is  52.054842710494995 sec.

Output --> [check Result directory for all output]
I have added a Single Result of a Tie Match Happen b/w [Rajasthan Royals vs Kolkata Knight Riders]

![1](https://user-images.githubusercontent.com/63579929/134929296-38a990fd-0367-444a-abc1-75f3a577deb7.png)
![2](https://user-images.githubusercontent.com/63579929/134929332-15dc3ea4-93f3-493f-81ae-f8c8ac31bd3f.png)

