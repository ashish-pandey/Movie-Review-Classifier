import numpy as np
import csv
import re

csv_file_object = csv.reader(open('twitDB_sarcasm.csv', 'rU'),delimiter='\n')

data=[]
remove_hashtags = re.compile(r'#\w+\s?')
remove_friendtag = re.compile(r'@\w+\s?')
remove_sarcasm = re.compile(re.escape('sarcasm'),re.IGNORECASE)
remove_sarcastic = re.compile(re.escape('sarcastic'),re.IGNORECASE)    

for row in csv_file_object:
    if len(row[0:])==1:
        temp=row[0:][0]
        temp=remove_hashtags.sub('',temp)
        if len(temp)>0 and 'http' not in temp and temp[0]!='@' and '\\u' not in temp: 
            temp=remove_friendtag.sub('',temp)
            temp=remove_sarcasm.sub('',temp)
            temp=remove_sarcastic.sub('',temp)
            temp=' '.join(temp.split()) #remove useless space
            if len(temp.split())>2:
                data.append(temp)

sacasticTweetsFile = open('sarcasticTweets.txt', 'w')

for i in range(0, len(data) -1):
	s = data[i] + "\n"
	sacasticTweetsFile.write(s)