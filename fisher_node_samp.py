#! /usr/bin/env python

import random
import sys

class packet_node: #class for the packets

    def __init__(self, device):
        self.start = device
        self.node = 'V'
        
    def add_node(self, n): 
        self.node = n

def node_sample_mark(p):
    """Marking procedure at router R :
    for each packet w
    let x be a random number from [0..1)
    if x < p then,
    write R into w .node"""
    x = random.random() #setting x to a random integer in [0 .. 1)

    if x < p: 
        return True
    else:
        return False

def node_sample_recon(x, NdTbl):

    # Algorithm for reconstructing path for node sampling

    """Path reconstruction procedure at victim v :
    let NodeTbl be a table of tuples (node,count)
    for each packet w from attacker
    z := lookup w .node in NodeTbl
    if z != NIL then
    increment z .count
    else
    insert tuple ( w .node,1) in NodeTbl
    sort NodeTbl by count
    extract path ( R i .. R j ) from ordered node fields in NodeTbl"""
    
    z = False #initializing z to false
    i = 0 #used to keep track of index for count
    #print(x)
    for tpl in NdTbl:
        #print("Here")
        if tpl[0] == x:
            z = True
            break
        else:
            z = False
        i += 1

    if z == True:             #executes if node is found in NodeTbl
        NdTbl[i][1] += 1
    else:                     #executes if node is not found in NodeTbl  
        NdTbl.append([w.node,1])

devices = ['A3','A4']
#attacker = devices[random.randint(0,len(devices)-1)] # Setting attacker to device
attacker = 'A1'

path_nodes = [('A1', 'R001', 'R005', 'R009', 'R012', 'R015', 'R017', 'R019', 'R020'),
              ('A1', 'R002', 'R006', 'R010', 'R013', 'R015', 'R017', 'R019', 'R020'),
              ('A2', 'R003', 'R007', 'R010', 'R014', 'R016', 'R018', 'R019', 'R020'),
              ('A3', 'R004', 'R008', 'R011', 'R014', 'R016', 'R018', 'R019', 'R020')]

x_times_packet = 100
total_packets = 0
p = 0.2
NodeTbl = [[attacker[0],1]]

print("Non-Attackers are using devices: %s" %devices)
print("Attacker is a device: %s" % attacker)
print("_"*40)
for edge in path_nodes: #marking the packets
    print(edge)
    for i in range(0,10):
        if edge[0] == attacker[0]:
            w = packet_node(attacker)
            for i in range(0, x_times_packet):
                total_packets += 1
                for node in edge[1:]:
                    if node_sample_mark(p) == True:
                        w.add_node(node)
                node_sample_recon(w.node, NodeTbl)
        else:
            w = packet_node(edge[0])
            total_packets += 1
            for node in edge[1:]:
                if node_sample_mark(p) == True:
                    w.add_node(node)
            node_sample_recon(w.node, NodeTbl)

NodeTbl.sort()
if NodeTbl[-1][0] == 'V':
    NodeTbl.pop()
print(NodeTbl)
print("Packets sent: %d" % total_packets)
