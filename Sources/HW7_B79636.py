#####################################################################
###EX4
import snap
import matplotlib.pyplot as plt

gh = snap.LoadEdgeList(snap.PUNGraph, "facebook/0.edges", 0, 1)
DegToCntV1 = snap.TIntPrV()
snap.GetDegCnt(gh, DegToCntV1)
print("Number of nodes::" + str(snap.CntNonZNodes(gh)))
print("Number of edges::" + str(snap.CntUniqUndirEdges(gh)))
facebook_hist={}
for item in DegToCntV1:
    facebook_hist[item.GetVal2()] = item.GetVal1()
plt.bar(facebook_hist.keys(), facebook_hist.values(), color='g')
fig_size = [14, 7]
plt.rcParams["figure.figsize"] = fig_size
plt.show()

gh2 = snap.LoadEdgeList(snap.PUNGraph, "facebook/348.edges", 0, 1)
DegToCntV2 = snap.TIntPrV()
snap.GetDegCnt(gh2, DegToCntV2)
print("Number of nodes::" + str(snap.CntNonZNodes(gh2)))
print("Number of edges::" + str(snap.CntUniqUndirEdges(gh2)))
f2_hist={}
for item in DegToCntV2:
    f2_hist[item.GetVal2()] = item.GetVal1()
    
plt.bar(map(str, f2_hist.keys()), f2_hist.values(), color='y')
plt.xticks(rotation=90)
plt.show()

gh3 = snap.LoadEdgeList(snap.PUNGraph, "facebook/107.edges", 0, 1)
DegToCntV3 = snap.TIntPrV()
snap.GetDegCnt(gh3, DegToCntV3)
print("Number of nodes::" + str(snap.CntNonZNodes(gh3)))
print("Number of edges::" + str(snap.CntUniqUndirEdges(gh3)))
f3_hist={}
for item in DegToCntV3:
    f3_hist[item.GetVal2()] = item.GetVal1()
plt.bar(map(str, f3_hist.keys()), f3_hist.values(), color='r')
plt.xticks(rotation=90)
plt.show()

gh4 = snap.LoadEdgeList(snap.PUNGraph, "facebook/686.edges", 0, 1)
DegToCntV4 = snap.TIntPrV()
snap.GetDegCnt(gh4, DegToCntV4)
print("Number of nodes::" + str(snap.CntNonZNodes(gh4)))
print("Number of edges::" + str(snap.CntUniqUndirEdges(gh4)))
f4_hist={}
for item in DegToCntV4:
    f4_hist[item.GetVal2()] = item.GetVal1()
plt.bar(map(str, f4_hist.keys()), f4_hist.values(), color='b')
plt.xticks(rotation=90)
plt.show()



#####################################################################
###EX5


import time

def bfs(graph, start):
    special = 666
    visited, queue = set(), [start, special]
    depth = 0
    while len(queue) > 1:
        vertex = queue.pop(0)
        if vertex == special:
            depth = depth + 1;
            queue.append(special);
        elif vertex not in visited:
            visited.add(vertex)
            queue.extend(set([Id for Id in graph.GetNI(vertex).GetOutEdges()]) - visited)
    #print depth
    return depth

graphs = [gh, gh2, gh3, gh4]
for g in graphs:
    Rnd = snap.TRnd(53)#seed
    deptharray = []
    starttime = time.time()
    for i in range(0, 1000):
        Rnd.Randomize()
        start = g.GetRndNId(Rnd)
        depth = bfs(g, start)
        deptharray.append(depth)
    t = time.time() - starttime
    diameter = max(deptharray)
    print("Running Time::" + str(t) + "sec, Dia::" + str(diameter))
	
######################################################################
##EX6

def coloring(graph, start):
    special = 666
    visited, queue = set(), [start, special]
    depth = 0
    black, red = set(), set()
    isBlack = True
    while len(queue) > 1:
        vertex = queue.pop(0)
        if vertex == special:
            depth = depth + 1;
            queue.append(special);
            isBlack = not isBlack;
        elif vertex not in visited:
            visited.add(vertex)
            if isBlack == True:
                black.add(vertex)
            else:
                red.add(vertex)
            queue.extend(set([Id for Id in graph.GetNI(vertex).GetOutEdges()]) - visited)
    return black, red

graphs = [gh, gh2, gh3, gh4]
for g in graphs:
    Rnd = snap.TRnd(53)#seed
    Rnd.Randomize()
    start = g.GetRndNId(Rnd)
    black, red = coloring(g, start)
    for edge in g.Edges():
        src = edge.GetSrcNId()
        dst = edge.GetDstNId()
        if (src in black and dst in black) or (src in red and dst in red):
            print("Biparitite Detected::Src" + str(src) + ",dst::" + str(dst))
            break
			
	
#######################################################################
###EX7

graphs = [gh, gh2, gh3, gh4]
for g in graphs:
    deptharray = []
    for i in range(0, 1000):
        Rnd.Randomize()
        start = g.GetRndNId(Rnd)
        depth = bfs(g, start)
        deptharray.append(depth)
    diameter = max(deptharray)
    print("Dia::" + str(diameter))
    DegToCnt = snap.TIntPrV()
    snap.GetDegCnt(g, DegToCnt)
    print("Number of nodes::" + str(snap.CntNonZNodes(g)))
    print("Number of edges::" + str(snap.CntUniqUndirEdges(g)))
    hist={}
    for item in DegToCnt:
        hist[item.GetVal2()] = item.GetVal1()
    plt.bar(hist.keys(), hist.values(), color='r')
    fig_size = [14, 7]
    plt.rcParams["figure.figsize"] = fig_size
    plt.show()
    
    Rnd = snap.TRnd(53)#seed
    Rnd.Randomize()
    start = g.GetRndNId(Rnd)
    black, red = coloring(g, start)
    
    dell = snap.TIntV()
    delList = []
    for edge in g.Edges() :
        src = edge.GetSrcNId()
        dst = edge.GetDstNId()
        if (src in black and dst in black) or (src in red and dst in red):
            if not src in delList:
                delList.append(src)
                dell.Add(src)
          
    snap.DelNodes(g, dell)
            
    deptharray = []
    for i in range(0, 1000):
        Rnd.Randomize()
        start = g.GetRndNId(Rnd)
        depth = bfs(g, start)
        deptharray.append(depth)
    diameter = max(deptharray)
    print("Dia::" + str(diameter))
    
    snap.GetDegCnt(g, DegToCnt)
    print("Number of nodes::" + str(snap.CntNonZNodes(g)))
    print("Number of edges::" + str(snap.CntUniqUndirEdges(g)))
    hist={}
    for item in DegToCnt:
        hist[item.GetVal2()] = item.GetVal1()
    plt.bar(hist.keys(), hist.values(), color='g')
    fig_size = [14, 7]
    plt.rcParams["figure.figsize"] = fig_size
    plt.show()