import sys


if __name__ == '__main__':
	sentiWords = []
	sentiScore = 0
	sentiment = 0
	word = ''
	f = open('SentiWordNet_3.0.0_20130122.txt' , 'r')
	for line in f:
		words = line.split()
		if words[0] == "#":
			continue
		elif words[0] != '':
			word = words[4]
			word = word.split("#")[0]
			sentiScore = float(words[2]) - float(words[3])
			if sentiScore < 0:
				sentiment = -1
			elif sentiScore == 0:
				sentiment = 0
			else:
				sentiment = 1
			sentiWords.append((word, sentiment, words[0]))
	
	g = open('sentiWordHelp.txt' ,'w')
	sentence = ''
	for s in sentiWords:
		sentence = s[0] + '\t' + str(s[1]) + '\t' + s[2] + '\n'
		g.write(sentence)
	
	f.close()
	g.close()
