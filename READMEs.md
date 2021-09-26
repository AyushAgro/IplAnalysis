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

How to Run --
1. Open Terminal and make sure you are in the same directory as you downloaded file
2. In terminal run Command
$ - make
$ - python app.py

Output -->
+------------+------------------------------------------------------+-----------------------+----------+--------------+
|   Match-id | Teams                                                | Venue                 | season   | Start Date   |
+============+======================================================+=======================+==========+==============+
|     335982 | Royal Challengers Bangalore vs Kolkata Knight Riders | M Chinnaswamy Stadium | 2007/08  | 2008-04-18   |
+------------+------------------------------------------------------+-----------------------+----------+--------------+

Kolkata Knight Riders
╒═════════════════╤══════════╤═══════╤════════╤══════╤══════╕
│ Batmans         │ Status   │   Run │   Ball │   4s │   6s │
╞═════════════════╪══════════╪═══════╪════════╪══════╪══════╡
│ SC Ganguly      │ B Khan   │    10 │     12 │    2 │    0 │
├─────────────────┼──────────┼───────┼────────┼──────┼──────┤
│ BB McCullum     │ Not Out  │   158 │     73 │   10 │   13 │
├─────────────────┼──────────┼───────┼────────┼──────┼──────┤
│ RT Ponting      │ B Kallis │    20 │     20 │    1 │    1 │
├─────────────────┼──────────┼───────┼────────┼──────┼──────┤
│ DJ Hussey       │ B Noffke │    12 │     12 │    1 │    0 │
├─────────────────┼──────────┼───────┼────────┼──────┼──────┤
│ Mohammad Hafeez │ Not Out  │     5 │      3 │    1 │    0 │
├─────────────────┼──────────┼───────┼────────┼──────┼──────┤
│ AB Dinda        │          │     0 │      0 │    0 │    0 │
├─────────────────┼──────────┼───────┼────────┼──────┼──────┤
│ I Sharma        │          │     0 │      0 │    0 │    0 │
├─────────────────┼──────────┼───────┼────────┼──────┼──────┤
│ AB Agarkar      │          │     0 │      0 │    0 │    0 │
├─────────────────┼──────────┼───────┼────────┼──────┼──────┤
│ LR Shukla       │          │     0 │      0 │    0 │    0 │
╘═════════════════╧══════════╧═══════╧════════╧══════╧══════╛
Extra-17( l-4, w-9, b-4,)

Royal Challengers Bangalore
╒════════════╤═══════════╤═══════╤════════╤══════╤══════╕
│ Batmans    │ Status    │   Run │   Ball │   4s │   6s │
╞════════════╪═══════════╪═══════╪════════╪══════╪══════╡
│ P Kumar    │ Not Out   │    18 │     15 │    1 │    2 │
├────────────┼───────────┼───────┼────────┼──────┼──────┤
│ Z Khan     │ B Ganguly │     3 │      8 │    0 │    0 │
├────────────┼───────────┼───────┼────────┼──────┼──────┤
│ AA Noffke  │ Run Out   │    10 │     10 │    1 │    0 │
├────────────┼───────────┼───────┼────────┼──────┼──────┤
│ JH Kallis  │ B Agarkar │     8 │      7 │    0 │    1 │
├────────────┼───────────┼───────┼────────┼──────┼──────┤
│ SB Joshi   │ B Shukla  │     3 │      6 │    0 │    0 │
├────────────┼───────────┼───────┼────────┼──────┼──────┤
│ CL White   │ B Agarkar │     6 │     10 │    0 │    0 │
├────────────┼───────────┼───────┼────────┼──────┼──────┤
│ R Dravid   │ B Sharma  │     2 │      3 │    0 │    0 │
├────────────┼───────────┼───────┼────────┼──────┼──────┤
│ W Jaffer   │ B Dinda   │     6 │     16 │    0 │    0 │
├────────────┼───────────┼───────┼────────┼──────┼──────┤
│ V Kohli    │ B Dinda   │     1 │      5 │    0 │    0 │
├────────────┼───────────┼───────┼────────┼──────┼──────┤
│ MV Boucher │ B Ganguly │     7 │      9 │    1 │    0 │
├────────────┼───────────┼───────┼────────┼──────┼──────┤
│ B Akhil    │ B Agarkar │     0 │      2 │    0 │    0 │
╘════════════╧═══════════╧═══════╧════════╧══════╧══════╛
Extra-19( w-11, l-8,)
