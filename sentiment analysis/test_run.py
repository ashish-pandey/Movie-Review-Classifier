import os   
import warnings                                                                                                       
from os.path import isfile , join
import re
import pickle

def warn(*args , **kwargs):
	pass

warnings.warn = warn

total_words = {}
test_documents = {}
wordMap = {}
stopwords = {}
uq_id = 1
wordDict = {}
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
		self.sw = [] #contains sentiment weighting
		self.wws = {} #contains the final weight of rhis word in each document
		self.freq = []
		self.freq.append(0)
		self.freq.append(0)
		self.orList = []
		self.orList.append(0)
		self.orList.append(0)


if __name__ == '__main__':
	print("getting total words")
	#get the trained words
	total_words = pickle.load(open('allWords.pickle' , 'rb'))
	print(len(total_words))
	#get the total_documents
	print("getting documents")
	test_documents = pickle.load(open('testDocuments.pickle' , 'rb'))
	#get the trained model
	print("getting trained model")
	trained_model = pickle.load(open('trainedSVM.sav' , 'rb'))
	print "Building Feature and prediction vectors"
	cnt = 0
	for d in test_documents:
		temp_vector = []
		c = 0
		for w in total_words:
			if w in test_documents[d].words:
				temp_vector.append(test_documents[d].words[w])
			else:
				temp_vector.append(0)
		X_label.append(temp_vector)
		Y_label.append(test_documents[d].pol)

	accuracy = trained_model.score(X_label , Y_label)
	print(accuracy)

