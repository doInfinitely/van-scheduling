import networkx as nx
import random
import operator

def add_random_edge(G):
    vertex_count = G.number_of_nodes()
    vertex1 = random.randrange(vertex_count)
    vertex2 = random.randrange(vertex_count)
    while vertex1 == vertex2:
        vertex2 = random.randrange(vertex_count)
    G.add_edge(vertex1, vertex2, weight=random.random())
    return G

def initialize_network(vertex_count, avg_connect):
    edge_count = vertex_count * avg_connect
    G = nx.Graph()
    for i in range(vertex_count):
        G.add_node(i)
    for i in range(edge_count):
        G = add_random_edge(G)
    while len(list(nx.connected_components(G))) > 1:
        for i in range(vertex_count):
            G = add_random_edge(G)
    return G
class User:
    def __init__(self, ID, origin, destination):
        self.ID = ID
        self.origin = origin
        self.destination = destination
class Request:
    def __init__(self, user, action):
        self.user = user
        self.action = action
        self.location = user.destination if action == "dropoff" else user.origin
    def __str__(self):
        return "User: {0}, Action: {1}, Location: {2}".format(self.user.ID, self.action, self.location)
class Van:
    def __init__(self, G):
        self.G = G
        self.queue = []
        self.history = [0]
        self.passengers = set()
    def get_next_node(self, target):
        current = self.history[-1]
        path = nx.dijkstra_path(self.G, current, target)
        #print(path)
        try:
            return path[1]
        except IndexError:
            return path[0]
    def schedule(self, request):
        self.queue.append(request)
    def distance(self, request):
        current = self.history[-1]
        return nx.dijkstra_path_length(self.G,current,request.location)
    def reschedule(self):
        self.queue = [x[1] for x in sorted([(self.distance(r),r) for r in self.queue], key=operator.itemgetter(0))]            
    def action(self):
        if self.queue[0].action == 'pickup':
            self.passengers.add(self.queue[0].user.ID)
            self.schedule(Request(self.queue[0].user, 'dropoff'))
            self.reschedule()
            del self.queue[0]
            return 0
        elif self.queue[0].action == 'dropoff':
            self.passengers.remove(self.queue[0].user.ID)
            del self.queue[0]
            return 1
    def move(self):
        try:
            target = self.queue[0].location
        except IndexError:
            target = self.history[-1]
        self.history.append(self.get_next_node(target))
        trips = 0
        while len(self.queue) and self.history[-1] == self.queue[0].location:
            trips += self.action()
        try:
            return self.G[self.history[-2]][self.history[-1]]['weight'], trips
        except KeyError:
            return 0, trips
            

class Fleet:
    def __init__(self, G, van_count):
        self.vans = [Van(G) for i in range(van_count)]
    def get_best_van(self, request):
        temp = sorted([((v.distance(request), len(v.queue)), v) for v in self.vans], key=operator.itemgetter(0))
        try:
            return temp[0][1]
        except IndexError:
            return None
    def move(self):
        distance = 0
        trips = 0
        for x in self.vans:
            d, t = x.move()
            distance += d
            trips += t
        return distance, trips

if __name__ == '__main__':
    G = nx.Graph()
    G.add_edges_from([(0, 3, {'weight': 0.1}), (0, 8,{'weight': 0.8}), (3,8,{'weight': 0.8}), (8,1, {'weight': 1.0}), (8,6, {'weight': 0.7}), (1,6, {'weight': 1.0}),  (1,4, {'weight': 0.6}),  (6,4, {'weight': 0.5}),  (6,7,{'weight': 0.9}), (4,5, {'weight': 0.5}), (4,7, {'weight': 0.4}), (4,9, {'weight': 1.0}),(7,5, {'weight': 0.8}),(7,9, {'weight': 0.4}), (2,8, {'weight': 0.7})])
    fleet = Fleet(G, 2)
    for c in range(1, 11):
        if c == 1:
            users = [User(1, 8, 9), User(2, 3, 6)]
        elif c == 2:
            users = [User(3, 4, 7), User(4, 2, 4)]
        elif c == 3:
            users = [User(5, 1, 7), User(6, 1, 9)]
        else:
            users = []
        requests = [Request(x, "pickup") for x in users]
        for x in requests:
            van = fleet.get_best_van(x)
            if van is not None:
                van.schedule(x)
                van.reschedule()
        fleet.move()
        
        for i,x in enumerate(fleet.vans):
            print(i, x.history)
            print([str(y) for y in x.queue])
            print()
