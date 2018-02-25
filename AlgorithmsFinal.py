"""
Austin Baysinger
Algorithms Final
12/11/17
"""

import math
import numpy
import networkx as nx

"""
Problem 1
The solution to this problem uses the textbooks implementation of Merge
Sort along with a slight modification to track reverses during the sorting
procedure.
"""

def mergeReverses(A, p, q, r):      # Merge Sort with a counter
    reverseCount = 0                # added counter variable
    n1 = q - p + 1
    n2 = r - q
    L = [0] * (n1)
    R = [0] * (n2)
    for i in range(0,n1):
        L[i] = A[p + i]
    for j in range(0,n2):
        R[j] = A[q + j + 1]
    i = 0
    j = 0
    k = p
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            A[k] = L[i]
            i += 1
        else:                                               # if L value > R value (reverse)
            A[k] = R[j]
            reverseCount = reverseCount + (n1 + j - k + p) # calculate displacement of L[i] in terms of L and R as a whole and increment
            j += 1
        k += 1
    while i < n1:
        A[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        A[k] = R[j]
        j += 1
        k += 1
    return reverseCount

def numReverses(A, p, r):                   # Merge driver adapted to pass the counter value along steps of recursion
    if p < r:
        q = math.floor((p + r) / 2)
        left = numReverses(A, p, q)
        right = numReverses(A, q+1, r)
        merged = mergeReverses(A, p, q, r)
        return left + right + merged
    return 0

randomArray = [0] * 100                 # two test arrays: one randomized, one with values 1 to 100 in reverse order
maxReverseArray = [0] * 100
counter = 100
for i in range(0,100):
    randomArray[i] = numpy.random.randint(0,100)
for i in range(0,100):
    maxReverseArray[i] = counter
    counter-=1
x = numReverses(randomArray,0,99)
y = numReverses(maxReverseArray,0,99)
print("Problem 1")
print("Number of reverses in randomized array: ", x)
print("Number of reverses in fully reversed array: ", y)





"""
Problem 3
My solution to this problem uses DFS to topologically 
reverse sort the vertices from the fly to the spider. 
Then the algorithm can start from the fly and count paths 
to the fly as it works its way to the spider.

Reference to CLRS pg.604 and pg.613 pertaining to DFS and topological sort
"""

def DFSvisit(G, u, topSort):                # textbook implementation of DFS
    G.add_node(u,color="gray")              # modified to append "finished" vertices to a list
    for v in G.neighbors(u):                # this list will be the graph topologically sorted
        if G.node[v]['color'] == "white":
            DFSvisit(G,v,topSort)
    G.add_node(u,color="black")
    topSort.append(u)

def DFS(G):
    topSort = list()
    for u in nx.nodes(G):
        G.add_node(u,color="white")
    for u in nx.nodes(G):
        if G.node[u]['color'] == "white":
           DFSvisit(G, u, topSort)
    return topSort

def spiderToFly(G):
    vertPathCount = {"Fly" : 1}                     # start from the fly and initialize its path count to 1
    orderVertList = DFS(G)                          # retrieve a topological sorting of the graph starting from the fly
    del orderVertList[0]
    for i in orderVertList:                     
        vertPathCount[i] = 0                        # initialize new path count for i to 0
        vertPrev = G.successors(i)                  # check all vertices next from the current one
        for j in vertPrev:
            vertPathCount[i] += vertPathCount[j]    # summate their path counts; this represents number of paths from vertex i to the fly
    return vertPathCount["Spider"]                  # at the end, the path count associated with the spider will be the total number of paths to the fly

G = nx.DiGraph()
G.add_edge('Spider', 'A', weight=1.0)
G.add_edge('Spider', 'H', weight=1.0)
G.add_edge('Spider', 'J', weight=1.0)

G.add_edge('H', 'G', weight=1.0)
G.add_edge('H', 'K', weight=1.0)

G.add_edge('G', 'L', weight=1.0)
G.add_edge('G', 'F', weight=1.0)

G.add_edge('F', 'E', weight=1.0)

G.add_edge('E', 'Fly', weight=1.0)

G.add_edge('J', 'S', weight=1.0)
G.add_edge('J', 'K', weight=1.0)

G.add_edge('K', 'L', weight=1.0)
G.add_edge('L', 'M', weight=1.0)
G.add_edge('M', 'N', weight=1.0)
G.add_edge('M', 'F', weight=1.0)

G.add_edge('N', 'O', weight=1.0)
G.add_edge('N', 'E', weight=1.0)

G.add_edge('O', 'Fly', weight=1.0)

G.add_edge('A', 'S', weight=1.0)
G.add_edge('A', 'B', weight=1.0)

G.add_edge('B', 'R', weight=1.0)
G.add_edge('B', 'C', weight=1.0)

G.add_edge('S', 'R', weight=1.0)
G.add_edge('R', 'Q', weight=1.0)

G.add_edge('Q', 'C', weight=1.0)
G.add_edge('Q', 'P', weight=1.0)

G.add_edge('C', 'D', weight=1.0)
G.add_edge('D', 'Fly', weight=1.0)
G.add_edge('P', 'D', weight=1.0)
G.add_edge('P', 'O', weight=1.0)
G.add_edge('O', 'Fly', weight=1.0)

G.add_edge('T', 'Q', weight=1.0)
G.add_edge('T', 'P', weight=1.0)
G.add_edge('T', 'O', weight=1.0)
G.add_edge('T', 'N', weight=1.0)
G.add_edge('T', 'M', weight=1.0)

G.add_edge('R', 'T', weight=1.0)
G.add_edge('S', 'T', weight=1.0)
G.add_edge('J', 'T', weight=1.0)
G.add_edge('K', 'T', weight=1.0)
G.add_edge('L', 'T', weight=1.0)

numPaths = spiderToFly(G)
print("Problem 4")
print("Number of paths from spider to fly: ", numPaths)





"""
Problem 4
My solution to this problem assumes distances between people have 
already been calculated and placed in a matrix. The matrix must also
abide by the other constraints listed in the problem.
"""

def dryOrWet(M, n):
    A = ["Dry"] * n                             # array holding states of people on plane
    for i in range(0, n):
        minIndex = M[i].index(min(M[i]))        # find position of min value in each row
        A[minIndex] = "Wet"                     # update that position in A
    return A

M = [[100,1,4],[1,100,3],[4,3,100]]             # simple test for n = 3, 100 is used for edges between a person and him/herself
A = dryOrWet(M, 3)
print("Problem 5")
print("List of people after balloons thrown: ", A)
