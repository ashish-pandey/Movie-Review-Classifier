import sys
from textblob import TextBlob

WT = {}
TT = {}
T = {}

f1 = open('finalTrainingData.txt', 'r')
fWT = open('WT.txt', 'r')
fTT = open('TT.txt', 'r')
fT = open('T.txt', 'r')

for line in fWT:
	words = line.split("\t")
	WT[(words[0], words[1])] = int(words[2])

for line in fTT:
	words = line.split("\t")
	TT[(words[0], words[1])] = int(words[2])

for line in fT:
	words = line.split("\t")
	T[words[0]] = int(words[1])

for para in f1:
	sentences = para.split(".")
	for sentence in sentences:
		words = sentence.split(" ")
		if len(words) > 3:
			firstword = True
			sentence = TextBlob(sentence)
			for t in sentence.tags:
				if firstword == True:
					previous_tag = '$'
					current_tag = t[1]
					firstword = False
				else:
					previous_tag = current_tag
					current_tag = t[1]
				#Word-Tag pair occurences
				if (t[0], t[1]) not in WT.keys():
					WT[(t[0], t[1])] = 1
				else:
					WT[(t[0], t[1])] = WT[(t[0], t[1])] + 1
				#Bigram tag occurences
				if (previous_tag, current_tag) not in TT.keys():
					TT[(previous_tag, current_tag)] = 1
				else:
					TT[(previous_tag, current_tag)] = TT[(previous_tag, current_tag)] + 1
				#Tag occurences
				if current_tag not in T.keys():
					T[current_tag] = 1
				else:
					T[current_tag] = T[current_tag] + 1

fWT = open('WT.txt', 'w')
fTT = open('TT.txt', 'w')
fT = open('T.txt', 'w')

for key in WT:
	s = key[0] + '\t' + key[1] + '\t' + str(WT[key]) + '\n'
	fWT.write(s)

for key in TT:
	s = key[0] + '\t' + key[1] + '\t' + str(TT[key]) + '\n'
	fTT.write(s)

for key in T:
	s = key + '\t' + str(T[key]) + '\n'
	fT.write(s)

f1.close()
fWT.close()
fTT.close()
fT.close()