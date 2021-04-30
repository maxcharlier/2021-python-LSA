import csv
from typing import Dict, List, Tuple
from math import ceil
from nodes.anchor import Anchor
from nodes.tag import Tag
from nodes.point import Point
from graphics import plot_network, plot_network_routing, dot_network_routing

class Topology():
  def __init__(self, x, y, space, comm_range, disruption_range, R, nb_tag_loc):
    """
    Topology class
    :param x the witdh of the grid in meters
    :param y the height of the grid in meters
    :param space the distance in meter between anchors
    :param com_range the  communication range of anchors
    :param disruption_range the disruption range of communication of anchors
    :param R the number of tag per cell
    :param nb_tag_loc the number of localisation per tag per slotframe
    """
    self.x = x
    self.y = y
    self.space = space
    self.comm_range = comm_range
    self.disruption_range = disruption_range
    self.R = R
    self.nb_tag_loc = nb_tag_loc
    self.nodes = [] #start with no node
    self.sinks = [] #start with no sink
    if(comm_range > disruption_range):
      raise Exception("Communication range need to be shorter that disruption range.")

  def generate_nodes(self):
    """Generate the grid based on the space between nodes, also generate tags node based on 3 closes anchors :
    one lower left, lower right, and upper left
    Return a list of anchors and tags
    """
    nodes_x = ceil(self.x/self.space)
    nodes_y = ceil(self.y/self.space)
    anchors =[]
    tags = []
    anchors_all = []
    for i in range(nodes_x):
      anchors.append([])
      for j in range(nodes_y):
        name = "a_" + str(i) + "_" + str(j)
        pos = Point(i*self.space, j*self.space)
        node = Anchor(name, pos, self.comm_range, self.disruption_range)
        anchors[-1].append(node)
        #add tags in cell
        if(i >=1 and j>= 1 and i < nodes_x and j < nodes_y):
          for n in range(self.R):
            name = "t_"+str(i)+"_"+str(j)+"_"+str(n)
            pos = Point((i-0.5)*self.space, (j-0.5)*self.space)
            tag = Tag(name, pos, self.comm_range, self.disruption_range)
            tag.add_parent(anchors[i-1][j-1], self.nb_tag_loc)
            tag.add_parent(anchors[i-1][j], self.nb_tag_loc)
            tag.add_parent(anchors[i][j-1], self.nb_tag_loc)
            tags.append(tag)
      anchors_all += anchors[-1]

    return (anchors_all, tags)

  def generate_neighbourhood(self, anchors, tags):
    """Generate for all nodes, the neighbourg (nodes in the communication range) and the connectivity (node in the disruption range)
    """
    for i in range(len(anchors)):
      for j in range(i):
        if anchors[i].is_recheable(anchors[j], self.comm_range):
          anchors[i].add_comm_node(anchors[j])
          #do other side because connectivity is be derectionnal
          anchors[i].add_disrupted_node(anchors[j])
          anchors[j].add_comm_node(anchors[i])
          anchors[j].add_disrupted_node(anchors[i])
        elif anchors[i].is_recheable(anchors[j], self.disruption_range):
          anchors[i].add_disrupted_node(anchors[j])
          #do other side because connectivity is be derectionnal
          anchors[j].add_disrupted_node(anchors[i])
    #connectivity of tags
    for tag in tags:
      tag.gen_comm_parents()
      tag.gen_disrupted_nodes()

    return (anchors, tags)

  def export_nodes(self, file):
    with open(file, 'w') as csvfile:
      fieldnames = ['name', 'position', 'comm_range', 'disruption_range', 'type', 'sink']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

      writer.writeheader()
      for node in self.nodes:
        if node.type == 'anchor' and node.sink == True:
          sink = True
        else:
          sink = False
        writer.writerow({'name': node.name, 'position': str(node.position), 'comm_range': str(node.comm_range), 'disruption_range': str(node.disruption_range), 'type': str(node.type), 'sink': str(sink)})

  def import_nodes(self, file):
    with open(file) as csvfile:
      reader = csv.DictReader(csvfile)
      self.nodes=[]
      for row in reader:
        position = Point.from_str(row['position'])

        if(row['type'] == 'anchor'):
          if(row['sink'] == 'True'):
            sink = True
          else:
            sink = False
          self.nodes.append(Anchor(row['name'], position, float(row['comm_range']), float(row['disruption_range']), sink))
          if sink:
            self.set_sink(self.nodes[-1])
        else:#tag
          self.nodes.append(Tag(row['name'], position, float(row['comm_range']), float(row['disruption_range'])))

  def set_sink(self, node):
    self.sinks.append(node)
          
  def set_nodes(self, anchors, tags):
    self.nodes = anchors + tags

  def generate_routing(self):
    """Can be call after having generate nodes and neighbourhood """
    if len(self.sinks) == 0:
      raise Exception("They are no sink to perform a routing")
    #first set nodes as sinks
    for sink in self.sinks:
      sink.set_as_sink(True)
    #then propagate the rank of each sink
    for sink in self.sinks:
      sink.broadcast_rank()
    for sink in self.sinks:
      sink.initialise_and_get_w()

  def export_connectivity(self, file):
    with open(file, 'w') as csvfile:
      fieldnames = ['source', 'destination']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      for source in self.nodes:
        for dest in source.disrupted_nodes:
          writer.writerow({'source': source.name, 'destination': dest.name})

  def import_connectivity(self, file):
    with open(file) as csvfile:
      reader = csv.DictReader(csvfile)
      nodes_name = []
      for node in self.nodes:
        nodes_name.append(node.name)
      for row in reader:
        self.nodes[nodes_name.index(row['source'])].add_disrupted_node(nodes_name.index(row['destination']))


  def export_routing(self, file):
    with open(file, 'w') as csvfile:
      fieldnames = ['source', 'destination', 'weight']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      for node in self.nodes:
        if node.type == 'anchor' and not node.sink :
          writer.writerow({'source': node.name, 'destination': node.parent.name, 'weight': node.parent_w})
        elif node.type == 'tag':
          for i in range(len(node.parents)):
            writer.writerow({'source': node.name, 'destination': node.parents[i].name, 'weight': node.parents_w[i]})


  def import_routing(self, file):
    with open(file) as csvfile:
      reader = csv.DictReader(csvfile)
      nodes_name = []
      for node in self.nodes:
        nodes_name.append(node.name)
      for row in reader:
        self.nodes[nodes_name.index(row['source'])].add_parent(self.nodes[nodes_name.index(row['destination'])], int(row['weight']))


if __name__ == '__main__':
  topology = Topology(50, 50, 10, 15, 25, 1, 1)
  (anchors, tags) = topology.generate_nodes()
  topology.generate_neighbourhood(anchors, tags)
  topology.set_sink(anchors[5])
  topology.set_sink(anchors[15])
  topology.set_nodes(anchors, tags)
  topology.generate_routing()
  plot_network(topology.nodes, "./topology.pdf")
  plot_network_routing(topology.nodes, "./plot_network_routing.pdf")
  dot_network_routing(topology.nodes, "./dot_network_routing.dot")

