from __future__ import division
import sys
import nltk
from nltk import Tree
from nltk.grammar import induce_pcfg, Nonterminal, is_nonterminal

class PCFG:
    def __init__(self,path):
        self.path = path
        self.all_lines = []
        self.train_set = []
        self.dev_set = []
        self.eval_set = []
        self.CFG_rules = []
        self.CNF_rules = []
        self.grammar = []
    
    
    def pre_process(self):
        #Split the data into different sets and ignoring the functional labels
        with open(self.path) as f:
            self.all_lines = f.readlines()
        for i in range(len(self.all_lines)):
            self.all_lines[i] = " ".join(map(lambda x: x[0:x.find('-')] if ('-' in x and x[0]=='(') else x,\
                                    self.all_lines[i].split()))[2:-1]
        self.train_set = self.all_lines[:round(len(self.all_lines)*0.8)]
        self.dev_set = self.all_lines[round(len(self.all_lines)*0.8):round(len(self.all_lines)*0.9)]
        self.eval_set = self.all_lines[round(len(self.all_lines)*0.9):]

    def extract_CFG_rules(self):
        #Extracting the CFG rules
        for i in range(len(self.all_lines)):
            t = Tree.fromstring(self.all_lines[i])
            self.CFG_rules += t.productions()


    def extract_CNF_rules(self):
        for i in range(len(self.all_lines)):
            t = Tree.fromstring(self.all_lines[i])
            Tree.chomsky_normal_form(t)
            self.CNF_rules += t.productions()


    def learning_CNF_probabilities(self):
        S = Nonterminal('SENT')
        self.grammar = induce_pcfg(S, self.CNF_rules).productions()
    
    

if __name__ == "__main__":
    #****************************************
    inpath = sys.argv[1]
    train_path = sys.argv[2]
    dev_path = sys.argv[3]
    eval_grd_truth = sys.argv[4]
    eval_path_txt = sys.argv[5]
    grammar_path = sys.argv[6]
    print('Preprocessing and Learning the grammar from sequoia corpus...')
    pcfg = PCFG(inpath)
    pcfg.pre_process()
    pcfg.extract_CNF_rules()
    pcfg.learning_CNF_probabilities()
    train_set = pcfg.train_set
    thefile_1 = open(train_path, 'w')
    for i in range(len(train_set)):
        thefile_1.write("%s\n" % train_set[i])
    dev_set = pcfg.dev_set
    thefile_2 = open(dev_path, 'w')
    for i in range(len(dev_set)):
        thefile_2.write("%s\n" % dev_set[i])
    eval_set = pcfg.eval_set
    thefile_3 = open(eval_grd_truth, 'w')
    for i in range(len(eval_set)):
        thefile_3.write("%s\n" % eval_set[i])
    thefile_4 = open(eval_path_txt, 'w')
    for i in range(len(eval_set)):
        sentence = ' '.join(Tree.fromstring(eval_set[i]).leaves())
        thefile_4.write("%s\n" % sentence)
    grammar = pcfg.grammar
    thefile_5 = open(grammar_path, 'w')
    for i in range(len(grammar)):
        thefile_5.write("%s\n" % grammar[i])

    
