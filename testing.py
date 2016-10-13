import pickle

listObj = [1 , 2 , 3 , 4, 5]
filename = "checkPickel.pickel"
tempObj = pickle.load(open(filename, 'rb'))
print listObj
print tempObj