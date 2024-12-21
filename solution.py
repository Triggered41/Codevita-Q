import math

class vertex:
    x = y = 0
    edges = set()

    def __init__(self, x, y, edges = set()) -> None:
        self.x, self.y = x, y
        self.edges = self.edges.union(edges)
    
    def get_vertex(self):
        return (self.x, self.y)
    
    def set_vertex(self, x, y):
        self.x, self.y = x, y

    def set_edges(self, edges):
        self.edges = edges
    
    def add_self(self, vertex):
        self.edges.add(vertex)
        # if (vertex != self):

    def add_edges(self, vertices):
        self.edges = self.edges.union(vertices)
        for i in vertices:
            i.add_self(self)
    
    def bisect_edge(self, x, y, edge):
        self.edges.discard(edge)
        edge.edges.discard(self)

        point = vertex(x, y, [self, edge])
        self.edges.add(point)
        edge.edges.add(point)
        return point

    def print_vertex(self, end='\n'):
        print((self.x, self.y), end=end)

    def print_edges(self):
        print((self.x, self.y), "-> ", end='')
        for i in self.edges:
            print((i.x, i.y), end=', ')
        print('')
    
    def print_all(self):
        self.print_vertex()

    def calc_slope(self, a, b):
        return (b.y - a.y)/(b.x - a.x)
    
    def calc_intercept(self, m, a):
        return a.y - m*a.x
    
    def invert_slope(self, m):
        return 0 if m==0 else -1/m
    
    def calc_intersection(self, m1, b1, m2, b2):
        if (m1-m2 == 0):
            return (0, 0)
        x = (b2-b1)/(m1-m2)
        y = m1 * x + b1
        return (x, y)
        
    def reflect(self, a, b):
        slope = self.calc_slope(a, b)
        intercept = self.calc_intercept(slope, a)

        inv_slope = self.invert_slope(slope)
        point_intercept = self.calc_intercept(inv_slope, self)
        
        intersection = self.calc_intersection(slope, intercept, inv_slope, point_intercept)
        
        self.x += 2*(intersection[0] - self.x)
        self.y += 2*(intersection[1] - self.y)
        
        self.x = round(self.x, 2)
        self.y = round(self.y, 2)

        # print(f"y = {slope}x + {intercept}")
        # print(f"y = {inv_slope}x + {point_intercept}")
        # print("Intersection:", intersection)

area = 9
side = math.sqrt(area) 

v1 = vertex(0, 0)
v2 = vertex(0, side)
v3 = vertex(side, side)
v4 = vertex(side, 0)

v1.add_edges([v2, v4])
v2.add_edges([v1, v3])
v3.add_edges([v2, v4])
v4.add_edges([v1, v3])


# Points must be the edge of square shape
bisect_line = { 'x1': 0, 'y1': 1, 'x2': 3, 'y2': 2}
p1 = v1.bisect_edge(bisect_line['x1'], bisect_line['y1'], v2)
p2 = v3.bisect_edge(bisect_line['x2'], bisect_line['y2'], v4)

v2.reflect(p1, p2)
v3.reflect(p1, p2)

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def is_intersecting(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def find_intersection(point1, point2, point3, point4):
    if (not is_intersecting(point1, point2, point3, point4)):
        return None
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    x4, y4 = point4

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denominator == 0:
        # print("Points are collinear, no unique intersection point.")
        return None

    x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
    y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator

    return round(float(x), 2), round(float(y), 2)

visited = []
queue = []
def get_all_edges():
    polygon_edges = []
    # v1.print_vertex()
    visited.append(v1)
    queue.append(v1)

    while queue:
        edge_set = []
        next = queue.pop(0)
        # next.print_edges()
        edge_set.append(next.get_vertex())
        for i in next.edges:
            edge_set.append(i.get_vertex())
        polygon_edges.append(edge_set)

        for i in next.edges:
            if i not in visited:
                visited.append(i)
                queue.append(i)
    return polygon_edges

e = get_all_edges()
intersections = set()
for row in range(0, len(e)):
    point1 = e[row][0]
    for col in range(0, len(e[row])):
        if (col != 0):
            edge1 = [point1, e[row][col]]
            for row1 in range(0, len(e)):
                if (row != row1):
                    point2 = e[row1][0]
                    for col1 in range(0, len(e[row1])):
                        if (col1 != 0):
                            edge2 = [point2, e[row1][col1]]
                            if (edge1[0] != edge2[0] and edge1[0] != edge2[1] and edge1[1] != edge2[1] and edge1[1] != edge2[0]):
                                a = find_intersection(edge1[0], edge1[1], edge2[0],edge2[1])
                                if (a != None):
                                    intersections.add(a)

tp = []
for i in e:
    tp.append(i[0])
tp += list(intersections)
print(tp)
