import csv
from typing import Dict, List, Tuple
import math
from nodes.anchor import Anchor
from nodes.tag import Tag
from nodes.point import Point
import graphics
import scheduling

class Topology():
  def __init__(self, x, y, space, comm_range, disruption_range, R, nb_tag_loc):
    """
    Topology class
    :param x the witdh of the grid in meters
    :param y the height of the grid in meters
    :param space the distance in meter between anchors
    :param com_range the communication range of anchors
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
    self.nb_anchors = 0
    self.nb_tags = 0

  def generate_nodes(self):
    """Generate the grid based on the space between nodes, also generate tags node based on 3 closes anchors :
    one lower left, lower right, and upper left
    Return a list of anchors and tags
    """
    nodes_x = math.ceil(self.x/self.space)
    nodes_y = math.ceil(self.y/self.space)
    anchors =[]
    tags = []
    anchors_all = []
    for i in range(nodes_x+1):
      print()
      anchors.append([])
      for j in range(nodes_y+1):
        name = "a-" + str(i) + "-" + str(j)
        pos = Point(i*self.space, j*self.space)
        node = Anchor(name, pos, self.comm_range, self.disruption_range)
        anchors[-1].append(node)
        #add tags in cell
        if(i >=1 and j>= 1 and i <= nodes_x and j <= nodes_y):
          for n in range(self.R):
            name = "t-"+str(i)+"-"+str(j)+"-"+str(n)
            pos = Point((i-0.5)*self.space, (j-0.5)*self.space)
            tag = Tag(name, pos, self.comm_range, self.disruption_range)
            tag.add_parent(anchors[i-1][j-1], self.nb_tag_loc)
            tag.add_parent(anchors[i-1][j], self.nb_tag_loc)
            tag.add_parent(anchors[i][j-1], self.nb_tag_loc)
            tags.append(tag)
      anchors_all += anchors[-1]

    return (anchors_all, tags)
  def filter_tags(tags, ref_filtering_node, dist):
    """Return tags that are less than dist meters of the ref_filtering_node"""
    select_tags = []
    for tag in tags:
      selected = False
      if ref_filtering_node.distance(tag) < dist :
        select_tags.append(tag)
      else:
        tag.remove()
    return select_tags

  def anchors_node_search(self, node_ref, list_nodes):
    """search all nodes cimetrical to node_ref 
    exampe : grid 10*10
    node ref (2,2) return node (8,2);(2,8);(8,8)"""
    selected_nodes = [node_ref]
    for node in list_nodes:
      if node != node_ref:
        if node.position.x == node_ref.position.x and node.position.y == self.y - node_ref.position.y:
          selected_nodes.append(node)
        elif node.position.x == self.x - node_ref.position.x and node.position.y == node_ref.position.y:
          selected_nodes.append(node)
        elif node.position.x == self.x - node_ref.position.x and node.position.y == self.y - node_ref.position.y:
          selected_nodes.append(node)
    return selected_nodes

  def node_search(self, position, list_nodes):
    """search all nodes cimetrical to node_ref 
    exampe : position (2,2) return node in (2,2)"""
    for node in list_nodes:
      if node.position.x == position.x and node.position.y == position.y:
        return node

  def generate_neighbourhood(self, anchors, tags):
    """Generate for all nodes, the neighbourg (nodes in the communication range) and the connectivity (node in the disruption range)
    """
    print("generate_neighbourhood anchors")

    for i in range(len(anchors)):
      for j in range(i):
        if anchors[i].is_recheable(anchors[j], self.comm_range):
          anchors[i].add_comm_node(anchors[j])
          #do other side because connectivity is bi-directionnal
          anchors[i].add_disrupted_node(anchors[j])
          anchors[j].add_comm_node(anchors[i])
          anchors[j].add_disrupted_node(anchors[i])
        elif anchors[i].is_recheable(anchors[j], self.disruption_range):
          anchors[i].add_disrupted_node(anchors[j])
          #do other side because connectivity is bi-directionnal
          anchors[j].add_disrupted_node(anchors[i])
    print("generate_neighbourhood tags")
    #connectivity of tags
    for tag in tags:
      tag.gen_comm_parents()
      tag.gen_disrupted_nodes()

    return (anchors, tags)

  def export_nodes(self, file):
    """Recommanded file name is "nodes.csv" """
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
    """Recommanded file name is "nodes.csv" """
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
          self.nodes.append(Anchor(row['name'], position, float(row['comm_range']), float(row['disruption_range'])))
          if sink:
            self.set_sink(self.nodes[-1])
            self.nodes[-1].set_as_sink(True)
        else:#tag
          self.nodes.append(Tag(row['name'], position, float(row['comm_range']), float(row['disruption_range'])))  



  def export_param(self, file):
    """Recommanded file name is "topology_param.csv" """
    with open(file, 'w') as csvfile:
      fieldnames = ['x', 'y', 'space', 'comm_range', 'disruption_range', 'R', 'nb_tag_loc']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

      writer.writeheader()
      writer.writerow({'x': str(self.x), 'y': str(self.y), 'space': str(self.space), 'comm_range': str(self.comm_range), 'disruption_range': str(self.disruption_range), 'R': str(self.R), 'nb_tag_loc': str(self.nb_tag_loc)})

  def import_param(file):
    """Recommanded file name is "topology_param.csv" """
    with open(file) as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        return Topology(float(row['x']), float(row['y']), float(row['space']), float(row['comm_range']), float(row['disruption_range']), int(row['R']), int(row['nb_tag_loc']))

  def set_sink(self, node):
    self.sinks.append(node)
          
  def set_nodes(self, anchors, tags):
    self.nodes = anchors + tags
    self.nb_anchors = len(anchors)
    self.nb_tags = len(tags)

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
      sink.initialise_Q()
    for node in self.nodes:
      #check if we have a path to the sink for all anchors
      if node.type == 'anchor' and not node.sink and node.parent == None:
        return False
    return True


  def export_connectivity(self, file):
    """Recommanded file name is "connectivity.csv" """
    with open(file, 'w') as csvfile:
      fieldnames = ['source', 'destination']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      for source in self.nodes:
        for dest in source.disrupted_nodes:
          writer.writerow({'source': source.name, 'destination': dest.name})

  def import_connectivity(self, file):
    """Recommanded file name is "connectivity.csv" """
    with open(file) as csvfile:
      reader = csv.DictReader(csvfile)
      nodes_name = []
      for node in self.nodes:
        nodes_name.append(node.name)
      for row in reader:
        self.nodes[nodes_name.index(row['source'])].add_disrupted_node(self.nodes[nodes_name.index(row['destination'])])
        # print("{} -> {}".format(row['source'], row['destination']))

  def export_routing(self, file):
    """Recommanded file name is "routing.csv" """
    with open(file, 'w') as csvfile:
      fieldnames = ['source', 'destination', 'weight']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      for node in self.nodes:
        if node.type == 'anchor' and not node.sink and node.parent != None:
          writer.writerow({'source': node.name, 'destination': node.parent.name, 'weight': node.current_weight})
        elif node.type == 'tag':
          for i in range(len(node.parents)):
            writer.writerow({'source': node.name, 'destination': node.parents[i].name, 'weight': node.parents_w[i]})


  def import_routing(self, file):
    """Recommanded file name is "routing.csv" """
    with open(file) as csvfile:
      reader = csv.DictReader(csvfile)
      nodes_name = []
      for node in self.nodes:
        nodes_name.append(node.name)
      for row in reader:
        index_source= nodes_name.index(row['source'])
        if self.nodes[index_source].type == 'tag' :
          self.nodes[index_source].add_parent(self.nodes[nodes_name.index(row['destination'])], int(row['weight']))
        else:
          self.nodes[index_source].set_routing_parent(self.nodes[nodes_name.index(row['destination'])], int(row['weight']))
      for sink in self.sinks:
        sink.initialise_Q()

  def print_sinks_Q(self):
    for sink in self.sinks:
      print("sink (" + str(sink.position.x) + ", " + str(sink.position.y) + ") Q : " +str(sink.Q))


if __name__ == '__main__':
  topology = Topology(50, 50, 10, 15, 25, 1, 1)
  (anchors, tags) = topology.generate_nodes()
  topology.generate_neighbourhood(anchors, tags)
  topology.set_sink(anchors[5])
  topology.set_sink(anchors[-1])
  # topology.set_sink(anchors[int(len(anchors)/2)])
  topology.set_nodes(anchors, tags)
  topology.generate_routing()
  graphics.plot_C(topology.nodes, "./example/graph-C.pdf")
  graphics.plot_neighbours(topology.nodes, "./example/plot_neighbours.pdf")
  graphics.plot_Q(topology.nodes, "./example/plot_Q.pdf")
  graphics.dot_network_routing(topology.nodes, "./example/dot_network_routing.dot")
  topology.export_connectivity("./example/export_connectivity.csv")
  topology.export_routing("./example/export_routing.csv")
  topology.export_nodes("./example/export_nodes.csv")
  (schedule, duration) = scheduling.scheduling(topology, n_ch=6, agregation=5)
  print("duration : " + str(duration))
  # scheduling.print_schedule(schedule)
  print("len schedule " + str(len(schedule)))
  scheduling.export_schedule(schedule, "./example/schedule.csv")