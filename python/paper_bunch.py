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


class Bunch_Parameters():
  def __init__(self, x, y, space, comm_range, disruption_range, R, nb_tag_loc, nb_ch, agregation, dist_sink, directory):
    """
    A bunch a paramater, we recommend to only vary one parameter per bunch
    :param x witdhs of grids in meters
    :param y heights of grids in meters
    :param space distances in meter between anchors
    :param comm_range communication range in meter between anchors
    :param disruption_range the disruption range of communication in meter between anchors
    :param R number of tags per cell
    :param nb_tag_loc number of localisations per tag per slotframe
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
    self.nb_ch = nb_ch
    self.dist_sink = dist_sink
    self.agregation = agregation
    if directory[-1] != '/':
      directory = directory + '/'
    self.directory = directory

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
        parameters.append(Bunch_Parameters(float(row['x']), float(row['y']), float(row['space']), float(row['comm_range']), float(row['disruption_range']), int(row['R']), int(row['nb_tag_loc']), str(row['sink_allocation']), int(row['nb_sink']), int(row['nb_ch']),  int(row['agregation']), str(row['directory']) ))
    return parameters
  
        


def gen_topology(parameters):    
  """
  Generate a bunch of topology
  :param param a Bunch_Parameters object
  """
  i = 0
  for param in parameters:
    print(str(param.x), str(param.y), str(param.space), str(param.comm_range), str(param.disruption_range), str(param.R), str(param.nb_tag_loc), str(param.sink_allocation), str(param.nb_sink), str(param.nb_ch), str(param.agregation), str(param.directory))
    current_directory = param.directory
    print("Current directory" + str(current_directory))
    topology_ = topology.Topology(param.x, param.y, param.space, param.comm_range, param.disruption_range, param.R, param.nb_tag_loc)
    (anchors, tags) = topology_.generate_nodes()
    topology_.generate_neighbourhood(anchors, tags)

    if param.sink_allocation == SINK_BEST:
      topology_.set_sink(anchors[math.floor(len(anchors)/2)])
    elif param.sink_allocation == SINK_WORST:
      topology_.set_sink(anchors[0])
    elif param.sink_allocation == SINK_RANDOM:
      topology_.set_sink(anchors[random.randint(0, len(anchors))])
    else:
      raise Exception("Sink position parameter have an unsupported value " + str(param.sink_allocation))

    try:
        os.makedirs(current_directory)
    except OSError:
        print ("Creation of the directory %s failed" % current_directory)
    else:
        print ("Successfully created the directory %s" % current_directory)

    topology_.set_nodes(anchors, tags)

    graphics.plot_neighbours(topology_.nodes, current_directory + "plot_neighbours.pdf")
    if(topology_.generate_routing()):
      print("Routing generated")
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


def compute_queue_size(param):    
  """
  Import bunch parameter and compute the maximum queue of each nodes in the network during the scheudling.
  """  
  i = 0
  for param in parameters:
    print(str(param.x), str(param.y), str(param.space), str(param.comm_range), str(param.disruption_range), str(param.R), str(param.nb_tag_loc), str(param.sink_allocation), str(param.nb_sink), str(param.nb_ch), str(param.agregation), str(param.directory))
    current_directory = param.directory
    print("Current directory" + str(current_directory))
    
    schedule = scheduling.import_schedule(current_directory + "schedule.csv", topology_.nodes)

    scheduling.queue_sizes(schedule)







if __name__ == '__main__':
  # gen_topology_from_file("./example/bunch/var_space/toplogy_param.csv")
  gen_topology(Bunch_Parameters.get_parameters_from_file("./example/bunch/var_agreg/bunch_parameters.csv"))
  # gen_topology(Bunch_Parameters.get_parameters_from_file("./example/bunch/var_channels/bunch_parameters.csv"))
