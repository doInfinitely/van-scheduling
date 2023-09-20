from van_scheduling import *
import random

node_count = 100
fleet_size = 30
connectivity = 3
random.seed(0)
G = initialize_network(node_count, connectivity)
fleet = Fleet(G, fleet_size)
ID = 1
distance_list = []
trips_list = []
for c in range(600):
    print(c)
    users = [User(ID+i, random.randrange(node_count), random.randrange(node_count)) for i in range(10)]
    ID += 10
    requests = [Request(x, "pickup") for x in users]
    for x in requests:
        van = fleet.get_best_van(x)
        if van is not None:
            van.schedule(x)
            van.reschedule()
    distance, trips = fleet.move()
    distance_list.append(distance)
    trips_list.append(trips)
print("average_distance ", sum(distance_list)/len(distance_list)/fleet_size)
print("average_trips ", sum(trips_list)/len(trips_list)/fleet_size)
