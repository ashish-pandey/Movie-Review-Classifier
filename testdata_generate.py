import os                                                                                                          
from os.path import isfile , join
import re
import pickle
from math import log
from nltk.stem.snowball import SnowballStemmer

total_documents = {}
total_words = {}
wordMap = {}
stopwords = {}
uq_id = 1
wordDict = {}
stemmer = SnowballStemmer("english")
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


if __name__ == '__main__':
	path = os.getcwd()
	path = join(path , 'dataset')
	path = join(path , 'test')
	print("getting total words")
	#get the trained words
	total_words = pickle.load(open('allWords.pickle' , 'rb'))
	#get the total_documents
	print("getting total documents")
	total_documents = pickle.load(open('allDocs.pickle' , 'rb'))
	#get the trained model
	print("getting trained model")
	trained_model = pickle.load(open('trainedSVM.sav' , 'rb'))

	i = 0
	for d in total_documents: 
		temp_vector = []
		for w in total_words:
			if w in total_documents[d].words:
				temp_vector.append(total_words[w].wws[d][0])
			else:
				temp_vector.append(0)

		X_label.append(temp_vector)
		Y_label.append(total_documents[d].pol)

	accuracy = trained_model.score(X_label , Y_label)
	print(accuracy)

