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


def readAndProcess(path , polVal , pol):
	global uq_id
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

		d = document(uq_id , pol)
		uq_id += 1
		max_wt = 0
		docList = {}

		for w in temp_words:
			w = stemmer.stem(w)
			w = str(w).lower()
			w = w.strip(' ')
			#if w not in wordDict:
			#	continue
			if len(w)<3:
				continue
			if w in stopwords:
				continue
			if w not in wordMap:
				wrd = word(uq_id , w)
				uq_id += 1
				wrd.documents[d.id] = 0
				wordMap[w] = wrd.id
				total_words[wrd.id] = wrd
			if w not in docList:
				d.words[wordMap[w]] = 0
				docList[w] = True
				total_words[wordMap[w]].orList[pol] += 1 
			total_words[wordMap[w]].freq[pol] +=1 #stores the freq of this word totally in neg or pos polarity reviews in total
			d.words[wordMap[w]] += 1
			temp_wt = d.words[wordMap[w]]
			if temp_wt > max_wt:
				max_wt = temp_wt


		total_documents[d.id] = d
		#calculate the word weighting WW(wi , dj)  here wi = ww and dj = d
		#Two metric for ww for a word wi in di:
		#1. total_documents[di].words[wi]   wi is the id here : calculated above already
		#2. total_words[wi].documents[di]   :calculted below
		for ww in d.words:
			total_words[ww].documents[d.id] = 0.5 + (0.5*int(d.words[ww]))/int(max_wt)



def calculateSW1(w):
	t1 = 1000
	t2 = 1000
	pols = total_words[w].orList
	ak = pols[0]
	bk = pols[1]
	if bk==0:
		tmp1 = 6
	else:
		tmp1 = float((1000-bk)*ak)
		tmp1 = tmp1/((1000-ak)*bk)
	if ak==0:
		tmp2 = 6
	else:
		tmp2 = float((1000-ak)*bk)
		tmp2 = tmp2/((1000-bk)*ak)
	print(ak , bk , tmp1 , tmp2)
	if tmp1==0.0:
		tmp1 = 1  #so that log makes it zero
	if tmp2 == 0.0:
		tmp2 = 1
	sw1 = max(log(tmp1 , 10) , log(tmp2 , 10))
	return sw1


def calculateSW2(w):
	return 1

def calculate_WWS():
	for w in total_words:
		wrd = total_words[w]
		sw1 = calculateSW1(w)
		sw2 = calculateSW2(w)
		for d in wrd.documents:
			ww1 = total_documents[d].words[w]
			ww2 = wrd.documents[d]
			wrd.sw[d] = [sw1 , sw2]
			wrd.wws[d] = [ww1*sw1 , ww2*sw1 , ww1*sw2 , ww2*sw2]


if __name__ =='__main__':
	#get the stop words
	f = open('stopwords.txt' , 'r')
	for line in f:
		line = line.replace('\n' , '')
		stopwords[line] = True

	#wordDict = pickle.load(open('unique_words.pickle' , 'rb'))
	#read the documents
	path = os.getcwd()
	path = join(path , 'dataset')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        	#preprocess the pos reviews first
	readAndProcess(path , 'pos' , 1)
	#preprocess the neg reviews
	readAndProcess(path , 'neg' , 0)
	#calculte vector for each word
	print "calculating wws"
	calculate_WWS()
 	print(len(wordMap) , len(total_documents) , uq_id)
 	print "words"
 	wordFile = 'allWords.pickle'
 	pickle.dump(total_words, open(wordFile, 'wb'))
 	print "documents"
 	docFile = 'allDocs.pickle'
 	pickle.dump(total_documents , open(docFile , 'wb'))
	#for w in total_words:
	#	print total_words[w].value