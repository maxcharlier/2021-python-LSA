from math import ceil
from nodes.anchor import Anchor
from nodes.tag import Tag
from nodes.point import Point
import graphics
import scheduling
import topology
import os #creation of directory
import random

"""This file is used to generate a bunch of topology , export them an then generate figure with a loader"""
SINK_BEST ="best"
SINK_WORST = "worst"
SINK_RANDOM = "random"

param_x = [20]
param_y = [20]
param_space = [1 ,5,10,15,20]
param_comm_range = [4]
param_disruption_range= [5]
param_R = [1]
param_nb_tag_loc = [1]
param_sink_allocation = [POSITION_CENTER]
param_nb_sink = [1]
param_nb_ch = [6]
param_agregation = [1]

def gen_topology(param_x, param_y, param_space, param_comm_range, param_disruption_range, param_R, param_nb_tag_loc, param_sink_allocation, param_nb_sink, param_nb_ch, param_agregation, directory):    
  """
  Generate a bunch of topology
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
  if directory[-1] != '/':
    directory = directory + '/'
  for x in param_x:
    for y in param_y:
      for space in param_space:
        for comm_range in param_comm_range:
          for disruption_range in param_disruption_range:
            for R in param_R:
              for nb_tag_loc in param_nb_tag_loc:
                for sink_allocation in  param_sink_allocation:
                  for nb_sink in  param_nb_sink:
                    for n_ch in param_nb_ch:
                      for agregation in param_agregation:

                        current_directory = "/x/" + str(x) + "/y/" + str(y) + "/space/" + str(space) + "/comm/" + str(comm) + "/disruption/" + str(disruption_range) + "/R/" + str(R) + "/tag-loc/" + str(nb_tag_loc) + "/sink/" + str(sink_allocation)+"/nb_sink/"+ str(nb_sink) + "/ch/" + str(n_ch) + "/agreg/" + str(agregation) + "/"
                        current_directory = directory + current_directory

                        topology_ = Topology(x, y, space, comm_range, disruption_range, R, nb_tag_loc)
                        (anchors, tags) = topology.generate_nodes()
                        topology_.generate_neighbourhood(anchors, tags)
                        if sink_allocation == SINK_BEST:
                          topology_.set_sink(anchors[floor(len(anchors)/2)])
                        elif sink_allocation == SINK_WORST:
                          topology_.set_sink(anchors[0])
                        elif sink_allocation == SINK_RANDOM:
                          topology_.set_sink(anchors[random.randint(0, len(anchors))])
                        else:
                          raise Exception("Sink position parameter have an unsupported value")

                        try:
                            os.makedirs(path)
                        except OSError:
                            print ("Creation of the directory %s failed" % path)
                        else:
                            print ("Successfully created the directory %s" % path)
                        topology_.set_nodes(anchors, tags)
                        topology_.generate_routing()
                        graphics.plot_C(topology_.nodes, current_directory + "graph-C.pdf")
                        graphics.plot_neighbours(topology_.nodes, current_directory + "plot_neighbours.pdf")
                        graphics.plot_network_routing(topology_.nodes, current_directory + "plot_network_routing.pdf")
                        graphics.plot_Q(topology_.nodes, current_directory + "plot_Q.pdf")
                        graphics.dot_network_routing(topology_.nodes, current_directory + "dot_network_routing.dot")

                        (schedule, duration) = scheduling.scheduling(topology_, n_ch=n_ch, agregation=agregation)

                        topology_.export_param(current_directory + "topology_param.csv")
                        topology_.export_nodes(current_directory + "nodes.csv")
                        topology_.export_connectivity(current_directory + "connectivity.csv")
                        topology_.export_routing(current_directory + "routing.csv")
                        scheduling.export_schedule(schedule, current_directory + "schedule.csv")
                        scheduling.export_schedule_stat(duration, schedule, topology_, current_directory + "schedule_stat.csv")
                        print("Topology " + current_directory + " duration " + str(duration))

def update_stat_topology(param_x, param_y, param_space, param_comm_range, param_disruption_range, param_R, param_nb_tag_loc, param_sink_allocation, param_nb_sink, param_nb_ch, param_agregation, directory):    
  """
  Generate a bunch of topology
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
  if directory[-1] != '/':
    directory = directory + '/'
  for x in param_x:
    for y in param_y:
      for space in param_space:
        for comm_range in param_comm_range:
          for disruption_range in param_disruption_range:
            for R in param_R:
              for nb_tag_loc in param_nb_tag_loc:
                for sink_allocation in  param_sink_allocation:
                  for nb_sink in  param_nb_sink:
                    for n_ch in param_nb_ch:
                      for agregation in param_agregation:
                        current_directory = "/x/" + str(x) + "/y/" + str(y) + "/space/" + str(space) + "/comm/" + str(comm) + "/disruption/" + str(disruption_range) + "/R/" + str(R) + "/tag-loc/" + str(nb_tag_loc) + "/sink/" + str(sink_allocation)+"/nb_sink/"+ str(nb_sink) + "/ch/" + str(n_ch) + "/agreg/" + str(agregation) + "/"
                        current_directory = directory + current_directory

                        topology_ = import_param(current_directory + "topology_param.csv")
                        topology_.import_nodes(current_directory + "nodes.csv")
                        topology_.import_connectivity(current_directory + "connectivity.csv")
                        topology_.import_routing(current_directory + "routing.csv")
                        
                        schedule = scheduling.import_schedule(current_directory + "schedule.csv", topology_.nodes)
                        #TODO
                        #import duration from schedule_stat
                        scheduling.export_schedule_stat(duration, schedule, topology_, current_directory + "schedule_stat.csv")
                        print("Topology " + current_directory + " duration " + str(duration))

def export_toplogy_param(param_x, param_y, param_space, param_comm_range, param_disruption_range, param_R, param_nb_tag_loc, param_sink_allocation, param_nb_sink, param_nb_ch, param_agregation, directory):
  """Recommanded file name is "toplogy_param.csv" """
    with open(file, 'w') as csvfile:
      fieldnames = ['param_x', 'param_y', 'param_space', 'param_comm_range', 'param_disruption_range', 'param_R', 'param_nb_tag_loc', 'param_sink_allocation', 'param_nb_sink', 'param_nb_ch', 'param_agregation', 'directory']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerow({'param_x': str(param_x), 'param_y': str(param_y), 'param_space': str(param_space), 'param_comm_range': str(param_comm_range), 'param_disruption_range': str(param_disruption_range), 'param_R': str(param_R), 'param_nb_tag_loc': str(param_nb_tag_loc), 'param_sink_allocation': str(param_sink_allocation),, 'param_nb_sink': str(param_nb_sink), 'param_nb_ch': str(param_nb_ch), 'param_agregation': str(param_agregation), 'directory': str(directory)})

def gen_topology_from_file(file):
  """Recommanded file name is "toplogy_param.csv" """
    with open(file) as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        return gen_topology(param_from_str(row['param_x']), param_from_str(row['param_y']), param_from_str(row['param_space']), param_from_str(row['param_comm_range']), param_from_str(row['param_disruption_range']), param_from_str(row['param_R']), param_from_str(row['param_nb_tag_loc']), param_from_str(row['param_sink_allocation']), param_from_str(row['param_nb_sink']), param_from_str(row['param_nb_ch']),  param_from_str(row['param_agregation']), str(row['directory']) )
      


def param_from_str(param):
    return list(pos.replace('[', '').replace(']', '').split(', '))

gen_topology_from_file("./example/bunch/var_space/toplogy_param.csv")
