from random import random
import random

# from GraphInterface import GraphInterface
from my_node import my_node
from my_pokemon import my_pokemon
from my_agents import my_agent


class my_graph ():

    """
    def __init__(self, nodes: dict, node_edge: dict):
        # dict of nodes: key = node_id, value = node object
        self.nodes = nodes
        # dict of edge: key = src node, value = dict, that key = dest node, value = weight of edge
        self.node_edge = node_edge
        self.node_Size = len(nodes.values())
        # dict of pokemons: key = id pokemon, value = pokemon object
        self.pokemons = {}
        self.mc = 0
        sum = 0
        for x in self.node_edge.keys():
            sum += len(node_edge.get(x))
        self.edge_Size = sum
    """

    def __init__(self):

        # dict of nodes: key = node_id, value = node object
        self.nodes = {}
        # dict of edge: key = src node, value = dict, that key = dest node, value = weight of edge
        self.node_edge = {}
        # list of pokemons
        self.pokemons = []
        # dict of agents: key = id agent, value = agents object
        self.agents = {}

        self.node_Size = 0
        self.mc = 0
        self.edge_Size = 0

    def node_size(self) -> int:
        return self.node_Size

    def edge_size(self) -> int:
        return self.edge_Size

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        # this edge already exist
        if self.node_edge.__contains__(id1) and self.node_edge.get(id1).__contains__(id2):
            return False
        else:
            # the nodes exists
            if self.nodes.__contains__(id1) and self.nodes.__contains__(id2):
                # if this key already exist so update it - add to his dictionary the new edge
                if self.node_edge.__contains__(id1):
                    self.node_edge.get(id1).update({id2: weight})
                # if this key not exist so add to edge_node dictionary the new edge
                else:
                    self.node_edge.update({id1: {id2: weight}})
                self.edge_Size += 1
                self.mc += 1
                return True
            else:
                return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        # this node already exist
        if self.nodes.__contains__(node_id):
            return False
        else:
            # create a new node from the data obtained in the functions
            if pos is None:
                x = random.randint(32, 35)
                x += random.random()
                y = random.randint(32, 35)
                y += random.random()
                new_node = my_node(node_id, x, y, 0)
            else:
                new_node = my_node(node_id, float(pos[0]), float(pos[1]), float(pos[2]))

            # update the dict of nodes, and edge_node
            self.nodes.update({node_id: new_node})
            self.node_edge.update({node_id: {}})
            self.node_Size += 1
            self.mc += 1
            return True

    def add_pokemon(self, type: int, value: float, pos: tuple = None) -> bool:
        # this pokemon already exist
            # create a new pokemon from the data obtained in the functions
            if pos is None:
                x = random.randint(32, 35)
                x += random.random()
                y = random.randint(32, 35)
                y += random.random()
                new_pos = (x, y, 0)
                edge = self.edge_pokemon(new_pos, type)
                new_pokemon = my_pokemon(type, value, edge[0], edge[1], x, y, 0)
            else:
                edge = self.edge_pokemon(pos, type)
                new_pokemon = my_pokemon(type, value, edge[0], edge[1], float(pos[0]), float(pos[1]), float(pos[2]))

            # update the dict of pokemon
            self.pokemons.append(new_pokemon)
            self.mc += 1
            return True

    # this function get pos of pokemon and return id src and id dest of the edge on which the pokemon is located
    def edge_pokemon(self, pos: tuple, type: int) -> (int, int):

        x = float(pos[0])
        y = float(pos[1])
        min_len = 1000000
        min_i = -1.000000000000000000000
        min_j = -1.00000000000000000000000

        for i in self.node_edge.keys():
            for j in self.node_edge.get(i).keys():
                node_src = self.nodes.get(i)
                node_dest = self.nodes.get(j)

                x_src = node_src.pos.get('x')
                y_src = node_src.pos.get('y')
                x_dest = node_dest.pos.get('x')
                y_dest = node_dest.pos.get('y')

                # dis between the src node to the dest node
                dis_nodes = (((x_src-x_dest)**2) + ((y_src-y_dest)**2)) **0.5
                # dis between the src node to the pokemon
                dis_src = (((x_src-x)**2) + ((y_src-y)**2)) **0.5
                # dis between the dest node to the pokemon
                dis_dest = (((x_dest-x)**2) + ((y_dest-y)**2)) **0.5
                # dis between the dest node to the pokemon + dis between the dest node to the pokemon
                dis_pok = dis_dest+dis_src
                # epsilon for inaccuracy - because of the amount of digits after the point
                e = 0.004
                #if the distances are equal
                if ((dis_nodes == dis_pok) or (abs(dis_nodes-dis_pok) <= e)) and (abs(dis_nodes-dis_pok) < min_len):
                    min_len = abs(dis_nodes-dis_pok)
                    min_i = i
                    min_j = j

        # if the type of the pokemon is equal to this edge, when i is the src and j is the dest
        if type < 0: #((min_i < min_j) and (type > 0)) or ((min_i > min_j) and (type < 0)) :
            return max(min_i,min_j), min(min_i,min_j)
        elif type > 0:
            return min(min_i,min_j), max(min_i,min_j)
        # if the pokeons not located on edge
        return -1,-1


    def add_agent(self, id: int, value: float, src :int, dest :int, speed: float, pos: tuple = None) -> bool:
        # this agent already exist
        if self.agents.__contains__(id):
            return False
        else:
            # create a new agent from the data obtained in the functions
            if pos is None:
                x = random.randint(32, 35)
                x += random.random()
                y = random.randint(32, 35)
                y += random.random()
                new_agent = my_agent(id, value, src, dest, speed, float(pos[0]), float(pos[1]), float(pos[2]))
            else:
                new_agent = my_agent(id, value, src, dest, speed, float(pos[0]), float(pos[1]), float(pos[2]))
            # update the dict of agent
            self.agents.update({id: new_agent})
            self.mc += 1
            return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        # this edge exist
        if self.node_edge.__contains__(node_id1) and self.node_edge.get(node_id1).__contains__(node_id2):
            self.node_edge.get(node_id1).__delitem__(node_id2)
            self.edge_Size -= 1
            self.mc += 1
            return True
        # this edge not exist
        else:
            return False

    def remove_node(self, node_id: int) -> bool:
        # if this node exist
        if self.nodes.__contains__(node_id):
            # delete from the nodes dict
            self.nodes.__delitem__(node_id)
            # delete the edge that this node is their src:
                # count the number of edges
            sum = len(self.node_edge.get(node_id))
            self.node_edge.__delitem__(node_id)
            self.edge_Size -= sum
            self.mc += sum
            # delete the edge that this node is their dest:
            for i in self.node_edge.keys():
                for j in self.node_edge.get(i).keys():
                    # if this node is dest of edge, delete this edge
                    if j == node_id:
                        self.node_edge.get(i).__delitem__(node_id)
                        self.edge_Size -= 1
                        self.mc += 1
                        # if in src node, you find dest node, that it is the node_id, break of the loop and go to the next i.
                        # because not exist more edge that start in this src, and end in this dest.
                        break
            self.node_Size -= 1
            self.mc += 1
            return True
        else:
            return False

    def get_all_v(self) -> dict:
        return self.nodes.__str__()

    def all_in_edges_of_node(self, id1: int) -> dict:
        if self.node_edge.__contains__(id1):
            dict_dest = {}
            for i in self.node_edge.keys():
                for j in self.node_edge.get(i).keys():
                    if j == id1:
                        dict_dest.update({i: self.node_edge.get(i).get(j)})
                        break
            return dict_dest
        else:
            return None

    def all_out_edges_of_node(self, id1: int) -> dict:
        if self.node_edge.__contains__(id1):
            return self.node_edge.get(id1).__str__()
        else:
            return None

    def __repr__(self):
        return f"Graph: |V|={self.node_Size}, |E|={self.edge_Size}"