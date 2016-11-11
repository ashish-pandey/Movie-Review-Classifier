import sys
from textblob import TextBlob

sentinet = open('sentiWordHelp.txt', 'r')
fWT = open('WT.txt', 'r')
fTT = open('TT.txt', 'r')
fT = open('T.txt', 'r')
fPosPhrase = open('positivePhrase.txt', 'w')
fNegPhrase = open('negativePhrase.txt', 'w')
fPosSen = open('positiveSentiment.txt', 'w')
fNegSen = open('negativeSentiment.txt', 'w')
f1 = open('sarcasticTweets.txt', 'r')

sentiHelp = {}
APT = {}
WT = {}
TT ={}
T = {}
positivePhrases = []
negativePhrases = []
positiveSentiment = []
negativeSentiment = []

for line in sentinet:
	words = line.split("\t")
	sentiHelp[words[0]] = int(words[1])

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


for para in f1:
	sentences = para.split(".")
	for sentence in sentences:
		words = sentence.split(" ")
		if len(words) > 3:
			firstword = True
			sentence = TextBlob(sentence)
			senWords = []
			WordTags = []
			for t in sentence.tags:
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
			#single word phrase extraction
			for i in range(0, len(senWords)-1):
				if senWords[i] not in sentiHelp.keys():
					sentiHelp[senWords[i]] = 0
				if (WordTags[i][:1] == "V") and (sentiHelp[senWords[i]] > 0):
					positivePhrases.append(senWords[i])
				elif (WordTags[i][:1] == "V" and sentiHelp[senWords[i]] < 0):
					negativePhrases.append(senWords[i])
				elif ((WordTags[i][:1] == "N" or WordTags[i][:1] == "J") and (sentiHelp[senWords[i]] > 0)):
					positiveSentiment.append(senWords[i])
				elif ((WordTags[i][:1] == "N" or WordTags[i][:1] == "J") and (sentiHelp[senWords[i]] < 0)):
					negativeSentiment.append(senWords[i])

			#bigram phrase extraction
			for i in range(0, len(senWords)-2):
				phrase = senWords[i] + " " + senWords[i+1]
				if senWords[i] not in sentiHelp.keys():
					sentiHelp[senWords[i]] = 0
				if senWords[i+1] not in sentiHelp.keys():
					sentiHelp[senWords[i+1]] = 0
				if (WordTags[i][:1] == "V" and WordTags[i+1][:2] == "RB") or (WordTags[i][:1] == "V" and WordTags[i+1][:1] == "N") or (WordTags[i][:1] == "J" and WordTags[i+1][:1] == "V") or(WordTags[i][:2] == "RB" and WordTags[i+1][:1] == "V"):
					if sentiHelp[senWords[i]] + sentiHelp[senWords[i+1]] > 0:
						positivePhrases.append(phrase)
					elif sentiHelp[senWords[i]] + sentiHelp[senWords[i+1]] < 0:
						negativePhrases.append(phrase)
				if (WordTags[i][:1] == "N" and WordTags[i+1][:2] == "V"):
					if sentiHelp[senWords[i]] + sentiHelp[senWords[i+1]] > 0:
						positiveSentiment.append(phrase)
					elif sentiHelp[senWords[i]] + sentiHelp[senWords[i+1]] < 0:
						negativeSentiment.append(phrase)
			#trigram phrase extraction
			for i in range(0, len(senWords)-3):
				phrase = senWords[i] + " " + senWords[i+1] + senWords[i+2]
				if senWords[i] not in sentiHelp.keys():
					sentiHelp[senWords[i]] = 0
				if senWords[i+1] not in sentiHelp.keys():
					sentiHelp[senWords[i+1]] = 0
				if senWords[i+2] not in sentiHelp.keys():
					sentiHelp[senWords[i+2]] = 0
				if (WordTags[i][:1] == "V" and WordTags[i][:2] == "RB" and WordTags[i+2][:1] == "J") or (WordTags[i][:1] == "V" and WordTags[i][:1] == "J" and WordTags[i+2][:1] == "N") or (WordTags[i][:1] == "J" and WordTags[i][:2] == "RB" and WordTags[i+2][:1] == "N"):
					if sentiHelp[senWords[i]] + sentiHelp[senWords[i+1]] + sentiHelp[senWords[i+2]] > 0:
						positivePhrases.append(phrase)
					elif sentiHelp[senWords[i]] + sentiHelp[senWords[i+1]] + sentiHelp[senWords[i+2]] < 0:
						negativePhrases.append(phrase)


for phrase in positivePhrases:
	s = phrase + "\n"
	fPosPhrase.write(s)

for phrase in negativePhrases:
	s = phrase + "\n"
	fNegPhrase.write(s)

for phrase in positiveSentiment:
	s = phrase + "\n"
	fPosSen.write(s)

for phrase in negativeSentiment:
	s = phrase + "\n"
	fNegSen.write(s)


