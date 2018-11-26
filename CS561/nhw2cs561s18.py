import sys
import re
import copy
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn import svm

def main():
    f = open(sys.argv[2], 'r')
    line = f.readline()
    counter = 0
    reviews = []
    lables = []
    Treviews = []
    Tlables = []
    vectorizer = CountVectorizer(min_df=1)


    for i in range(60000):
        line = line.split()
        if counter % 5 != 4:
            lables.append(line[0])
            reviews.append(line[1:])
            line = f.readline()
        else:
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

    #clf = tree.DecisionTreeClassifier()
    #clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=1)
    #clf = GaussianNB()
    clf = NearestCentroid()
    #clf = svm.SVC()
    clf = clf.fit(counts_train, lables)

    print "TREE!"

    f2 = open("f2", 'wb')
    pickle.dump(clf, f2)
    f2.close()

    print "DONE!"

    #print clf.predict(counts_test)


if __name__=="__main__":
    main()
