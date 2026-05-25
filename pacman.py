#! /usr/bin/python3

from collections import deque
import random
import time

class DisjointSet:
    def __init__(self, vertex):
        # Connected component features:
        self.vertex = vertex
        self.parent = None
        self.children = []
        self.size = 1
    
    def setParent(self, parent):
        self.parent = parent
        self.parent.children.append(self)
        self.parent.size += self.size

    def getParent(self):
        return self.parent
    
    def getSize(self):
        return self.size
    
    def __eq__(self, other):
        return self.vertex == other.vertex
    
    def find(self):
        curr = self

        while curr.getParent() is not None:
            curr = curr.getParent()

        return curr
    
    def getVertex(self):
        return self.vertex
    
    def _strHelper(self):
        string = ""

        if self.parent is None:
            string += "{"

        string += str(self.vertex)

        for child in self.children:
            string += ", " + child._strHelper()

        if self.parent is None:
            string += "}"

        return string
    
    def __str__(self):

        """ String representation of the connected component.
        Pre-order traversal of tree rooted at the representative.
        Example:
        self.getVertex() = (6,4)
        Connected component tree:
                   (5,3) (rep)
                 //     \\
             (5,4)       (4,2)
            //   \\     //   \\
        (6,4)  (4,3)  (4,1)  (5,2)
        
        self.__str__(): '{(5, 3), (5, 4), (6, 4), (4, 3), (4, 2), (4, 1), (5, 2)}'
        """
        rep = self.find()
        return rep._strHelper()

class Square:
    def __init__(self, vertex):

        # Maze node features:
        self._neighbors = []
        self.vertex = vertex

        # Distances from a reference node. May be overwritten.
        self.dist1 = 0
        self.dist2 = 0

    def getNeighbors(self):
        return self._neighbors
        
    def addNeighbor(self, other):
        self._neighbors.append(other)
        other._neighbors.append(self)

    def isNeighbor(self, vertex):

        for n in self._neighbors:
            if vertex == n.getVertex():
                return True
            
        return False
    
    def __eq__(self, other):
        return self.vertex == other.vertex
    
    def getVertex(self):
        return self.vertex

class MazeNode:
    """ === MazeNode ===
    This class serves as both a node within a connected component to be used in
    the DisjointSetUnion class, as well as a node within a maze grid with 0 to
    4 neighbors to be used in the Maze class.
    """
    def __init__(self, vertex):
        self.square = Square(vertex)
        self.disjointSet = DisjointSet(vertex)

class DisjointSetUnion:
    """ === DisjointSetUnion ===
    A set of connected components.
    Usage:
    - makeSet: Add a new connected component and initialize its representative.
    - find: Find the representative of a connected component given by a node within.
    - union: Combine two connected components into one.
    Invariants:
    - Representative vertices are unique: len(sets.keys()) == len(set(sets.keys()))
    - Sets are disjoint: sum([len(self.sets[s]) for s in self.sets]) ==
                         (len(self.sets[1]|...|self.sets[n]) for all n keys of self.set)
    """
    def __init__(self):
        # Dictionary representing set collection
        # representative vertex: Tuple -> connected component: MazeNode
        self.sets = {}
    def __str__(self):
        """ String representation of DSU
        Example:
        DSU: 3 sets; first set contains (1, 2), (2, 3), (2, 4) with representative (2, 3).
             second set contains (4, 5), (5, 5) with representative (5, 5)
             third set contains (5, 6) with representative (5, 6).
        self.__str__(): 
        '''{{(1, 2), (2, 3), (2, 4)} rep=(2, 3),
           {(4, 5), (5, 5)} rep=(5, 5),
           {(5, 6)} rep=(5, 6)}
        '''
        """ 
        string = "{"
        for s in self.sets.keys():
            string += str(self.sets[s]) + " rep=" + str(self.sets[s].find().getVertex()) + ",\n"
        string = string[:-2 if len(self.sets) > 0 else len(string)] + "}"
        return string
    def makeSet(self, node):
        # O(1)
        self.sets[node.getVertex()] = node
    def find(self, tree):
        # O(height of tree)
        return tree.find()
    def union(self, node1, node2):
       # O(height of tallest tree + len(sets)) = O(max(height of tallest tree, len(sets)))
        rep1 = self.find(node1) # O(height of tree)
        rep2 = self.find(node2)
        if rep2 != rep1:
            if rep2.getSize() < rep1.getSize():
                temp = rep2.find().getVertex()
                rep2.setParent(rep1)
                self.sets.pop(temp) # O(len(sets)) = O(number of connected components)
            else:
                temp = rep1.find().getVertex()
                rep1.setParent(rep2)
                self.sets.pop(temp)
            return True
        else:
            return False

"""
dsu = DisjointSetUnion()
print(str(dsu))
print("add a=(1, 2)")
a = dsu.makeSet((1, 2))
print(str(dsu))
print("add b=(2, 3)")
b = dsu.makeSet((2, 3))
print(str(dsu))
print("add c=(2, 4)")
c = dsu.makeSet((2, 4))
print(str(dsu))
print("union b and c")
dsu.union(c, b)
print(str(dsu))
print("union b and a")
dsu.union(a, b)
print(str(dsu))
"""

class Maze:
    def __init__(self, w, h):
        self.width = w
        self.height = h

        # Adjacency list representing adjacent spaces with no wall in between.
        # 0 <= len(graph[(x, y)]) <= 4 for all (x, y).
        self.graph = {}
        for x in range(w):
            for y in range(h):
                self.graph[(x, y)] = MazeNode((x, y))
    # def _fillGridTemp(self):
    #     for x in range(self.width):
    #         for y in range(self.height):
    #             adjacentCoords = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    #             for c in adjacentCoords:
    #                 if 0 <= c[0] < self.width and 0 <= c[1] < self.height:
    #                     self.graph[(x, y)].addNeighbor(self.graph[c])
    # def _testLessThanDegreeTemp(self):
    #     self._fillGridTemp()
    #     a = (0, 1)
    #     b = (2, 3)
    #     print("dist(A, B) < 4", self._lessThanDegree(self.graph[a], self.graph[b], 4))
    #     print("dist(A, B) < 5", self._lessThanDegree(self.graph[a], self.graph[b], 5))
    def _lessThanDegree(self, x, y, degree):
        # Check if MazeNode <x> is less than <degree> degrees apart from 
        # Mazenode <y>.
        # Pre-condition: <x> and <y> are nodes on a connected graph.

        # Queue of nodes in breadth-first search traversals.
        currx = x
        curry = y
        queuex = deque([x])
        queuey = deque([y])

        # Set of nodes in the outer layer of explored nodes from BFS.
        # Invariant:
        # max(dist1 of nodes in setx) - min(dist1 of nodes in setx) <= 1,
        # max(dist2 of nodes in sety) - min(dist2 of nodes in sety) <= 1
        # Distances of all elements (from <x> or <y>) may vary by at most 1.
        setx = {x.getVertex()}
        sety = {y.getVertex()}

        # Already explored nodes.
        visitedx = {x.getVertex()}
        visitedy = {y.getVertex()}

        # Reset node distances.
        # Note: Other node distances don't need to be reset since distx/disty
        # are only checked on visited nodes with updated distances.
        x.dist1 = 0
        x.dist2 = 0
        y.dist1 = 0
        y.dist2 = 0

        # Bidirectional BFS from <x> and <y>.
        while currx.dist1 < degree and len(queuex) > 0 and len(queuey) > 0:
            # BFS on <x>
            currx = queuex.popleft()
            setx.remove(currx.getVertex())
            for n in currx.getNeighbors():
                if n.getVertex() not in visitedx:
                    if n.getVertex() in sety:
                        # Path found: Node is in outer layer of both BFS traversals.
                        if currx.dist1 + 1 + n.dist2 < degree:
                            # Node is in outer layer of both BFS traversals and
                            # sum of distances is less than <degree>. Distance
                            # between <x> and <y> is less than <degree>.
                            return True
                        else:
                            # Node is in outer layer of both BFS traversals and
                            # sum of distances is at least <degree>. Due to the
                            # invariant on dist1/dist2 within setx and sety, there
                            # cannot exist a shorter path. Therefore, distance
                            # between <x> and <y> is greater than <degree>.
                            return False
                    n.dist1 = currx.dist1 + 1
                    setx.add(n.getVertex())
                    visitedx.add(n.getVertex())
                    queuex.append(n)
            # BFS on <y>
            curry = queuey.popleft()
            sety.remove(curry.getVertex())
            for n in curry.getNeighbors():
                if n.getVertex() not in visitedy:
                    if n.getVertex() in setx:
                        if n.dist1 + curry.dist2 + 1 < degree:
                            return True
                        else:
                            return False
                    n.dist2 = curry.dist2 + 1
                    sety.add(n.getVertex())
                    visitedy.add(n.getVertex())
                    queuey.append(n)
        # If all nodes are visited and searches don't meet, or if the BFS
        # from <x> has already reached a depth of <degree>, the shortest
        # path between <x> and <y> is longer than <degree>.
        return False
    def setup(self):
        edgesLst = deque([])
        dsu = DisjointSetUnion()
        for x in range(self.width - 1):
            for y in range(self.height - 1):
                edgesLst.append((self.graph[(x, y)], self.graph[(x + 1, y)]))
                edgesLst.append((self.graph[(x, y)], self.graph[(x, y + 1)]))
                dsu.makeSet(self.graph[(x, y)].disjointSet)
        for x in range(self.width - 1):
            edgesLst.append((self.graph[(x, self.height - 1)], self.graph[(x + 1, self.height - 1)]))
            dsu.makeSet(self.graph[(x, self.height - 1)].disjointSet)
        for y in range(self.height - 1):
            edgesLst.append((self.graph[(self.width - 1, y)], self.graph[(self.width - 1, y + 1)]))
            dsu.makeSet(self.graph[(self.width - 1, y)].disjointSet)
        dsu.makeSet(self.graph[(self.width - 1, self.height - 1)].disjointSet)
        random.shuffle(edgesLst)
        edges = deque(edgesLst)
        while len(edges) > 0:
            edge = edges.popleft()
            vertex1 = edge[0]
            vertex2 = edge[1]
            isDisjoint = dsu.union(vertex1.disjointSet, vertex2.disjointSet)
            if isDisjoint:
                vertex1.square.addNeighbor(vertex2.square)
            else:
                isSmallCycle = self._lessThanDegree(vertex1.square, vertex2.square, 6)
                if not isSmallCycle:
                    vertex1.square.addNeighbor(vertex2.square)
    def __str__(self):
        string = ""
        for x in range(self.width - 1):
            if self.graph[(x, 0)].square.isNeighbor((x + 1, 0)):
                string += "__"
            else:
                string += "  "
        string += "\n"
        for y in range(1, self.height):
            for x in range(self.width - 1):
                if self.graph[(x, y)].square.isNeighbor(((x, y - 1))):
                    string += "|"
                else:
                    string += ","
                if self.graph[(x, y)].square.isNeighbor(((x + 1, y))):
                    string += "_"
                else:
                    string += " "
            if self.graph[(self.width - 1, y)].square.isNeighbor(((self.width - 1, y - 1))):
                string += "|"
            else:
                string += ","
            string += "\n"
        return string

myMaze = Maze(18, 18)
myMaze.setup()
print(str(myMaze))