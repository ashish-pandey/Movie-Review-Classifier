import pickle
from sklearn.cross_validation import train_test_split
from sklearn import svm

X_train = []
Y_train = []
total_docs = {}
total_words = {}
trainx = []
trainy = []
testx = []
testy = []
#temp_vector = []*8*13157

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
		self.sw = []
		self.ww = {}
		self.wws = {}
		self.freq = []
		self.freq.append(0)
		self.freq.append(0)



if __name__ == '__main__':
	docFile = 'allDocs.pickle'
	wordFile = 'allWords.pickle'
	print "reading pickle files"
	total_docs = pickle.load(open(docFile , 'rb'))
	total_words = pickle.load(open(wordFile , 'rb'))
	print "Building Feature and prediction vectors"
	print(len(total_words))
	for d in total_docs:
		temp_vector = []
		for w in total_words:
			if w in total_docs[d].words:
				temp_vector.append(total_words[w].wws[d][0])
			else:
				temp_vector.append(0)

		X_train.append(temp_vector)
		Y_train.append(total_docs[d].pol)

	trainx , testx , trainy , testy = train_test_split(X_train, Y_train, test_size=0.1, random_state=43)
	#apply svm and save the result
	print "Training the dataset"
	trainedSet = svm.LinearSVC()
	trainedSet.fit(trainx , trainy)
	accuracy = trainedSet.score(testx , testy)
	print accuracy
	filename = 'trainedSVM.sav'
	pickle.dump(trainedSet , open(filename , 'wb') , protocol=2)
	


