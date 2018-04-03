from __future__ import division
import sys
import nltk
from nltk import Tree
from nltk.grammar import induce_pcfg, Nonterminal, is_nonterminal
from Code_PCFG import PCFG

class CKY:
    def __init__(self,grammar):
        self.non_terminal_dic = dict()
        self.terminals_dic = dict()
        self.grammar = grammar
        self.non_terminal = set()
        self.leaves_rules = set()
        self.unary_rules = set()
        self.binary_rules = set()
    
    def nonTerminal(self):
        for prod in self.grammar:
            if is_nonterminal(prod.lhs()):
                self.non_terminal.add(prod.lhs())
                for i in range(len(prod.rhs())):
                    y = prod.rhs()[i]
                    if is_nonterminal(y):
                        self.non_terminal.add(y)

    def leavesRules(self):
        for prod in self.grammar:
            if type(prod.rhs()[0]) == str:
                self.leaves_rules.add(prod)


    def unaryRules(self):
        for prod in self.grammar:
            if len(prod.rhs())==1 and type(prod.rhs()[0])!=str:
                self.unary_rules.add(prod)


    def binaryRules(self):
        for prod in self.grammar:
            if len(prod.rhs())==2:
                self.binary_rules.add(prod)

    

    def backtrack(self,sentence,nodes,begin,end,label):
        begin_ = begin
        end_ = end
        label_ = label
        n = len(sentence)
        if nodes[0][n][Nonterminal('SENT')] == 0:
            return None
        next_ =  nodes[begin_][end_][label_]
        if next_ == 0:
            if (begin_,end_,label_) in self.terminals_dic:
                t = Tree(str(label_),[self.terminals_dic[(begin_,end_,label_)]])
                return t
        if type(next_)!=tuple:
            label_ = next_
            t1 = self.backtrack(sentence,nodes,begin_,end_,label_)
            t = Tree(str(label),[t1])
            return t
        else:
            (split, B, C) = next_
            t1 = self.backtrack(sentence,nodes,begin,split,B)
            t2 = self.backtrack(sentence,nodes,split,end,C)
            t = Tree(str(label_),[t1,t2])
            return t





    def cky(self,sentence):
        for nonterm in self.non_terminal:
            self.non_terminal_dic[nonterm] = 0
        n = len(sentence)
        score = [[self.non_terminal_dic.copy() for i in range(n+1)] for j in range(n+1)]
        nodes = [[self.non_terminal_dic.copy() for i in range(n+1)] for j in range(n+1)]
        for i in range(n):
            for prod in self.leaves_rules:
                if prod.rhs()[0] == sentence[i]:
                    score[i][i+1][prod.lhs()] = prod.prob()
                    self.terminals_dic[(i,i+1,prod.lhs())] = sentence[i]
            added = True
            while added:
                added = False
                for prod in self.unary_rules:
                    if (score[i][i+1][prod.rhs()[0]]>0):
                        A = prod.lhs()
                        B = prod.rhs()[0]
                        proba = prod.prob()*score[i][i+1][B]
                        if proba > score[i][i+1][A]:
                            score[i][i+1][A] = proba
                            nodes[i][i+1][A] = B
                            added = True
        for span in range(2,n+1):
            for begin in range(0,n-span+1):
                end = begin+span
                for split in range(begin+1,end):
                    for prod in self.binary_rules:
                        A = prod.lhs()
                        B = prod.rhs()[0]
                        C = prod.rhs()[1]
                        proba = score[begin][split][B]*score[split][end][C]*prod.prob()
                        if proba > score[begin][end][A]:
                            score[begin][end][A] = proba
                            nodes[begin][end][A] = (split,B,C)
                added = True
                while added:
                    added = False
                    for prod in self.unary_rules:
                        A = prod.lhs()
                        B = prod.rhs()[0]
                        proba = prod.prob()*score[begin][end][B]
                        if proba > score[begin][end][A]:
                            score[begin][end][A] = proba
                            nodes[begin][end][A] = B
                            added = True

        t = self.backtrack(sentence,nodes,0,n,Nonterminal('SENT'))
        Tree.un_chomsky_normal_form(t)
        return(t)

if __name__ == "__main__":
    #****************************************
    inpath = sys.argv[1]
    eval_path = sys.argv[2]
    output_path = sys.argv[3]
    pcfg = PCFG(inpath)
    pcfg.pre_process()
    pcfg.extract_CNF_rules()
    pcfg.learning_CNF_probabilities()
    grammar = pcfg.grammar
    with open(eval_path) as f:
        lines = f.readlines()
    eval_set = list(map(lambda x: x.split(),lines))
    cky_parser = CKY(grammar)
    cky_parser.nonTerminal()
    cky_parser.binaryRules()
    cky_parser.leavesRules()
    cky_parser.unaryRules()
    thefile = open(output_path, 'w')
    print('Number of sentence to be proceeded is : ', len(eval_set))
    count = 0
    for sentence in eval_set:
        count += 1
        print('Sentence number',count,'is in process...')
        t = cky_parser.cky(sentence)
        if t is None:
            thefile.write("%s\n" % 'Not found in the Grammar')
        else:
            prediction = ' '.join(str(t).split())
            thefile.write("%s\n" % prediction)





