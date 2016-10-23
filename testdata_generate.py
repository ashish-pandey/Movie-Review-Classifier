import os                                                                                                          
from os.path import isfile , join
import re
import pickle
from math import log
from nltk.stem.snowball import SnowballStemmer

test_documents = {}
total_words = {}
wordMap = {}
stopwords = {}
uq_id = 1
wordDict = {}
stemmer = SnowballStemmer("english")
featureVector = [] #saves the feature vector as a list for each document
polVector = [] #saves the pol of each document
X_label = []
Y_label = []

class document:
	def __init__(self , self_id , pol):
		self.id = self_id
		self.words = {}
		self.pol = pol

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
		self.documents = {} #contains documents and word weighting
		self.sw = {} #contains sentiment weighting
		self.wws = {} #contains the final weight of rhis word in each document
		self.freq = []
		self.freq.append(0)
		self.freq.append(0)
		self.orList = []
		self.orList.append(0)
		self.orList.append(0)


def readTestFiles(path , polVal , pol):
	global uq_id
	global featureVector
	path = join(path , polVal)
	allfiles = os.listdir(path)
	print(len(allfiles))
	i = 0
	for f in allfiles:
		i += 1
		f1 = open(join(path , f) , 'r')
		for line in f1:
			line = re.sub(r'[^\x00-\x7F]+' , '' , line)
			line = re.sub('[,`=."!0-9()#<*>\-/?:;_\']' , ' ' , line)
			temp_words = line.split(' ')

		max_wt = 0
		docList = {}
		polVector.append(pol)
		d = document(uq_id , pol)
		uq_id +=1 

		for w in temp_words:
			w = stemmer.stem(w)
			w = str(w).lower()
			w = w.strip(' ')
			if w not in wordDict:
				continue
			if w not in d.words:
				d.words[wordDict[w]] = 0

			d.words[wordDict[w]] +=1
			if max_wt<d.words[wordDict[w]]:
				max_wt = d.words[wordDict[w]]

		for w in total_words:
			if w in d.words:
				sw1 = total_words[w].sw[0]
				sw2 = total_words[w].sw[1]
				ww1 = d.words[w]
				ww2 = 0.5 + (0.5*d.words[w])/max_wt
				#wws = [ww1*sw1 , ww2*sw1 , ww1*sw2 , ww2*sw2]
				d.words[w] = sw1*ww1

		test_documents[d.id] = d



if __name__ == '__main__':
	path = os.getcwd()
	path = join(path , 'dataset')
	path = join(path , 'test')
	print("getting total words")
	#get the trained words
	total_words = pickle.load(open('allWords.pickle' , 'rb'))
	print(len(total_words))
	#build the unique word dictionary
	for w in total_words:
		wordDict[total_words[w].value] = total_words[w].id

	#get all the negative and positive files
	readTestFiles(path , 'pos' , 1)
	readTestFiles(path , 'neg' , 0)

	print("writing to file")
	filename = "testDocuments.pickle"
	pickle.dump(test_documents , open(filename , 'wb'))

