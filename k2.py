import sys

import networkx as nx

import csv

import matplotlib.pyplot as plt

import numpy as np

import math

from functools32 import lru_cache

import pandas as pd

G = nx.DiGraph()

dataFrame = []


def write_gph(dag, filename):
    with open(filename, 'w') as f:
        for edge in dag.edges():
            f.write("{}, {}\n".format(edge[0], edge[1]))


@lru_cache(maxsize = 32768)
def countNum(node, nodeVal, j, parentConfigTable, parentIndices):
    numHits = 0
    if len(parentConfigTable) !=0:
        parentValueList = list(np.unravel_index(j, parentConfigTable))
        qString = ''
        for i in range(0, len(parentValueList)):
            qString = qString + parentIndices[i] + '==' + str(parentValueList[i] + 1) + ' and '
        qString = qString + node + '==' + str(nodeVal +1)
        return len(dataFrame.query(qString))
    else:
        qString = node + '==' + str(nodeVal + 1)
        return len(dataFrame.query(qString))


def computeBayeScore(numPossibleValues, VarToIndex):
    r = dict()
    q = dict()
    for node in G.nodes():
        q[node] = 1
        r[node] = numPossibleValues[VarToIndex[node]]
        for edge in G.predecessors(node):
            q[node] = q[node] * numPossibleValues[VarToIndex[edge]]
    score = 0
    # i in K2 alg
    for node in G.nodes():
        q_i = q[node]
        r_i = r[node]
        parentConfigs = []
        parents = []
        for parent in G.predecessors(node):
            parents.append(parent)
            parentConfigs.append(r[parent])
        tupParConfigs = tuple(parentConfigs)
        parents = tuple(parents)
        # j in K2 alg
        for j in range(0, q_i):
            a_ij0 = r_i
            m_ij0 = 0
            # k in K2 alg
            k_sum = 0
            for k in range(0, r_i):
                m_ijk = countNum(node, k, j, tupParConfigs, parents)
                m_ij0 = m_ij0 + m_ijk
                k_sum = k_sum + math.lgamma(m_ijk + 1)
            score = score + math.lgamma(a_ij0) - math.lgamma(a_ij0 + m_ij0) + k_sum
    return score


def K2(numPossibleValues, VarToIndex, dataFrame):
    Nodes = G.nodes()
    bayeScore = computeBayeScore(numPossibleValues, VarToIndex)
    nodeRemoved = False
    for node in Nodes:
        for possibleParent in Nodes :
            if (node!= possibleParent and len(G.in_edges(node)) < 8 and (possibleParent != 'OUTCOME')):
                G.add_edge(possibleParent, node)
                if (nx.is_directed_acyclic_graph(G) == False):
                    G.remove_edge(possibleParent, node)
                    nodeRemoved = True
                if (nodeRemoved == False):
                    currScore = computeBayeScore(numPossibleValues, VarToIndex)
                    if (currScore > bayeScore):
                        bayeScore = currScore
                    else:
                        G.remove_edge(possibleParent, node)
                nodeRemoved = False


def compute(infile, outfile):
    global G
    global dataFrame
    global removedNodes
    removedNodes = []
    DataArr = []
    NodeList = []
    numPossibleValues = []
    VarToIndex = dict()
    blacklist = set(['HOME_FOR1_HOME','HOME_FOR2_HOME', 'HOME_CENTER_HOME', 'HOME_GUARD1_HOME', 'HOME_GUARD2_HOME', 'HOME_6MAN_HOME', 'AWAY_FOR1_HOME','AWAY_FOR2_HOME', 'AWAY_CENTER_HOME', 'AWAY_GUARD1_HOME', 'AWAY_GUARD2_HOME', 'AWAY_6MAN_HOME'])
    blacklistIndices = set()
    with open(infile) as csvfile:
         reader = csv.reader(csvfile)
         firstLineRead = False
         for row in reader:
            if firstLineRead:
                CurrList = []
                count = 0
                for num in row:
                    if count not in blacklistIndices:
                        CurrList.append((int)(num) + 1)
                    count = count + 1
                DataArr.append(np.array(CurrList))
            else:
                count = 0
                for node in row:
                    if str(node) not in blacklist:
                        NodeList.append(str(node))
                        VarToIndex[NodeList[len(NodeList) - 1]] = len(NodeList) - 1
                    else:
                        blacklistIndices.add(count)
                    count = count + 1
                firstLineRead = True
    DataArr = np.array(DataArr)
    for node in NodeList:
        G.add_node(node)
    numPossibleValues= np.amax(DataArr, 0) 
    dataFrame = pd.DataFrame(DataArr, columns = NodeList)
    K2(numPossibleValues, VarToIndex, dataFrame)
    print (str(computeBayeScore(numPossibleValues, VarToIndex)))
    plt.subplot(121)
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()

def main():
    if len(sys.argv) != 3:
        raise Exception("usage: python project1.py <infile>.csv <outfile>.gph")

    inputfilename = sys.argv[1]
    outputfilename = sys.argv[2]
    compute(inputfilename, outputfilename)
    
if __name__ == '__main__':
    main()
