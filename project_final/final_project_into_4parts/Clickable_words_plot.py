import numpy as np
import plotly.graph_objects as go

# -------------------- Open positive_words file that has words from my Mind_Map --------------------

posFile = open('../positive_words.csv', 'r')
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