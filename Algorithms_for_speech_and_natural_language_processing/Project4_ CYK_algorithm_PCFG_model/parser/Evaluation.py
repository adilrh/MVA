from __future__ import division
import sys
import nltk
from nltk import Tree


class Evaluation:
    def __init__(self,ground_truth_path,predicted_path):
        self.ground_truth_path = ground_truth_path
        self.predicted_path = predicted_path
        self.ground_truth = []
        self.predicted = []
        self.lines_1 = []
        self.precision = 0
        self.recall = 0
        self.f1_score = 0
        self.accuracy = 0
    
    def preprocess_eval(self):
        with open(self.ground_truth_path) as f:
            lines = f.readlines()
        lines = list(map(lambda x: x.rstrip(),lines))
        for i in range(len(lines)):
            self.ground_truth.append(Tree.fromstring(lines[i]).productions())
        with open(self.predicted_path) as f:
            self.lines_1 = f.readlines()
        self.lines_1 = list(map(lambda x: x.rstrip(),self.lines_1))
        for i in range(len(self.lines_1)):
            self.predicted.append(Tree.fromstring(self.lines_1[i]).productions())


    def Precision(self):
        count = 0
        length = 0
        for grdtruth, predict in zip(self.ground_truth,self.predicted):
            length += len(grdtruth)
            for prod in predict:
                if prod in grdtruth:
                    count += 1
        self.precision = count/length

    def Recall(self):
        count = 0
        length = 0
        for grdtruth, predict in zip(self.ground_truth,self.predicted):
            length += len(predict)
            for prod in predict:
                if prod in grdtruth:
                    count += 1
        self.recall = count/length

    def F1_score(self):
        self.f1_score = 2*(self.precision*self.recall)/(self.precision+self.recall)

    def true_predicted(self):
        count = 0
        for x,y in zip(self.ground_truth,self.predicted):
            if x==y:
                count+=1
        self.accuracy = count/len(self.ground_truth)
        return count

    def false_predictions(self):
        L1 = []
        index = []
        count = 0
        for x,y in zip(self.ground_truth,self.predicted):
            if x!=y:
                L1.append(self.lines_1[count])
                index.append(count)
            count+=1
        return L1,index



if __name__ == "__main__":
    ground_truth_path = sys.argv[1]
    predicted_path = sys.argv[2]
    output_path = sys.argv[3]
    evaluation = Evaluation(ground_truth_path,predicted_path)
    evaluation.preprocess_eval()
    evaluation.Precision()
    evaluation.Recall()
    evaluation.F1_score()
    precision  = evaluation.precision
    print("Precision = ", precision)
    recall  = evaluation.recall
    print("Recall = ", recall)
    f1_score = evaluation.f1_score
    print("F1 score = ", f1_score)
    true_predictions = evaluation.true_predicted()
    print("The number of correct predictions is : ", true_predictions)
    L1,index = evaluation.false_predictions()
    accuracy = evaluation.accuracy
    print("The accuracy is then : ", accuracy)
    
    thefile = open(output_path, 'w')
    thefile.write("Precision = %s\n" % round(precision,4))
    thefile.write("Recall = %s\n" % round(recall,4))
    thefile.write("F1 score = %s\n" % round(f1_score,4))
    thefile.write("The number of correct predictions is : %s\n" % true_predictions)
    thefile.write("The accuracy is then : : %s\n" % round(accuracy,4))
    thefile.write("The sentences false grammar predictions are :\n ")
    for i in range(len(L1)):
        thefile.write(" \nSentence number %s:\n " % index[i])
        thefile.write("%s" % L1[i])


