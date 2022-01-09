import json
import math
import random
from time import time
from copy import copy, deepcopy
from typing import List
from my_graph import my_graph
from my_node import my_node
from my_pokemon import my_pokemon
from my_agents import my_agent




class GraphAlgo():

    def __init__(self, graph: my_graph = None):
        self.graph = graph

    def get_graph(self) -> my_graph:
        return self.graph

    def load_graph_data(self, json_file: str) -> bool:
        new_graph = my_graph()

        list_of_data = json.loads(json_file)

        for node in list_of_data["Nodes"]:
            pos = node.get('pos').split(',', 3)
            new_graph.add_node(node.get('id'), pos)

        for edge in list_of_data["Edges"]:
            new_graph.add_edge(edge.get('src'), edge.get('dest'), edge.get('w'))

        self.graph = new_graph
        return True


    def load_pokemons(self, json_file: str) -> bool:
        self.graph.pokemons = []

        data = json.loads(json_file)

        for p in range(len(data["Pokemons"])):
            pos = data["Pokemons"][p]["Pokemon"]["pos"].split(',',3)
            value = data["Pokemons"][p]["Pokemon"]["value"]
            type = data["Pokemons"][p]["Pokemon"]["type"]
            self.graph.add_pokemon(type, value, pos)

        return True


    def load_agents(self, json_file: str) -> bool:
        self.graph.agents = {}

        data = json.loads(json_file)

        for a in range(len(data["Agents"])):
            pos = data["Agents"][a]["Agent"]["pos"].split(',', 3)
            id = data["Agents"][a]["Agent"]["id"]
            value = data["Agents"][a]["Agent"]["value"]
            src = data["Agents"][a]["Agent"]["src"]
            dest = data["Agents"][a]["Agent"]["dest"]
            speed = data["Agents"][a]["Agent"]["speed"]

            self.graph.add_agent(id, value, src, dest, speed, pos)

        return True

    def save_graph_json(self, file_name: str) -> bool:

        list_edge = []
        node_edge = self.graph.node_edge
        for n_s in node_edge.keys():
            for n_d in node_edge.get(n_s).keys():
                w = node_edge.get(n_s).get(n_d)
                edge = {"src": n_s, "w": w, "dest": n_d}
                list_edge.append(edge)

        list_node=[]
        nodes = self.graph.nodes
        for n in nodes.values():
            node = {"pos": n.get_location(), "id": n.get_id()}
            list_node.append(node)

        graph_data = {"Edges": list_edge, "Nodes": list_node}

        try:
            with open(file_name, 'w') as json_file:
                json.dump(graph_data, json_file, indent=2)
                return True

        except IOError as e:
            print(e)
            return False


    # return the shortest path from id1 to id2, and a list of all the nodes in this route between them
    def shortest_path(self, id1: int, id2: int) -> (float, list):

        route = []
        # if one of the node not exist
        if (not self.graph.nodes.__contains__(id1)) or (not self.graph.nodes.__contains__(id2)):
            return float('inf'), route
        else:
            # hash in order to update the weight of the nodes
            node = deepcopy(self.graph.nodes)

            # dict to previous node that pointed me. key - id node, value - the node that pointed at me
            pointer = {}

            # start when the weight of the node is very high, and they don't view
            for n in node.values():
                n.set_tag(0)
                n.set_weight(1000000)

            # queue for the connection nodes
            queue = []
            # the first node
            node.get(id1).set_weight(0)
            node.get(id1).set_tag(1)
            queue.append(node.get(id1))
            pointer.update({id1: None})

            # while the queue is not empty
            while queue.__len__() != 0:
                current = self.get_min(queue)
                queue.remove(current)
                if current.get_id() == id2:
                    break
                edge = deepcopy(self.graph.node_edge.get(current.get_id()))
                for e in edge.keys():
                    new_weight = current.get_weight()+edge.get(e)
                    if new_weight < node.get(e).get_weight():
                        node.get(e).set_weight(new_weight)
                        pointer.update({e: current})
                        if node.get(e).get_tag() == 0:
                            node.get(e).set_tag(1)
                            queue.append(node.get(e))

            current = node.get(id2)
            if current.get_tag() == 0:
                return float('inf'), route  # or current.get_weight()==1000000 , or pointer.get(id2) == None   -> There is no route from id1 to id2
            else:
                current_id = current.get_id()
                route.append(current_id)
                previous = pointer.get(current.get_id())
                while previous is not None:
                    current = previous
                    current_id = current.get_id()
                    route.insert(0, current_id)
                    previous = pointer.get(current.get_id())
            current_w = node.get(id2).get_weight()
            return current_w, route

    # return the node with lowest weight
    def get_min(self, queue: list) -> my_node:
        mini = queue[0]
        for current in queue:
            if mini.get_weight() > current.get_weight():
                mini = current
        return mini

    # return the center node, and the maximun distance from this node to the farest node
    def centerPoint(self) -> (int, float):
        mini = 1000000
        for n in self.graph.nodes.values():
            maxi = 0
            current_node = self.center(n.get_id())
            # found the maximum distance from node n
            for n2 in current_node.values():
                # if there is node that not view - this graph not connected
                if n2.get_tag == 0:
                    return None, float('inf')
                if n2.get_weight() > maxi:
                    maxi = n2.get_weight()
                # if there is node that not view - this graph not connected
                if maxi == 1000000:
                    return None, float('inf')
            if maxi < mini:
                mini = maxi
                ans = n
        current_id = ans.get_id()
        return current_id, mini

    # Dijkstra's_algorithm
    def center(self, node_id: int) -> dict:
        # if one of the node not exist
        if not self.graph.nodes.__contains__(node_id):
            return self.graph.nodes
        else:
            # hash in order to update the weight of the nodes
            node = deepcopy(self.graph.nodes)

            # start when the weight of the node is very high, and they don't view
            for n in node.values():
                n.set_tag(0)
                n.set_weight(1000000)

            # queue for the connection nodes
            queue = []
            # the first node
            node.get(node_id).set_weight(0)
            node.get(node_id).set_tag(1)
            queue.append(node.get(node_id))

            # while the queue is not empty
            while queue.__len__() != 0:
                current = self.get_min(queue)
                queue.remove(current)
                edge = deepcopy(self.graph.node_edge.get(current.get_id()))
                for e in edge.keys():
                    new_weight = current.get_weight() + edge.get(e)
                    if new_weight < node.get(e).get_weight():
                        node.get(e).set_weight(new_weight)
                        if node.get(e).get_tag() == 0:
                            node.get(e).set_tag(1)
                            queue.append(node.get(e))
            return node


    def TSP(self, node_lst: List[int]) -> (List[int], float):
        route = []
        dis = 0

        # the loop get the node with the min id, to start
        min_id = 1000000
        for n in node_lst:
            n_id = int(self.graph.nodes.get(n).get_id())
            if n_id < min_id:
                min_id = n_id
                min_node = self.graph.nodes.get(n)
        current = min_node
        node_lst.remove(min_node.get_id())
        route.append(min_node.get_id())

        while node_lst.__len__() != 0:
            min_id = 1000000
            # the loop get the node with the min id
            for n in node_lst:
                n_id = int(self.graph.nodes.get(n).get_id())
                if n_id < min_id:
                    min_id = n_id
                    min_node = self.graph.nodes.get(n)
                # found the short route from current node to min node
                short_route_dis, short_route_list = self.shortest_path(current.get_id(), min_node.get_id())
                # if there isn't exist route
                if short_route_dis == float('inf') or short_route_list is None:
                    return float('inf'), []
                short_route_list.pop(0)
                dis += short_route_dis
                # add the short route to route
                route.extend(short_route_list)
                node_lst.remove(min_node.get_id())

                # if there is a node in the short route list that we found, remove it from the node_lst list
                while short_route_list.__len__() != 0:
                    if node_lst.__contains__(short_route_list.__getitem__(0)):
                        node_lst.remove(short_route_list.__getitem__(0))
                    short_route_list.pop(0)
                current = min_node

        return route, dis