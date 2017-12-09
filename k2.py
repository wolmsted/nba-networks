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
        print ("About to process node " + node)
        for possibleParent in getAvailableNodes(node, Nodes):
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

def getAvailableNodes(node, Nodes):
    if 'HOME_FOR1' in node:
        return ['AWAY_FOR1_AST','AWAY_FOR1_BLK','AWAY_FOR1_FG3A','AWAY_FOR1_FG3M','AWAY_FOR1_FGA','AWAY_FOR1_FGM','AWAY_FOR1_FTA','AWAY_FOR1_FTM','AWAY_FOR1_MIN','AWAY_FOR1_PF','AWAY_FOR1_PTS','AWAY_FOR1_REB','AWAY_FOR1_STL','AWAY_FOR1_TO']
    elif 'HOME_FOR2' in node:
        return ['AWAY_FOR2_AST','AWAY_FOR2_BLK','AWAY_FOR2_FG3A','AWAY_FOR2_FG3M','AWAY_FOR2_FGA','AWAY_FOR2_FGM','AWAY_FOR2_FTA','AWAY_FOR2_FTM','AWAY_FOR2_MIN','AWAY_FOR2_PF','AWAY_FOR2_PTS','AWAY_FOR2_REB','AWAY_FOR2_STL','AWAY_FOR2_TO']
    elif 'HOME_GUARD1' in node:
        return ['AWAY_GUARD1_AST','AWAY_GUARD1_BLK','AWAY_GUARD1_FG3A','AWAY_GUARD1_FG3M','AWAY_GUARD1_FGA','AWAY_GUARD1_FGM','AWAY_GUARD1_FTA','AWAY_GUARD1_FTM','AWAY_GUARD1_MIN','AWAY_GUARD1_PF','AWAY_GUARD1_PTS','AWAY_GUARD1_REB','AWAY_GUARD1_STL','AWAY_GUARD1_TO']
    elif 'HOME_GUARD2' in node:
        return ['AWAY_GUARD2_AST','AWAY_GUARD2_BLK','AWAY_GUARD2_FG3A','AWAY_GUARD2_FG3M','AWAY_GUARD2_FGA','AWAY_GUARD2_FGM','AWAY_GUARD2_FTA','AWAY_GUARD2_FTM','AWAY_GUARD2_MIN','AWAY_GUARD2_PF','AWAY_GUARD2_PTS','AWAY_GUARD2_REB','AWAY_GUARD2_STL','AWAY_GUARD2_TO']
    elif 'HOME_CENTER' in node:
        return ['AWAY_CENTER_AST','AWAY_CENTER_BLK','AWAY_CENTER_FG3A','AWAY_CENTER_FG3M','AWAY_CENTER_FGA','AWAY_CENTER_FGM','AWAY_CENTER_FTA','AWAY_CENTER_FTM','AWAY_CENTER_MIN','AWAY_CENTER_PF','AWAY_CENTER_PTS','AWAY_CENTER_REB','AWAY_CENTER_STL','AWAY_CENTER_TO']
    elif 'HOME_6MAN' in node:
        return ['AWAY_6MAN_AST','AWAY_6MAN_BLK','AWAY_6MAN_FG3A','AWAY_6MAN_FG3M','AWAY_6MAN_FGA','AWAY_6MAN_FGM','AWAY_6MAN_FTA','AWAY_6MAN_FTM','AWAY_6MAN_MIN','AWAY_6MAN_PF','AWAY_6MAN_PTS','AWAY_6MAN_REB','AWAY_6MAN_STL','AWAY_6MAN_TO']
    elif 'AWAY_FOR1' in node:
        return ['HOME_FOR1_AST','HOME_FOR1_BLK','HOME_FOR1_FG3A','HOME_FOR1_FG3M','HOME_FOR1_FGA','HOME_FOR1_FGM','HOME_FOR1_FTA','HOME_FOR1_FTM','HOME_FOR1_MIN','HOME_FOR1_PF','HOME_FOR1_PTS','HOME_FOR1_REB','HOME_FOR1_STL','HOME_FOR1_TO']
    elif 'AWAY_FOR2' in node:
        return ['HOME_FOR2_AST','HOME_FOR2_BLK','HOME_FOR2_FG3A','HOME_FOR2_FG3M','HOME_FOR2_FGA','HOME_FOR2_FGM','HOME_FOR2_FTA','HOME_FOR2_FTM','HOME_FOR2_MIN','HOME_FOR2_PF','HOME_FOR2_PTS','HOME_FOR2_REB','HOME_FOR2_STL','HOME_FOR2_TO']
    elif 'AWAY_GUARD1' in node:
        return ['HOME_GUARD1_AST','HOME_GUARD1_BLK','HOME_GUARD1_FG3A','HOME_GUARD1_FG3M','HOME_GUARD1_FGA','HOME_GUARD1_FGM','HOME_GUARD1_FTA','HOME_GUARD1_FTM','HOME_GUARD1_MIN','HOME_GUARD1_PF','HOME_GUARD1_PTS','HOME_GUARD1_REB','HOME_GUARD1_STL','HOME_GUARD1_TO']
    elif 'AWAY_GUARD2' in node:
        return ['HOME_GUARD2_AST','HOME_GUARD2_BLK','HOME_GUARD2_FG3A','HOME_GUARD2_FG3M','HOME_GUARD2_FGA','HOME_GUARD2_FGM','HOME_GUARD2_FTA','HOME_GUARD2_FTM','HOME_GUARD2_MIN','HOME_GUARD2_PF','HOME_GUARD2_PTS','HOME_GUARD2_REB','HOME_GUARD2_STL','HOME_GUARD2_TO']
    elif 'AWAY_6MAN' in node:
        return ['HOME_6MAN_AST','HOME_6MAN_BLK','HOME_6MAN_FG3A','HOME_6MAN_FG3M','HOME_6MAN_FGA','HOME_6MAN_FGM','HOME_6MAN_FTA','HOME_6MAN_FTM','HOME_6MAN_MIN','HOME_6MAN_PF','HOME_6MAN_PTS','HOME_6MAN_REB','HOME_6MAN_STL','HOME_6MAN_TO']
    elif 'AWAY_CENTER' in node:
        return ['HOME_CENTER_AST','HOME_CENTER_BLK','HOME_CENTER_FG3A','HOME_CENTER_FG3M','HOME_CENTER_FGA','HOME_CENTER_FGM','HOME_CENTER_FTA','HOME_CENTER_FTM','HOME_CENTER_MIN','HOME_CENTER_PF','HOME_CENTER_PTS','HOME_CENTER_REB','HOME_CENTER_STL','HOME_CENTER_TO']
    else:
        return Nodes
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
    #write_gph(G, outfile)
    nx.write_dot(G, outfile)

def main():
    if len(sys.argv) != 3:
        raise Exception("usage: python project1.py <infile>.csv <outfile>.gph")

    inputfilename = sys.argv[1]
    outputfilename = sys.argv[2]
    compute(inputfilename, outputfilename)
    
if __name__ == '__main__':
    main()
