import sys
import re
import copy
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer
import pickle

def main():
    f = open(sys.argv[2], 'r')
    line = f.readline()
    counter = 0
    reviews = []
    lables = []
    Treviews = []
    Tlables = []
    vectorizer = CountVectorizer(min_df=1)


    for i in range (10000):
        if counter % 5 != 4:
            line = line.split()
            lables.append(line[0])
            reviews.append(line[1:])
            line = f.readline()
        else:
            line = line.split()
            Tlables.append(line[0])
            Treviews.append(line[1:])
            line = f.readline()
        counter = counter + 1

    f.close()

    for i in range (len(reviews)):
        reviews[i] = ''.join(reviews[i])

    for i in range (len(Treviews)):
        Treviews[i] = ''.join(Treviews[i])

    #print reviews

    count_v1= CountVectorizer(max_df = 0.5);
    counts_train = count_v1.fit_transform(reviews);

    f1 = open("f1", 'wb')
    pickle.dump(count_v1, f1)
    f1.close()

    print "vocabulary!"

    count_v2 = CountVectorizer(vocabulary=count_v1.vocabulary_);
    counts_test = count_v2.fit_transform(Treviews);

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(counts_train, lables)

    print "TREE!"

    f2 = open("f2", 'wb')
    pickle.dump(clf, f2)
    f2.close()

    print "DONE!"

    #print clf.predict(counts_test)


if __name__=="__main__":
    main()
