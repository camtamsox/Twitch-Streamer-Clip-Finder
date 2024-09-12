# Twitch Streamer Clip Finder
To use this program, follow the steps below:

Step #1: 
Get the urls from past Twith streams using urlSaver.py. To do this, navigate to a twitch streamer's past broadcasts, modify the streamer name in the python file (line 25), and run the file. Then hover over each stream you want to save, press "`" (top left on a keyboard), and finally, press "s" to save the moments to a file on your computer.

Step #2:
Download the chat data using downloadFromUrlMultiprocessing.py. To do this, change the streamer names in the list on line 53 of the python file to only include the ones with urls you have already saved to your computer. Next, run the file. Since the entire chat of a stream is very long, this process might take a while.

Step #3:
Analyze the chat data using chatAnalyzerv2.py. Again, you must modify the code to make sure it has the correct streamer name. This is done on line 104. Once you run the file, it will look at all the chats and analyze them which will take some time. When it is done, it will automatically open a past stream and tell you the time where the funniest moment happened and the number of people laughing at that second. You can do the same thing but for "sus" moments by changing the find_funny_comments variable on line 106 to False.


This program allowed me to gather many funny moments from several streamers which I then compiled and put on a YouTube channel. The channel currently has more than 60,000 total views.
<img width="959" alt="image" src="https://github.com/user-attachments/assets/a3a4d756-4ec9-4f2d-98ca-d3ec48ebc77e">
