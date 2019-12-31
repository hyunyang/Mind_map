import networkx as nx

from bokeh.io import show, output_file
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxSelectTool
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.palettes import Spectral4
from bokeh.models import ColumnDataSource,LabelSet,CustomJSTransform
from bokeh.transform import transform


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