import os                                                                                                          
from os.path import isfile , join
import re
import pickle
import warnings
from math import log
from nltk.stem.snowball import SnowballStemmer

def warn(*args , **kwargs):
	pass

warnings.warn = warn

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
text_to_verify_list = ["The movie was not upto the mark as the actors were bad" , "The movie was a big superhit. I liked the movie",
                       "The story revolves around the actors trying to find a gold mine. Pointless plot with some good acting" ]
text_to_verify = "The story revolves around the actors trying to find a gold mine. Pointless plot with some good acting"

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


def preProcessText():
	line = text_to_verify
	line = re.sub(r'[^\x00-\x7F]+' , '' , line)
	line = re.sub('[,`=."!0-9()#<*>\-/?:;_\']' , ' ' , line)
	temp_words = line.split(' ')

	max_wt = 0
	docList = {}
	d = document(uq_id , 1)

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
			X_label.append(ww1*sw1)
		else:
			X_label.append(0)



if __name__ == '__main__':
	print("getting total words")
	#get the trained words
	total_words = pickle.load(open('allWords.pickle' , 'rb'))
	#print(len(total_words))
	#build the unique word dictionary
	for w in total_words:
		wordDict[total_words[w].value] = total_words[w].id

	#get all the negative and positive files
	preProcessText()
	print("Getting the Trained model....")
	trainedSet = pickle.load(open('trainedSVM.sav' , 'rb'))
	output = trainedSet.predict(X_label)
	if output[0] ==1:
		result = "positive"
	else:
		result = "negative"
	print(result)
