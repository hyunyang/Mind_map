print('------- Mind_Map_Project -------')

import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import time
import os
import networkx as nx

from bokeh.io import show, output_file
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxSelectTool
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.palettes import Spectral4
from bokeh.models import ColumnDataSource,LabelSet,CustomJSTransform
from bokeh.transform import transform

# -------------------- Open positive_words file that has words from my Mind_Map --------------------

posFile = open('./positive_words.csv', 'r')
# print(type(posFile))

posListWords = []
header = posFile.readline()
# print(type(posListWords))

while True:
    content = posFile.readline()
    content = content.replace("\n"," ")
    if len(content) == 0:
        break
    else:
        posListWords.append(content)

for idx in range(len(posListWords)):
    # print(file)
    print(posListWords[idx])

posFile.close()


# -------------------- Figuring out the frequency of words --------------------

posWordsDict = dict()
# print(posWordsDict)

for idx1 in range(len(posListWords)):
    phrase = posListWords[idx1]
    splitWords = phrase.split()
    numSplitWords = len(splitWords)
    # print(len(phrase))
    # print(len(splitWords))

    for idx2 in range(numSplitWords):
        if splitWords[idx2] in posWordsDict:
            posWordsDict[splitWords[idx2]] = posWordsDict[splitWords[idx2]] + 1
        else:
            posWordsDict[splitWords[idx2]] = 1

# print(posWordsDict)


# -------------------- Basic canvas layout setting part --------------------

dictPosition = len(posWordsDict)
# print(type(dictPosition))

x = np.random.rand(dictPosition)
y = np.random.rand(dictPosition)

nodeLabel = []
nodeSize = []

for key in posWordsDict.keys():
    nodeLabel.append(key)
#     print(key, ": ", posWordsDict[key])
    nodeSize.append(posWordsDict[key]*25)
# nodeLabel = list(posWordsDict.keys())
# nodeSize = list(posWordsDict.values())
# print(nodeLabel)
# print(nodeSize)

f = go.FigureWidget(
    data = go.Scatter(
        x = x,
        y = y,
        mode = 'markers + text',
        text = nodeLabel,
        marker = dict(size = nodeSize, color = ['#d8b65c']*dictPosition)
    ),
    layout = go.Layout(
        plot_bgcolor = 'black', # or 'white'
        height = 1000,
        width = 1000,
        font = dict(family = 'Helvetica', size = 15, color = '#ffffff')
    )
)


# -------------------- Make a short sentence by clicking three words --------------------

totalClickedNum = 0
clickedNodeText = []
scatter = f.data[0]

def update_point(trace, points, selector):
    global totalClickedNum
    global clickedNodeText
    idx3 = points.point_inds[0]

    print(trace['text'][idx3])

    c = list(trace.marker.color)
    c[idx3] = '#4a9878'
    # print(c)

    clickedNodeText.append(trace['text'][idx3])
    totalClickedNum = totalClickedNum + 1
    # print(clickedNodeText)
    print(totalClickedNum)

    with f.batch_update():
        if totalClickedNum == 3:
            newPhrase = " "
            for testText in clickedNodeText:
                newPhrase += testText + " "
                print(testText, end = " ")
            print()
            totalClickedNum = 0
            clickedNodeText = []

            scatter.marker.color = ['#d8b65c']*dictPosition
            # print(scatter.marker.color)

            if os.path.isfile("posWords_dataSet.txt"):
                oFile = open("posWords_dataSet.txt", "a+")
            else:
                oFile = open("posWords_dataSet.txt", "a+")
                oFile.write("Phrase\tcreateTime\n")

            oFile.write(newPhrase + "\t" + str(datetime.today()) + "\n")
            oFile.close()

        else:
            scatter.marker.color = c

scatter.on_click(update_point)

f.update_xaxes(showticklabels=False)
f.update_yaxes(showticklabels=False)
f


# -------------------- Graph drawing part --------------------
# -------------------- Of the words combination result from above --------------------

G = nx.DiGraph()

posResult = open("/Users/hyun/Downloads/project_programming/posWords_dataSet.txt", "r")
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


# -------------------- Graph drawing with more function part --------------------
# -------------------- Of the words combination result from above --------------------

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
        node_color='#1d1e3a',
        node_shape='h', #node_shape="d,h,o,p,s,v,x,"
        alpha=0.7, #node transparancy rate out of '1'
        linewidths=4,
        font_size=10,
        font_color='#45e2e4',
        font_weight='bold',
        width=1,
        edge_color='#ff4e60'
       )

# -------------------- Setting a Plot option part --------------------

plot = Plot(plot_width=1000, plot_height=750,
            x_range=Range1d(-1.2, 1.2), y_range=Range1d(-1.2, 1.2))
plot.title.text = "My Positive Words Graph (hold 'shift' key for multi-clicking)"

plot.add_tools(HoverTool(tooltips=None), TapTool(), BoxSelectTool())

# -------------------- Edge adding in Graph part --------------------

popular = dict()
G = nx.DiGraph()
for line in posWordsList:
    words = line.split()
    # adding edge
    G.add_edge(words[0], words[1])
    G.add_edge(words[1], words[2])
    # word-frequency
    for word in words:
        if word in popular.keys():
            popular[word] += 1
        else:
            popular[word] = 1

# -------------------- node size setting part --------------------

for i in list(G.nodes()):
    G.nodes[i]['popular'] = popular[i] * 12

# -------------------- graph rendering part --------------------

graph_renderer = from_networkx(
    G,
    nx.circular_layout,
    #layout type -> nx.circular_layout, nx.spring_layout, nx.planar_layout, nx.spiral_layout,
    scale=1,
    center=(0, 0))
graph_renderer.node_renderer.glyph = Circle(size='popular', fill_color=Spectral4[0])
graph_renderer.node_renderer.selection_glyph = Circle(size=20, fill_color=Spectral4[1])
graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[2])

graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.4, line_width=5)
graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[0], line_width=2)
graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[3], line_width=2)
#Spectral4[] -> 0 = blue, 1 = green, 2 = orange, 3 = red

# -------------------- setting detail options part --------------------

source = graph_renderer.node_renderer.data_source
# print(source.data)

source.data['name'] = [x for x in source.data['index']]
# print(source.date['name'])

# create a transform that can extract the acutal x,y positions
code = """
    var result = new Float64Array(xs.length)
    for (var i = 0; i < xs.length; i++) {
        result[i] = provider.graph_layout[xs[i]][%s]
    }
    return result
"""

xcoord = CustomJSTransform(v_func=code % "0", args=dict(provider=graph_renderer.layout_provider))
ycoord = CustomJSTransform(v_func=code % "1", args=dict(provider=graph_renderer.layout_provider))

# Use the transforms to supply coords to a LabelSet
labels = LabelSet(x=transform('index', xcoord),
                  y=transform('index', ycoord),
                  text='name', text_font_size="12px",
                  x_offset=-10, y_offset=-5,
                  source=source, render_mode='canvas')

plot.add_layout(labels)

graph_renderer.selection_policy = NodesAndLinkedEdges()
graph_renderer.inspection_policy = EdgesAndLinkedNodes()

plot.renderers.append(graph_renderer)

# -------------------- save and draw in a file part --------------------

output_file("./myFavoriteWords.html")
show(plot)

print('-------------------- FINISH Mind_Map_Project using PYTHON --------------------')
