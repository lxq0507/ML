import sys
import re
import copy
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer
import pickle

def main():
    f = open(sys.argv[2], 'r')
    line = f.readline()
    Treviews = []
    vectorizer = CountVectorizer(min_df=1)

    Treviews.append(line)

    f.close()

    f1 = open("f1", 'rb')
    count_v1 = pickle.load(f1)
    f1.close()

    count_v2 = CountVectorizer(vocabulary=count_v1.vocabulary_);
    counts_test = count_v2.fit_transform(Treviews);

    f2 = open("f2", 'rb')
    clf = pickle.load(f2)
    f2.close()

    #print clf.predict(counts_test)
    result = clf.predict(counts_test)

    for i in range (len(result)):
        if result[i] == "__label__2":
            result[i] = '1'
        else:
            result[i] = '0'

    fOut = open("output.txt", "w+")
    fOut.write(result[0])
    fOut.close()


if __name__=="__main__":
    main()
