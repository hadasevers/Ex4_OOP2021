import json
import time
from copy import deepcopy

import pygame.time

from GraphAlgo import GraphAlgo
from my_graph import my_graph
from my_node import my_node
from client import Client
from pygame import font, color, Color, draw, rect, Rect, display, MOUSEBUTTONDOWN, QUIT, RESIZABLE
from button_menu import *


# get the scaled data with proportions min_data, max_data relative to min and max screen dimensions
def scale(data, min_screen, max_screen, min_data, max_data):
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values
def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


# Calculation to find the point of intersection between the rib and the vertex - to find the tip of the arrow
def x2point(xs, ys, xd, yd, d):
    m = (ys - yd) / (xs - xd)
    n = yd - (m * xd)
    a = (1 + m * m)
    b = (-2 * xd) + (2 * n * m) - (2 * yd * m)
    c = (-(d * d)) + (xd * xd) + (yd * yd) + (n * n) - (2 * yd * n)
    x1 = (-b - ((b * b) - (4 * a * c)) ** 0.5) / (2 * a)
    x2 = (-b + ((b * b) - (4 * a * c)) ** 0.5) / (2 * a)
    return x1, x2, m, n


# Calculation to find the other 2 points of the arrow
def x1point(xd, yd, d, m1):
    if m1 == 0:
        m = 0
    else:
        m = -1 / m1
        n = yd - (m * xd)
        a = (1 + m * m)
        b = (-2 * xd) + (2 * n * m) - (2 * yd * m)
        c = (-(d * d)) + (xd * xd) + (yd * yd) + (n * n) - (2 * yd * n)
        x1 = (-b - ((b * b) - (4 * a * c)) ** 0.5) / (2 * a)
        x2 = (-b + ((b * b) - (4 * a * c)) ** 0.5) / (2 * a)
        return x1, x2, m, n


# this func choose to every agent the next node
def next_node():
    pokemons = deepcopy(g.get_graph().pokemons)
    # this loop delete from the pokemon dict, all the pokemons that have an agent very close to them
    for agent in g.get_graph().agents.values():
        for pok in pokemons:
            if (agent.get_dest() == pok.get_dest()) and (agent.get_src() == pok.get_src()):
                pokemons.remove(pok)

    # this loop updat the dest of adgent who have dest = -1
    for agent in g.get_graph().agents.values():
        next = -1
        pos_pok = None
        if agent.get_dest() == -1:
            min_route = 1000000
            # find the closest pokemons by shortest_path algo, and update the dest to be the next node in the path
            for pokemon in pokemons:
                # shortest_path return list of (len_route, list of the nodes in this route when the first node is the now location)
                short = g.shortest_path(agent.get_src(), pokemon.get_src())
                if short[0] != 'inf' and short[0] < min_route:
                    # len route
                    min_route = short[0]
                    # the second node in the path=route
                    if len(short[1]) > 1:
                        next = short[1][1]
                    else:
                        # there is route, but the len of the route is 1, so- the src of the agent = src of the pok
                        next = pokemon.get_dest()

                    # saves information about this closest pokemon to know which other pokemon to delete from the list as well
                    src_pok = pokemon.get_src()
                    dest_pok = pokemon.get_dest()

            # this loop delete all the pokemons that are on the same edge as the closest pokemon, and also the closest pokemon itself
            for pok in pokemons:
                if (pok.get_src() == src_pok) and (pok.get_dest() == dest_pok):
                    pokemons.remove(pok)

            client.choose_next_edge('{"agent_id":' + str(agent.get_id()) + ', "next_node_id":' + str(next) + '}')

# this func order the pok by their value
def list_value() -> list:
    current_list = deepcopy(g.get_graph().pokemons)
    new_list = []
    while (len(current_list) > 0):
        max_value = 0
        pok = -1
        for p in range(len(current_list)):
            if current_list[p].get_value() > max_value:
                max_value = current_list[p].get_value()
                pok = p
        new_list.insert(len(new_list), current_list[pok])
        current_list.pop(pok)

    return new_list

# this func set the start location for every agent
def start_pos(num_of_agent):
    pok_list = list_value()
    new_list = []

    # this loop delete all the pokemons that their dest is src of another pokemons, or location on same edge like pok
    # after this loop we get a list of pokemon sorted by value
    while len(pok_list) > 0:
        src = pok_list[0].get_src()
        dest = pok_list[0].get_dest()
        new_list.insert((len(new_list)), pok_list[0])
        pok_list.pop(0)
        p = 0
        while len(pok_list) > 0:
            # this pokemon location on same edge like pok
            if (pok_list[p].get_src() == src) and (pok_list[p].get_dest() == dest):
                pok_list.pop(p)
            # this pokemon src is the dest of pok
            elif (pok_list[p].get_src() == dest):
                pok_list.pop(p)
            # another pokemons
            else:
                new_list.insert((len(new_list)), pok_list[p])
                pok_list.pop(p)

    for agent in range(num_of_agent):
        """
        # if there were agents left who were not given a starting position, they were given a pos of the center node
        if len(new_list) == 0:
            center_node = g.centerPoint()[0]
            client.add_agent("{\"id\":" + str(center_node) + "}")

        # update the start pos of agent - for all the agent, as long as there are pokemon on the list
        else:
        """
        next = new_list[0].get_src()
        client.add_agent("{\"id\":" + str(next) + "}")
        new_list.pop(0)


# This function will consider after how long it is worthwhile to call the action move,
# so that they will eat the most pokemon in as few move actions as possible
def time_to_sleep() -> float:
    time_sleep = 10

    for agent in g.get_graph().agents.values():
        src_a = agent.get_src()
        dest_a = agent.get_dest()
        pos_a = agent.pos
        speeed_agent = float(agent.get_speed())
        for pok in g.get_graph().pokemons:
            src_p = pok.get_src()
            dest_p = pok.get_dest()
            pos_p = pok.pos
            if src_a == src_p and dest_a == dest_p:
                before = True
                # now we check if this agent realy before this pok - this agent in the way to eat this pok
                # the pos of src node
                x_src = g.get_graph().nodes.get(src_a).pos.get('x')
                y_src = g.get_graph().nodes.get(src_a).pos.get('y')
                # dis between the agent to the src node
                node_agent = distance(x_src, pos_a.get('x'), y_src, pos_a.get('y'))
                # dis between the agent to the pokemons
                agent_pok = distance(pos_a.get('x'), pos_p.get('x'), pos_a.get('y'), pos_p.get('y'))
                # dis between the src node to the pokemons
                pok_node = distance(x_src, pos_p.get('x'), y_src, pos_p.get('y'))
                dis_agent = agent_pok+node_agent
                e = 0.004
                # check if this agent before the pok
                if (pok_node == dis_agent) or (abs(pok_node-dis_agent) <= e):
                    before = True
                else: before = False

                # if this agent before the pok, fint the speed, in order to find the time to sleep
                if before == True:
                    # the len btween the pok and agent = agent_pok
                    # find the speed of this edge
                    speed_edge = float(g.get_graph().node_edge.get(src_a).get(dest_a))
                    current_time = (speed_edge/speeed_agent) /10
                    if current_time < time_sleep:
                        time_sleep = current_time

    # if there isn't exist an agent who its location very close to pokemon
    if time_sleep == 10:
        # find the closest dest node to any agent, and check the time it takes to reach it
        for agent in g.get_graph().agents.values():
            #src_a = agent.get_src()
            #dest_a = agent.get_dest()
            #pos_a = agent.pos
            speeed_agent = float(agent.get_speed())
            # the pos of the dest node
            #x_dest = g.get_graph().nodes.get(dest_a).pos.get('x')
            #y_dest = g.get_graph().nodes.get(dest_a).pos.get('y')
            # dis between the agent to the dest node
            #node_agent = distance(x_dest, pos_a.get('x'), y_dest, pos_a.get('y'))
            # find the speed of this edge
            speed_edge = float(g.get_graph().node_edge.get(src_a).get(dest_a))
            current_time = (speed_edge / speeed_agent)
            if current_time < time_sleep:
                time_sleep = current_time

    #time_sleep = 0.125
    return time_sleep


def distance(x1, x2, y1, y2) -> float:
    dis = (((x1 - x2) ** 2) + ((y1 - y2) ** 2)) ** 0.5
    return dis

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
clock = pygame.time.Clock()

# build a client for connection to the server
client = Client()
client.start_connection(HOST, PORT)

# build a pygame
pygame.init()
screen = pygame.display.set_mode((1100, 700), flags=RESIZABLE)
pygame.font.init()
Font2 = font.SysFont('Calibri', 10, bold=False)

# build a button to stop
stop = Button("stop", (0, 0))

g = GraphAlgo()

# load ll the data to this level:
g.load_graph_data(client.get_graph())
print(g.get_graph().node_edge)
g.load_pokemons(client.get_pokemons())

# to now the number of agent
data_info = json.loads(client.get_info())
num_of_agent = data_info["GameServer"]["agents"]

center_node = g.centerPoint()[0]

# embed each agent the start pos
start_pos(num_of_agent)

g.load_agents(client.get_agents())

# find the proportions of this graph
min_x = 1100
min_y = 700
max_x = 0
max_y = 0
for n in g.graph.nodes.values():
    x = n.pos.get('x')
    y = n.pos.get('y')
    if x > max_x:
        max_x = x
    if x < min_x:
        min_x = x
    if y > max_y:
        max_y = y
    if y < min_y:
        min_y = y

""" 
# find the proportions of this graph
min_x = float(min(list(g.get_graph().nodes.values()), key=lambda n: n.pos.get('x')).pos.get('x'))
min_y = float(min(list(g.get_graph().nodes.values()), key=lambda n: n.pos.get('y')).pos.get('y'))
max_x = float(max(list(g.get_graph().nodes.values()), key=lambda n: n.pos.get('x')).pos.get('x'))
max_y = float(max(list(g.get_graph().nodes.values()), key=lambda n: n.pos.get('y')).pos.get('y'))
"""

radius = 7

# this commnad starts the server - the game is running now
client.start()

num_pok = 0
grade = 0

# creat timer
time_to_end = int(int(client.time_to_end())/1000)
pygame.time.set_timer(pygame.USEREVENT, 1000)
text = str(time_to_end)

while client.is_running() == 'true':

    g.load_pokemons(client.get_pokemons())
    g.load_agents(client.get_agents())

    # check events
    for event in pygame.event.get():
        if event.type == QUIT:
            client.stop_connection()
            quit()
            exit(0)

        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            clicked, _, _ = pygame.mouse.get_pressed()

            # If you select the stop
            if stop.rect.collidepoint(mouse_pos):
                t = client.stop()

        # update the timer
        if event.type == pygame.USEREVENT:
            time_to_end -= 1
            if time_to_end > 0:
                text = str(time_to_end)
            else: text = 'end!'

    # refresh surface
    screen.fill(Color(250, 250, 250))

    # draw edges
    for s in g.graph.node_edge.keys():

        # find the edge src
        src = g.graph.nodes.get(s)
        src_x = my_scale(src.pos.get('x'), x=True)
        src_y = my_scale(src.pos.get('y'), y=True)

        for d in g.graph.node_edge.get(s):

            # find the edge dest
            dest = g.graph.nodes.get(d)
            dest_x = my_scale(dest.pos.get('x'), x=True)
            dest_y = my_scale(dest.pos.get('y'), y=True)

            # draw the line
            pygame.draw.line(screen, Color(61, 72, 126), (src_x, src_y), (dest_x, dest_y), width=1)

            # draw the arrow
            if dest_x == src_x:
                if dest_y < src_y:
                    pygame.draw.polygon(screen, Color(61, 72, 126), [(dest_x, dest_y+7), (dest_x+5, dest_y+17), (dest_x-5, dest_y+17)])
                else:
                    pygame.draw.polygon(screen, Color(61, 72, 126), [(dest_x, dest_y - 7), (dest_x + 5, dest_y - 17),(dest_x - 5, dest_y - 17)])

            elif dest_y == src_y:
                if dest_x < src_x:
                    pygame.draw.polygon(screen, Color(61, 72, 126), [(dest_x+7, dest_y), (dest_x +17, dest_y+5),(dest_x+17, dest_y-5)])
                else:
                    pygame.draw.polygon(screen, Color(61, 72, 126), [(dest_x-7, dest_y), (dest_x -17, dest_y+5),(dest_x-17, dest_y-5)])

            else:
                x1, x2, m, n = x2point(src_x, src_y, dest_x, dest_y, radius)
                if dest_x > src_x:
                    xs = min(x1, x2)
                else: xs = max(x1, x2)
                ys = m * xs + n
                x1, x2, m, n = x2point(src_x, src_y, xs, ys, 10)
                if dest_x > src_x:
                    x = min(x1, x2)
                else: x = max(x1, x2)
                y = m * x + n
                x3, x4, m, n = x1point(x, y, 5, m)
                y3 = m * x3 + n
                y4 = m * x4 + n
                pygame.draw.polygon(screen, Color(61, 72, 126), [(xs,ys), (x3,y3), (x4,y4)])


    # draw nodes
    for n in g.graph.nodes.values():

        # find node location
        x = my_scale(n.pos.get('x'), x=True)
        y = my_scale(n.pos.get('y'), y=True)

        # draw the nodes
        pygame.draw.circle(screen, Color(230, 219, 230), (int(x), int(y)), radius=radius)
        gfxdraw.aacircle(screen, int(x), int(y), radius, Color(85, 0, 85))

        # draw the node id
        id_srf = Font2.render(str(n.get_id()), True, Color(85, 0, 85))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw pokemons
    for p in g.graph.pokemons:
        # find pokemons location
        r = 10
        x = my_scale(p.pos.get('x'), x=True)
        y = my_scale(p.pos.get('y'), y=True)
        if p.type == -1:
            pos = [[x, y + r], [x - r, y - r], [x + r, y - r]]
            pygame.draw.polygon(screen, Color(53, 232, 211), pos)
        elif p.type == 1:
            pos = [[x, y - r], [x - r, y + r], [x + r, y + r]]
            pygame.draw.polygon(screen, Color(232, 165, 32), pos)
        # draw the pokemon
        #gfxdraw.aacircle(screen, int(x), int(y), radius, Color(85, 0, 85))


    # draw agents
    for a in g.graph.agents.values():
        # find agent location
        x = my_scale(a.pos.get('x'), x=True)
        y = my_scale(a.pos.get('y'), y=True)

        # draw the agent
        pygame.draw.circle(screen, Color(128, 64, 64), (int(x), int(y)), radius=radius)
        #gfxdraw.aacircle(screen, int(x), int(y), radius, Color(85, 0, 85))

        # draw the agent id
        #id_srf = Font2.render(str(a.get_id()), True, Color(250, 250, 250))
        #rect = id_srf.get_rect(center=(x, y))
        #screen.blit(id_srf, rect)



    #screen.fill((255, 255, 255))
    # draw button
    stop.draw(screen)

    # draw number of pokemon eaten
    title_srf = Font.render(str(num_pok), True, Color(43, 43, 43))
    title_rect = title_srf.get_rect(center=Rect((0, 20), (70, 20)).center)
    screen.blit(title_srf, title_rect)

    # draw the grade
    title_srf = Font.render(str(grade), True, Color(43, 43, 43))
    title_rect = title_srf.get_rect(center=Rect((0, 40), (70, 20)).center)
    screen.blit(title_srf, title_rect)

    # draw timer
    title_srf = Font.render(text, True, Color(43, 43, 43))
    title_rect = title_srf.get_rect(center=Rect((0, 60), (70, 20)).center)
    screen.blit(title_srf, title_rect)

    pygame.display.flip()

    # choose next edge
    next_node()

    # update the number of pokemons eaten, and the current grade
    data_info = json.loads(client.get_info())
    now_grade = float(data_info["GameServer"]["grade"])
    if grade != now_grade:
        grade = now_grade
        num_pok += 1

    g.load_agents(client.get_agents())
    time_sleep = time_to_sleep()
    time.sleep(time_sleep)
    client.move()
    print(client.get_info())



