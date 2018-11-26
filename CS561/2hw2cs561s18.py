import sys
import re
import copy
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn import svm

import matplotlib
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import precision_recall_curve


def main():
    f = open(sys.argv[2], 'r')
    line = f.readline()
    counter = 0
    reviews = []
    lables = []
    Treviews = []
    Tlables = []
    vectorizer = CountVectorizer(min_df=1)


    while line:
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

    print accuracy_score(result, Tlables)
    #print Tlables

    xx = []
    yy = []

    for i in range (len(result)):
        if result[i] == "__label__2":
            xx.append(1)
        else:
            xx.append(0)
    for i in range (len(Tlables)):
        if Tlables[i] == "__label__2":
            yy.append(1)
        else:
            yy.append(0)
    #print result

    xx = np.array(xx)
    yy = np.array(yy)
    #print Tlables

    fresult = open("fresult.txt", "w+")
    fresult.write(result)
    fresult.close()


    print "HERE!"

    false_positive_rate, true_positive_rate, thresholds = roc_curve(xx, yy, pos_label = 1)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    plt.title('Receiver Operating Characteristic')
    plt.plot(false_positive_rate, true_positive_rate, 'b',
    label='AUC = %0.2f'% roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0,1],[0,1],'r--')
    plt.xlim([-0.1,1.2])
    plt.ylim([-0.1,1.2])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()
    #plt.savefig('p-r.png')

    from sklearn.metrics import average_precision_score
    average_precision = average_precision_score(xx, yy)
    precision, recall, _ = precision_recall_curve(xx, yy)

    plt.step(recall, precision, color='b', alpha=0.2,
             where='post')
    plt.fill_between(recall, precision, step='post', alpha=0.2,
                     color='b')

    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title('2-class Precision-Recall curve: AP={0:0.2f}'.format(average_precision))
    plt.show()



    for i in range (len(result)):
        if result[i] == "__label__2":
            result[i] = 1
        else:
            result[i] = 0

    fOut = open("output.txt", "w+")
    fOut.write(result)
    fOut.close()


if __name__=="__main__":
    main()
