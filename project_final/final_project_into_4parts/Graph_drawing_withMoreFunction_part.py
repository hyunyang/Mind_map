plt.figure(figsize = (10, 7))
G = nx.DiGraph()
posWordsResultDict = dict()
# print(posWordsResultDict)

for idx11 in range(len(posWordsList)):
    phrase2 = posWordsList[idx11]
    splitWords2 = phrase2.split()
    numSplitWords2 = len(splitWords2)
    # print(phrase2)
    # print(splitWords2))
    G.add_edge(splitWords2[0], splitWords2[1])
    G.add_edge(splitWords2[1], splitWords2[2])
    for idx12 in range(numSplitWords2):
        if splitWords2[idx12] in posWordsResultDict:
            posWordsResultDict[splitWords2[idx12]] = posWordsResultDict[splitWords2[idx12]] + 1
        else:
            posWordsResultDict[splitWords2[idx12]] = 1
# print(posWordsResultDict)

nodeSize2 = []
for key1 in posWordsResultDict.keys():
    # print(key1, ": ", posWordsResultDict[key1])
    nodeSize2.append(posWordsResultDict[key1]*1000)
# print(nodeSize2)
nx.draw(G, with_labels=True,
        node_size=nodeSize2,
        node_color='#EFC9AF',
        node_shape='h', #node_shape="d,h,o,p,s,v,x,"
        alpha=0.7, #node transparancy rate out of '1'
        linewidths=4,
        font_size=10,
        font_color='#104C91',
        font_weight='bold',
        width=1,
        edge_color='#1F8AC0'
       )