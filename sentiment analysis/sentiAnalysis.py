import os                                                                                                          
from os.path import isfile , join
import re
import pickle
import warnings
from math import log
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import sentiwordnet as swn


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
text_to_verify_list = ["The movie was not upto the mark as the actors were bad" , "The movie was a big super hit. I liked the movie",
                       "The story revolves around the actors trying to find a gold mine. Pointless plot with some good acting" ]
text_to_verify = "The story revolves around the actors trying to find a gold mine. The plot was bad with some good acting"

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
	path = join(path , 'neg')
	allfiles = os.listdir(path)
	nc = 0
	pc = 0
	negc = 0
	for f in allfiles:
		f1 = open(join(path , f) , 'r')
		for line in f1:
			line = re.sub(r'[^\x00-\x7F]+' , '' , line)
			line = re.sub('[,`=."!0-9()#<*>\-/?:;_\']' , ' ' , line)
			tokens = nltk.word_tokenize(line)
		tagged = nltk.pos_tag(tokens) #for POSTagging
		neg_words = 0
		pos_words = 0
		neg_score = 0
		pos_score = 0
		for i in range(0 , len(tagged)):
			if len(tagged[i][0]) < 3:
				continue
			if tagged[i][1] == 'JJ' and len(swn.senti_synsets(tagged[i][0],'a'))>0:
				tpos = (list(swn.senti_synsets(tagged[i][0],'a'))[0]).pos_score()
				tneg = (list(swn.senti_synsets(tagged[i][0],'a'))[0]).neg_score()
				if  tpos > 0.25:
					pos_words += 1
					pos_score += tpos 
				elif tneg > 0.3:
					neg_words += 1
					neg_score += tneg

		#print(neg_words , neg_score , pos_words , pos_score)

		if neg_words%2 ==1 and neg_score > neg_words*0.4:
			negc +=1
		elif neg_words%2==0 and pos_score > pos_words*0.4:
			pc +=1
		else:
			nc +=1

	print(pc , nc , negc)
