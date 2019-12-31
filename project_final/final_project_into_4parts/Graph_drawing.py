import networkx as nx

G = nx.DiGraph()

posResult = open("../posWords_dataSet.txt", "r")
# posResult = open("./posWords_dataSet.txt", "r")
header = posResult.readline()

posWordsList = []

while True:
    content = posResult.readline()
    #     content = content.replace("\n"," ")
    wordsResult = content.split("\t")
    if len(content) == 0:
        break
    #     print(wordsResult[0])
    posWordsList.append(wordsResult[0])

posResult.close()
# print(posWordsList)

for idx10 in range(len(posWordsList)):
        # print(idx10)
    phase1 = posWordsList[idx10]
    # print(phase1)
    splitWords1 = phase1.split()
        # numSplitWords1 = len(splitWords1)
        # print(phase1)
        # print(splitWords1)
        # print(numSplitWords1)

    # print('->', splitWords1[0], splitWords1[1])
    # print('->', splitWords1[1], splitWords1[2])

    G.add_edge(splitWords1[0], splitWords1[1])
    G.add_edge(splitWords1[1], splitWords1[2])
# G.add_edge("a", "c")
# G.add_edge("c","d")
# G.add_edge("e", "f")

nx.draw(G, with_labels=True)