import sys
from textblob import TextBlob

text = "I love to wait forever"

sentiNetFile = open("sentiWordHelp.txt", "r")
positiveFile = open("positivePhrase.txt", 'r')
negativeFile = open("negativePhrase.txt", 'r')
positiveSen = open("positiveSentiment.txt", 'r')
negativeSen = open("negativeSentiment.txt", 'r')
fWT = open('WT.txt', 'r')
fTT = open('TT.txt', 'r')
fT = open('T.txt', 'r')

sentiWordHelp = {}
APT = {}
WT = {}
TT ={}
T = {}
positivePhrases = {}
negativePhrases = {}
posSen = {}
negSen = {}

for line in positiveFile:
	words = line.split("\t")
	positivePhrases[words[0]] = words[0]

for line in negativeFile:
	words = line.split("\t")
	negativePhrases[words[0]] = words[0]

for line in positiveSen:
	words = line.split("\t")
	posSen[words[0]] = words[0]

for line in negativeSen:
	words = line.split("\t")
	negSen[words[0]] = words[0]

for line in sentiNetFile:
	words = line.split("\t")
	sentiWordHelp[words[0]] = int(words[1])

for line in fWT:
	words = line.split("\t")
	APT[words[0]] = []
	WT[(words[0], words[1])] = int(words[2])

for key in WT:
	APT[key[0]].append(key[1])

for line in fTT:
	words = line.split("\t")
	TT[(words[0], words[1])] = int(words[2])

for line in fT:
	words = line.split("\t")
	T[words[0]] = int(words[1])

text = TextBlob(text)
print(text.tags)
senWords = []
WordTags = []
phrasesInText = []

sentimentScore = 0

firstword = True
for t in text.tags:
	maxprob = 0
	if firstword == True:
		current_word = t[0]
		current_tag = t[1]
		if t[1] != 'CD':
			if current_word in APT.keys():
				for tag in APT[current_word]:
					tempProb = WT[(current_word, tag)]/T[tag]
					if tempProb > maxprob:
						maxprob = tempProb
						current_tag = tag
				senWords.append(current_word)
				WordTags.append(current_tag)
				firstword = False
	else:
		previous_tag = current_tag
		current_tag = t[1]
		current_word = t[0]
		if current_word in APT.keys():
			for tag in APT[current_word]:
				if (previous_tag, tag) in TT.keys():
					tempProb = (WT[(current_word, tag)] / T[tag]) * (TT[previous_tag, tag] / T[previous_tag])
					if tempProb > maxprob:
						maxprob = tempProb
						current_tag = tag
			senWords.append(current_word)
			WordTags.append(current_tag)

for i in range(0, len(senWords)):
	if senWords[i] in sentiWordHelp.keys():
		sentimentScore = sentimentScore + sentiWordHelp[senWords[i]]

#single word phrase extraction
for i in range(0, len(senWords)):
	if (WordTags[i][:1] == "V"):
		phrasesInText.append(senWords[i])
#bigram phrase extraction
for i in range(0, len(senWords)-1):
	phrase = senWords[i] + " " + senWords[i+1]
	if (WordTags[i][:1] == "V" and WordTags[i+1][:2] == "RB") or (WordTags[i][:1] == "V" and WordTags[i+1][:1] == "N") or (WordTags[i][:1] == "J" and WordTags[i+1][:1] == "V") or(WordTags[i][:2] == "RB" and WordTags[i+1][:1] == "V"):
		phrasesInText.append(phrase)
#trigram phrase extraction
for i in range(0, len(senWords)-2):
	phrase = senWords[i] + " " + senWords[i+1] + senWords[i+2]
	if (WordTags[i][:1] == "V" and WordTags[i][:2] == "RB" and WordTags[i+2][:1] == "J") or (WordTags[i][:1] == "V" and WordTags[i][:1] == "J" and WordTags[i+2][:1] == "N") or (WordTags[i][:1] == "J" and WordTags[i][:2] == "RB" and WordTags[i+2][:1] == "N"):
		phrasesInText.append(phrase)

flag = False
for phrase in phrasesInText:
	print(phrase)
	if sentimentScore > 0:
		for key in negativePhrases.keys():
			if key in phrase or phrase in key:
				print("Definite sarcasm detected with positive sentiment score.")
				flag = True
				break
	elif sentimentScore < 0:
		for key in positivePhrases.keys():
			if (key in phrase) or (phrase in key):
				print("Definite sarcasm detected with negative sentiment score.")
				flag = True
				break
	if flag == True:
		break

if flag == False:
	print("Unable to predict correctly.")


####Sarcasm paper algo######
print("Executing demo algo")
sarcasmFlag = False
positiveEncounter = False
negativeEncounter = False
phraseForWord = []
for t in text.tags:
	if t[0] in posSen.keys():
		positiveEncounter = True
		for phrase in phrasesInText:
			wordsInPhrase = phrase.split(" ")
			for word in wordsInPhrase:
				if word == t[0]:
					phraseForWord.append(phrase)
					break
		for phrase in phraseForWord:
			if phrase in negativePhrases.keys():
				sarcasmFlag = True
	if t[0] in negSen.keys():
		negativeEncounter = True
		for phrase in phrasesInText:
			wordsInPhrase = phrase.split(" ")
			for word in wordsInPhrase:
				if word == t[0]:
					phraseForWord.append(phrase)
					break
		for phrase in phraseForWord:
			if phrase in positivePhrases.keys():
				sarcasmFlag = True

if sarcasmFlag == True:
	print("Sarcasm detected bitch")
else:
	print("No sarcasm detected")
