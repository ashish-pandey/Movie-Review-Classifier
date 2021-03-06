import pickle
import warnings
from sklearn.cross_validation import train_test_split
from sklearn import svm

def warn(*args , **kwargs):
	pass

warnings.warn = warn


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
	print("Training the dataset.....")
	trainedSet = svm.LinearSVC()
	trainedSet.fit(trainx , trainy)
	accuracy = trainedSet.score(testx , testy)
	print("Acuuracy of the model on the sampled data: %s"   %(accuracy))
	outputs = trainedSet.predict(testx);
	# we calculate the precion and recall for both the positive and negative
	# precision means if it says 
	# if our objective is to find positive reviews then:
	#		True positve = positive items that were identified as positive
	#		True negative = negative items that were identified as negative
	#		False positive = negative items that were identified as positive
	#		False negative = positive items that were classified as negative
	p = 0
	TP = {}
	TN = {}
	FP = {}
	FN = {}
	TP['pos'] = TP['neg'] = 0
	TN['pos'] = TN['neg'] = 0
	FP['pos'] = FP['neg'] = 0
	FN['pos'] = FN['neg'] = 0
	for i in outputs:
		if i == testy[p]:
			if i==1:
				TP['pos'] +=1
				TN['neg'] +=1
			else:
				TP['neg'] +=1
				TN['pos'] +=1
		else:
			if testy[p] == 1:
				FN['pos'] +=1
				FP['neg'] +=1
			else:
				FP['pos'] +=1
				FN['neg'] +=1
		p +=1

	pos_precision = float(TP['pos'])/(TP['pos'] + FP['pos'])
	neg_precision = float(TP['neg'])/(TP['neg'] + FP['neg'])
	pos_recall = float(TP['pos'])/(TP['pos'] + FN['pos'])
	neg_recall = float(TP['neg'])/(TP['neg'] + FN['neg'])
	pos_fscore = (2*pos_recall*pos_precision)/(pos_precision+pos_recall)
	neg_fcore = (2*neg_recall*neg_precision)/(neg_precision + neg_recall)
	print("Positive:- Precision : %s , recall : %s and f-score : %s" %(pos_precision , pos_recall ,  pos_fscore))
	print("Negative:- Precision : %s , recall : %s and f-score : %s" %(neg_precision , neg_recall ,neg_fcore))
	print("Saving the Trained model......")
	filename = 'trainedSVM.sav'
	pickle.dump(trainedSet , open(filename , 'wb') , protocol=2)
	


