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

param_x = [20]
param_y = [20]
param_space = [1 ,5,12,15,20]
param_comm_range = [4]
param_disruption_range= [5]
param_R = [1]
param_nb_tag_loc = [1]
param_sink_allocation = [SINK_BEST]
param_nb_sink = [1]
param_nb_ch = [6]
param_agregation = [1]
directory = './example/bunch/var_space'
class Bunch_Parameters():
  def __init__(self, x, y, space, comm_range, disruption_range, R, nb_tag_loc, sink_allocation, nb_sink, nb_ch, agregation, directory):
    """
    A bunch a paramater, we recommend to only vary one parameter per bunch
    :param param_x witdhs of grids in meters
    :param param_y heights of grids in meters
    :param param_space distances in meter between anchors
    :param param_comm_range communication range in meter between anchors
    :param param_disruption_range the disruption range of communication in meter between anchors
    :param param_R number of tags per cell
    :param param_nb_tag_loc number of localisations per tag per slotframe
    :param param_sink_allocation Define the pattern of allocation of anchors (best, worst or random)
    :param param_nb_sink Define the number of sink
    :param param_nb_ch Define the number of channels
    :param param_agregation Define the aggregation capacity of anchors 
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

  def export_toplogy_param(self, file="toplogy_param.csv"):
    """Recommanded file name is "toplogy_param.csv" """

    file = self.directory + file
    with open(file, 'w') as csvfile:
      fieldnames = ['x', 'y', 'space', 'comm_range', 'disruption_range', 'R', 'nb_tag_loc', 'sink_allocation', 'nb_sink', 'nb_ch', 'agregation', 'directory']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerow({'x': str(self.x), 'y': str(self.y), 'space': str(self.space), 'comm_range': str(self.comm_range), 'disruption_range': str(self.disruption_range), 'R': str(R), 'nb_tag_loc': str(self.nb_tag_loc), 'sink_allocation': str(self.sink_allocation), 'nb_sink': str(self.nb_sink), 'nb_ch': str(self.nb_ch), 'agregation': str(self.agregation), 'directory': str(self.directory)})

  def get_param_from_file(file):
    """Recommanded file name is "toplogy_param.csv" """
    def str_from_str(param):
        return list(param.replace('[', '').replace(']', '').replace('\'', '').split(', '))
    def int_from_str(param):
        params = list(param.replace('[', '').replace(']', '').replace('\'', '').split(', '))
        for i in range(len(params)):
          params[i] = int(params[i])
        return params
    def float_from_str(param):
        params = list(param.replace('[', '').replace(']', '').replace('\'', '').split(', '))
        for i in range(len(params)):
          params[i] = float(params[i])
        return params
    with open(file) as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        # print(str(row['directory']))
        # print(float_from_str(row['x']), float_from_str(row['y']), float_from_str(row['space']), float_from_str(row['comm_range']), float_from_str(row['disruption_range']), int_from_str(row['R']), int_from_str(row['nb_tag_loc']), str_from_str(row['sink_allocation']), int_from_str(row['nb_sink']), int_from_str(row['nb_ch']),  int_from_str(row['agregation']), str(row['directory']))
        return Bunch_Parameters(float_from_str(row['x']), float_from_str(row['y']), float_from_str(row['space']), float_from_str(row['comm_range']), float_from_str(row['disruption_range']), int_from_str(row['R']), int_from_str(row['nb_tag_loc']), str_from_str(row['sink_allocation']), int_from_str(row['nb_sink']), int_from_str(row['nb_ch']),  int_from_str(row['agregation']), str(row['directory']) )
  
  def get_str_variable_parameter(self):
    """Return the name of the variable parameter"""
    if len(self.x) > 1:
      return "x"
    elif len(self.y) > 1:
      return "y"
    elif len(self.space) > 1:
      return "space"
    elif len(self.comm_range) > 1:
      return "Communication Range"
    elif len(self.disruption_range) > 1:
      return "Disruption Range"
    elif len(self.R) > 1:
      return "R"
    elif len(self.nb_tag_loc) > 1:
      return "Number of tag loc"
    elif len(self.sink_allocation) > 1:
      return "Sink Allocation"
    elif len(self.nb_sink) > 1:
      return "Number of sink"
    elif len(self.nb_ch) > 1:
      return "Number of channels"
    elif len(self.agregation) > 1:
      return "Agregation"
    return "Unknown paramter"  

  def get_variable_parameter(self):
    """Return the name of the variable parameter"""
    if len(self.x) > 1:
      return self.x
    elif len(self.y) > 1:
      return self.y
    elif len(self.space) > 1:
      return self.space
    elif len(self.comm_range) > 1:
      return self.comm_range
    elif len(self.disruption_range) > 1:
      return self.disruption_range
    elif len(self.R) > 1:
      return self.R
    elif len(self.nb_tag_loc) > 1:
      return self.nb_tag_loc
    elif len(self.sink_allocation) > 1:
      return self.sink_allocation
    elif len(self.nb_sink) > 1:
      return self.nb_sink
    elif len(self.nb_ch) > 1:
      return self.nb_ch
    elif len(self.agregation) > 1:
      return self.agregation
    return None

        


def gen_topology(param):    
  """
  Generate a bunch of topology
  :param param a Bunch_Parameters object
  """
  print(str(param.x), str(param.y), str(param.space), str(param.comm_range), str(param.disruption_range), str(param.R), str(param.nb_tag_loc), str(param.sink_allocation), str(param.nb_sink), str(param.nb_ch), str(param.agregation), str(param.directory))
  directory = param.directory
  for x in param.x:
    for y in param.y:
      for space in param.space:
        for comm_range in param.comm_range:
          for disruption_range in param.disruption_range:
            for R in param.R:
              for nb_tag_loc in param.nb_tag_loc:
                for sink_allocation in  param.sink_allocation:
                  for nb_sink in  param.nb_sink:
                    for nb_ch in param.nb_ch:
                      for agregation in param.agregation:

                        current_directory = "x/" + str(x) + "/y/" + str(y) + "/space/" + str(space) + "/comm/" + str(comm_range) + "/disruption/" + str(disruption_range) + "/R/" + str(R) + "/tag-loc/" + str(nb_tag_loc) + "/sink/" + str(sink_allocation)+"/nb_sink/"+ str(nb_sink) + "/ch/" + str(nb_ch) + "/agreg/" + str(agregation) + "/"
                        current_directory = directory + current_directory
                        print("Current directory" + str(current_directory))
                        topology_ = topology.Topology(x, y, space, comm_range, disruption_range, R, nb_tag_loc)
                        (anchors, tags) = topology_.generate_nodes()
                        topology_.generate_neighbourhood(anchors, tags)

                        if sink_allocation == SINK_BEST:
                          topology_.set_sink(anchors[math.floor(len(anchors)/2)])
                        elif sink_allocation == SINK_WORST:
                          topology_.set_sink(anchors[0])
                        elif sink_allocation == SINK_RANDOM:
                          topology_.set_sink(anchors[random.randint(0, len(anchors))])
                        else:
                          raise Exception("Sink position parameter have an unsupported value " + str(sink_allocation))

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

                          (schedule, duration) = scheduling.scheduling(topology_, n_ch=nb_ch, agregation=agregation)

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
  print(str(param.x), str(param.y), str(param.space), str(param.comm_range), str(param.disruption_range), str(param.R), str(param.nb_tag_loc), str(param.sink_allocation), str(param.nb_sink), str(param.nb_ch), str(param.agregation), str(directory))
  if directory[-1] != '/':
    directory = directory + '/'
  for x in param.x:
    for y in param.y:
      for space in param.space:
        for comm_range in param.comm_range:
          for disruption_range in param.disruption_range:
            for R in param.R:
              for nb_tag_loc in param.nb_tag_loc:
                for sink_allocation in  param.sink_allocation:
                  for nb_sink in  param.nb_sink:
                    for nb_ch in param.nb_ch:
                      for agregation in param.agregation:
                        current_directory = "/x/" + str(x) + "/y/" + str(y) + "/space/" + str(space) + "/comm/" + str(comm_range) + "/disruption/" + str(disruption_range) + "/R/" + str(R) + "/tag-loc/" + str(nb_tag_loc) + "/sink/" + str(sink_allocation)+"/nb_sink/"+ str(nb_sink) + "/ch/" + str(nb_ch) + "/agreg/" + str(agregation) + "/"
                        current_directory = directory + current_directory

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
  # export_toplogy_param(param_x, param_y, param_space, param_comm_range, param_disruption_range, param_R, param_nb_tag_loc, param_sink_allocation, param_nb_sink, param_nb_ch, param_agregation, directory)
  # gen_topology_from_file("./example/bunch/var_space/toplogy_param.csv")
  # gen_topology(Bunch_Parameters.get_param_from_file("./example/bunch/var_agreg/toplogy_param.csv"))
  gen_topology(Bunch_Parameters.get_param_from_file("./example/bunch/var_channels/toplogy_param.csv"))
