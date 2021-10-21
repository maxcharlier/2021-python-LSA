from math import ceil
from nodes.anchor import Anchor
from nodes.tag import Tag
from nodes.point import Point
import graphics
import scheduling
import topology
import os #creation of directory
import random
import csv
import math

"""This file is used to generate a bunch of topology , export them an then generate figure with a loader"""
SINK_BEST ="best"
SINK_WORST = "worst"
SINK_RANDOM = "random"
SINK_ALL = "all"


class Bunch_Parameters():
  def __init__(self, x, y, space, comm_range, disruption_range, R, nb_tag_loc, sink_allocation, nb_sink, nb_ch, agregation, directory):
    """
    A bunch a paramater, we recommend to only vary one parameter per bunch
    :param x witdhs of grids in meters
    :param y heights of grids in meters
    :param space distances in meter between anchors
    :param comm_range communication range in meter between anchors
    :param disruption_range the disruption range of communication in meter between anchors
    :param R number of tags per cell
    :param nb_tag_loc number of localisations per tag per slotframe
    :param sink_allocation Define the pattern of allocation of anchors (best, worst or random)
    :param nb_sink Define the number of sink
    :param nb_ch Define the number of channels
    :param agregation Define the aggregation capacity of anchors 
    :param directory Define the directory where file will be saved.
    """
    self.x = x
    self.y = y
    self.space = space
    self.comm_range = comm_range
    self.disruption_range = disruption_range
    self.R = R
    self.nb_tag_loc = nb_tag_loc
    self.sink_allocation = sink_allocation
    self.nb_sink = nb_sink
    self.nb_ch = nb_ch
    self.agregation = agregation
    if directory[-1] != '/':
      directory = directory + '/'
    self.directory = directory
    self.dist_sink = 0
    self.name = None
    self.seed = 0

  def set_dist_sink(self, dist_sink):
    self.dist_sink = dist_sink

  def set_name(self, name):
    self.name = name

  def set_seed(self, seed):
    """Define the seed generator for a randomized uniform distribution of tag in the network"""
    self.seed = seed

  def export_toplogy_param(parameters, file="toplogy_param.csv"):
    """Recommanded file name is "toplogy_param.csv" """

    file = parameters[0].directory + file
    with open(file, 'w') as csvfile:
      fieldnames = ['x', 'y', 'space', 'comm_range', 'disruption_range', 'R', 'nb_tag_loc', 'sink_allocation', 'nb_sink', 'nb_ch', 'agregation', 'directory']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      for parameter in parameters:
        writer.writerow({'x': str(parameter.x), 'y': str(parameter.y), 'space': str(parameter.space), 'comm_range': str(parameter.comm_range), 'disruption_range': str(parameter.disruption_range), 'R': str(R), 'nb_tag_loc': str(parameter.nb_tag_loc), 'sink_allocation': str(parameter.sink_allocation), 'nb_sink': str(parameter.nb_sink), 'nb_ch': str(parameter.nb_ch), 'agregation': str(parameter.agregation), 'directory': str(parameter.directory)})

  def get_parameters_from_file(file):
    """Recommanded file name is "toplogy_param.csv" """
    parameters = []
    with open(file) as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        parameters.append(Bunch_Parameters(float(row['x']), float(row['y']), float(row['space']), float(row['comm_range']), float(row['disruption_range']), int(row['R']), int(row['nb_tag_loc']), str(row['sink_allocation']), int(row['nb_sink']), int(row['nb_ch']),  int(row['agregation']), str(row['directory'])))
        if "dist_sink" in row.keys():
          parameters[-1].set_dist_sink(float(row['dist_sink']))
        if "name" in row.keys():
          parameters[-1].set_name(str(row['name']))
        if "seed" in row.keys():
          parameters[-1].set_seed(int(row['seed']))
    return parameters
  
  def get_str_variable_1_parameter(parameters):
    """Return the name of the variable parameter"""
    if len(parameters) > 1 and parameters[0].x != parameters[1].x:
      return "x"
    elif len(parameters) > 1 and parameters[0].y != parameters[1].y:
      return "y"
    elif len(parameters) > 1 and parameters[0].space != parameters[1].space:
      return "space"
    elif len(parameters) > 1 and parameters[0].comm_range != parameters[1].comm_range:
      return "Communication Range"
    elif len(parameters) > 1 and parameters[0].disruption_range != parameters[1].disruption_range:
      return "Disruption Range"
    elif len(parameters) > 1 and parameters[0].R != parameters[1].R:
      return "R"
    elif len(parameters) > 1 and parameters[0].nb_tag_loc != parameters[1].nb_tag_loc:
      return "Number of tag loc"
    elif len(parameters) > 1 and parameters[0].sink_allocation != parameters[1].sink_allocation:
      return "Sink Allocation"
    elif len(parameters) > 1 and parameters[0].nb_sink != parameters[1].nb_sink:
      return "Number of sink"
    elif len(parameters) > 1 and parameters[0].nb_ch != parameters[1].nb_ch:
      return "Number of channels"
    elif len(parameters) > 1 and parameters[0].agregation != parameters[1].agregation:
      return "Agregation"
    return "Unknown paramter"  

  def get_variable_1_parameter(parameters):
    """Return the name of the variable parameter"""
    if len(parameters) > 1 and parameters[0].x != parameters[1].x:
      return [param.x for param in parameters]
    elif len(parameters) > 1 and parameters[0].y != parameters[1].y:
      return [param.y for param in parameters]
    elif len(parameters) > 1 and parameters[0].space != parameters[1].space:
      return [param.space for param in parameters]
    elif len(parameters) > 1 and parameters[0].comm_range != parameters[1].comm_range:
      return [param.comm_range for param in parameters]
    elif len(parameters) > 1 and parameters[0].disruption_range != parameters[1].disruption_range:
      return [param.disruption_range for param in parameters]
    elif len(parameters) > 1 and parameters[0].R != parameters[1].R:
      return [param.R for param in parameters]
    elif len(parameters) > 1 and parameters[0].nb_tag_loc != parameters[1].nb_tag_loc:
      return [param.nb_tag_loc for param in parameters]
    elif len(parameters) > 1 and parameters[0].sink_allocation != parameters[1].sink_allocation:
      return [param.sink_allocation for param in parameters]
    elif len(parameters) > 1 and parameters[0].nb_sink != parameters[1].nb_sink:
      return [param.nb_sink for param in parameters]
    elif len(parameters) > 1 and parameters[0].nb_ch != parameters[1].nb_ch:
      return [param.nb_ch for param in parameters]
    elif len(parameters) > 1 and parameters[0].agregation != parameters[1].agregation:
      return [param.agregation for param in parameters]
    return None

        


def gen_topology(parameters, plot_graph=True):    
  """
  Generate a bunch of topology
  :param param a Bunch_Parameters object
  """
  i = 0
  for param in parameters:
    print(str(param.x), str(param.y), str(param.space), str(param.comm_range), str(param.disruption_range), str(param.R), str(param.nb_tag_loc), str(param.sink_allocation), str(param.nb_sink), str(param.nb_ch), str(param.agregation), str(param.directory))

    topology_ = topology.Topology(param.x, param.y, param.space, param.comm_range, param.disruption_range, param.R, param.nb_tag_loc)
    
    (anchors, tags) = topology_.generate_nodes(param.seed)

    #ref_filtering_node define the node used has reference point to filter tags with distance
    #by default it is in the center, but it's place change when using "Worst" position of sink
    ref_filtering_node = anchors[math.floor(len(anchors)/2)]
    if param.sink_allocation == SINK_BEST:
      if param.nb_sink == 1:
        # add sink to the center
        node = anchors[math.floor(len(anchors)/2)]
        topology_.set_sink(node)
        node.set_as_sink(True)
      if param.nb_sink == 2:
        selected_nodes = []
        selected_nodes.append(topology_.node_search(Point(math.floor(param.x/4)*param.space, math.floor(param.y/4)*param.space), anchors))
        selected_nodes.append(topology_.node_search(Point(math.floor(param.x/4)*param.space*3, math.floor(param.y/4)*param.space*3), anchors))
        for node in selected_nodes:
          topology_.set_sink(node)
          node.set_as_sink(True)
      if param.nb_sink == 3:
        sinks = []
        sinks.append(topology_.node_search(Point(math.floor(param.x/2)*param.space, math.floor(param.y/4)*param.space), anchors))
        sinks.append(topology_.node_search(Point(math.floor(param.x/4)*param.space, math.floor(param.y/3)*param.space*2), anchors))
        sinks.append(topology_.node_search(Point((math.floor(param.x/4)*param.space)*3, math.floor(param.y/3)*param.space*2), anchors))
        for sink in sinks:
          topology_.set_sink(sink)
          sink.set_as_sink(True)
        # for i in range(1, 3):
        #   node = anchors[math.floor((len(anchors)/3)*i)]
        #   topology_.set_sink(node)
        #   node.set_as_sink(True)
      if param.nb_sink == 4:
        node = anchors[math.floor(len(anchors)/5)]
        selected_nodes = topology_.anchors_node_search(node, anchors)
        for node in selected_nodes:
          topology_.set_sink(node)
          node.set_as_sink(True)
      if param.nb_sink == 5:
        node = anchors[math.floor(len(anchors)/5)]
        selected_nodes = topology_.anchors_node_search(node, anchors)
        selected_nodes.append(anchors[math.floor(len(anchors)/2)])
        topology_.set_sink(node)
        node.set_as_sink(True)
        for node in selected_nodes:
          topology_.set_sink(node)
          node.set_as_sink(True)
      if param.nb_sink == 9:
        node = topology_.node_search(Point(math.floor(param.x/6)*param.space, math.floor(param.y/6)*param.space), anchors)
        selected_nodes = topology_.anchors_node_search(node, anchors)
        #node in the center
        selected_nodes.append(anchors[math.floor(len(anchors)/2)])

        node = topology_.node_search(Point(math.floor(param.x/2)*param.space, math.floor(param.y/6)*param.space), anchors)
        selected_nodes += topology_.anchors_node_search(node, anchors)
        node = topology_.node_search(Point(math.floor(param.x/6)*param.space, math.floor(param.y/2)*param.space), anchors)
        selected_nodes += topology_.anchors_node_search(node, anchors)

        for node in selected_nodes:
          topology_.set_sink(node)
          node.set_as_sink(True)
      if param.nb_sink == 18:

        for i in range(0, 3):
          for j in range(0,3):
            x = round((param.x/13)*(param.space*(i*4)+1))
            y = round((param.y/13)*(param.space*(j*4)+3))
            # print("i " + str(i) + "j " + str(j) + "x " + str(x) + "y " + str(y))
            node = topology_.node_search(Point(x, y), anchors)
            topology_.set_sink(node)
            node.set_as_sink(True)
            x = round((param.x/13)*(param.space*(i*4)+3))
            y = round((param.y/13)*(param.space*(j*4)+1))
            # print("i " + str(i) + "j " + str(j) + "x " + str(x) + "y " + str(y))
            node = topology_.node_search(Point(x, y), anchors)
            topology_.set_sink(node)
            node.set_as_sink(True)
    elif param.sink_allocation == SINK_WORST:
      ref_filtering_node = anchors[0]
      topology_.set_sink(anchors[0])
      anchors[0].set_as_sink(True)
    elif param.sink_allocation == SINK_RANDOM:
      random_anchor = anchors[random.randint(0, len(anchors))]
      topology_.set_sink(random_anchor)
      random_anchor.set_as_sink(True)
    elif param.sink_allocation == SINK_ALL:
      for node in anchors:
        topology_.set_sink(node)
        node.set_as_sink(True)
    else:
      raise Exception("Sink position parameter have an unsupported value " + str(param.sink_allocation))

    current_directory = param.directory

    if param.dist_sink > 0:
      print("filter tags " + str(param.dist_sink))
      tags = topology.Topology.filter_tags(tags, ref_filtering_node, param.dist_sink)
      # print(tags)


    print("Current directory" + str(current_directory))

    topology_.generate_neighbourhood(anchors, tags)

    try:
        os.makedirs(current_directory)
    except OSError:
        print ("Creation of the directory %s failed" % current_directory)
    else:
        print ("Successfully created the directory %s" % current_directory)

    topology_.set_nodes(anchors, tags)
    if plot_graph:
      graphics.plot_neighbours(topology_.nodes, current_directory + "plot_neighbours.pdf")
    
    if(topology_.generate_routing()):
      print("Routing generated")
      # topology_.print_sinks_Q()
      graphics.plot_sinks_Q(topology_.sinks, current_directory + "plot_sinks_Q.pdf")
      if plot_graph: 
        graphics.plot_C(topology_.nodes, current_directory + "graph-C.pdf")
        graphics.plot_network_routing(topology_.nodes, current_directory + "plot_network_routing.pdf")
        graphics.plot_Q(topology_.nodes, current_directory + "plot_Q.pdf")
        graphics.dot_network_routing(topology_.nodes, current_directory + "dot_network_routing.dot")

      (schedule, duration) = scheduling.scheduling(topology_, n_ch=param.nb_ch, agregation=param.agregation)

      topology_.export_param(current_directory + "topology_param.csv")
      topology_.export_nodes(current_directory + "nodes.csv")
      topology_.export_connectivity(current_directory + "connectivity.csv")
      topology_.export_routing(current_directory + "routing.csv")
      scheduling.export_schedule(schedule, current_directory + "schedule.csv")
      scheduling.export_schedule_stat(duration, schedule, topology_, current_directory + "schedule_stat.csv")
      print("Topology " + current_directory + " duration " + str(duration))
    else:
      print("No all anchors have a path to the sinks.")
    

def update_stat_topology(param):    
  """
  Update the schedule stat of a bunch
  """  
  i = 0
  for param in parameters:
    print(str(param.x), str(param.y), str(param.space), str(param.comm_range), str(param.disruption_range), str(param.R), str(param.nb_tag_loc), str(param.sink_allocation), str(param.nb_sink), str(param.nb_ch), str(param.agregation), str(param.directory))
    current_directory = param.directory
    print("Current directory" + str(current_directory))

    topology_ = import_param(current_directory + "topology_param.csv")
    topology_.import_nodes(current_directory + "nodes.csv")
    topology_.import_connectivity(current_directory + "connectivity.csv")
    topology_.import_routing(current_directory + "routing.csv")
    
    schedule = scheduling.import_schedule(current_directory + "schedule.csv", topology_.nodes)
    #TODO
    #import duration from schedule_stat
    stat = scheduling.import_schedule_stat(current_directory + "schedule_stat.csv")
    scheduling.export_schedule_stat(stat['duration'], schedule, topology_, current_directory + "schedule_stat.csv")
    print("Topology " + current_directory + " duration " + str(stat['duration']))







if __name__ == '__main__':
  # gen_topology_from_file("./example/bunch/var_space/toplogy_param.csv")
  gen_topology(Bunch_Parameters.get_parameters_from_file("./example/bunch/var_agreg/bunch_parameters.csv"))
  # gen_topology(Bunch_Parameters.get_parameters_from_file("./example/bunch/var_channels/bunch_parameters.csv"))
