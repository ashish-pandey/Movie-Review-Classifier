import os
from os.path import isfile , join
import pickle

class document:
	def __init__(self , self_id , pol):
		self.id = self_id
		self.words = {}
		self.pol = pol

	def preprocess(self):
		wordList = self.text.split(" ");
		for w in wordList:
			if w not in self.words:
				self.words[w] = 0
			self.words[w] = self.words[w] + 1;

	def wordInDoc(self , word):
		if word in self.words:
			return True
		else:
			return False

	def someFunction(self):
		#do something
		print("Function Called")


class word:
	def __init__(self , self_id , value):
		self.id = self_id
		self.value = value
		self.documents = {}
		self.sw = {}
		self.ww = {}
		self.wws = {}
		self.freq = []
		self.freq.append(0)
		self.freq.append(0)



if __name__ =='__main__':
	filename = 'allWords2.pickle'
	totalwords = pickle.load(open(filename, 'rb'))
	#totaldocs = pickle.load(open('allDocs.pickle' , 'rb'))
	words = {}
	c = 0
	

	for w in totalwords:
		if totalwords[w].freq[0] + totalwords[w].freq[1] >75:
			words[totalwords[w].value] = w

	fname = "unique_words2.pickle"
	pickle.dump(words , open(fname , 'wb'))