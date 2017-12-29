# Whatsapp chat analyzer

## Overview

This project aims to give some stats of conversations in the whatsapp application chats. It gives 6 insights into the chat:

**1.** Daily message frequency. Tells how many messages are sent every day.

**2.** Month frequency. For each month counts the number of messages sent.

**3.** Day of week frequency. 

The above 3 elements are shown in a graph.

**4.**  For each person in the chat, counts number of messages sent by each.

**5.** Counts the ocurrences of certain words. 

The later 2 are printed in console output. 

**6.** Day of week-time of day punchcard. 

This last item is exported as a csv files with the information to create a punchcard with the vertical axis being the day of week, horizontal axis being time of day (given in 24h format), and for each day of week-time of day, the size of the point.

The input for the program is a txt file from the exported conversation. In whatsapp this is done by selecting the "send by email" option. The exported conversation will be emailed in txt format.

## Dependencies

- seaborn (for daily frequency graph).
- matplotlib.pyplot
- pandas
- (optional) fogleman/Punchcard (for printing exported puchcard matrix as a png graph). It can be found [here](https://github.com/fogleman/Punchcard)

## Using this code

This code is free to use. To use, you may download or clone this repo and execute the *analyzer.py* file. Though, some configurations should be tuned in order to work correctly. First of all, change the value of the *date_config* variable in both *analyzer.py* and *date_manager.py* to match the date format of your exported chat. If you wish, you may change the *start_line* value to match a set of characters that will **not** be found in the chat exported. This is to avoid inconsistencies in data, as this value is used to identify where each message starts. You must change also the file name to match the txt file name of the chat to analyze in the code's line 23. 
