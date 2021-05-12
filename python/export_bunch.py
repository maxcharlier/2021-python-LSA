from math import ceil
from nodes.anchor import Anchor
from nodes.tag import Tag
from nodes.point import Point
import graphics
import scheduling
import topology
import os #creation of directory

"""This file is used to generate a bunch of topology , export them an then generate figure with a loader"""
POSITION_CENTER ="center"
POSITION_CONER = "left_lower_corner"

param_x = (20, 20, 0)
param_y = (20,20 ,0)
param_space = (1, 20, 1)
param_comm_range = (4, 4, 0)
param_disruption_range= (5, 5, 0)
param_R = (1, 1 ,0)
param_nb_tag_loc = (1, 1, 0)
param_sink_position = [POSITION_CENTER]
param_n_ch = (6, 6, 0)
param_agregation = (1, 1, 0)

def gen_topology(param_x, param_y, param_space, param_comm_range, param_disruption_range, param_R, param_nb_tag_loc, param_sink_position, param_n_ch, param_agregation, directory):
  if directory[-1] != '/':
    directory = directory + '/'
  for x in range(param_x[0], param_x[1], param_x[2]):
    for y in range(param_y[0], param_y[1], param_y[2]):
      for space in range(param_space[0], param_space[1], param_space[2]):
        for comm_range in range(param_comm_range[0], param_comm_range[1], param_comm_range[2]):
          for disruption_range in range(param_disruption_range[0], param_disruption_range[1], param_disruption_range[2]):
            for R in range(param_R[0], param_R[1], param_R[2]):
              for nb_tag_loc in range(param_nb_tag_loc[0], param_nb_tag_loc[1], param_nb_tag_loc[2]):
                for sink_position in  param_sink_position:
                  for n_ch in range(param_n_ch[0], param_n_ch[1], param_n_ch[2]):
                    for agregation in range(param_agregation[0], param_agregation[1], param_agregation[2]):

                      topology_ = Topology(x, y, space, comm_range, disruption_range, R, nb_tag_loc)
                      (anchors, tags) = topology.generate_nodes()
                      topology_.generate_neighbourhood(anchors, tags)
                      if sink_position == POSITION_CENTER:
                        topology_.set_sink(anchors[floor(len(anchors)/2)])
                      elif sink_position == POSITION_CONER:
                        topology_.set_sink(anchors[0])
                      else:
                        raise Exception("Sink posotion parameter have an unsupported value")

                      current_directory = directory + "_x" + str(x) + "_y" + str(y) + "_space" + str(space) + "_comm" + str(comm) + "_disruption" + str(disruption_range) + "_R" + str(R) + "_tl" + str(nb_tag_loc) + "_sink-" + str(sink_position) + "_ch" + str(n_ch) + "_agreg" + str(agregation) + "/"
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
                      scheduling.export_schedule_stat(duration, schedule, current_directory + "schedule_stat.csv")
                      print("Topology " + current_directory + " duration " + str(duration))

def export_toplogy_param(file, param_x, param_y, param_space, param_comm_range, param_disruption_range, param_R, param_nb_tag_loc, param_sink_position, param_n_ch, param_agregation, directory):
  """Recommanded file name is "toplogy_param.csv" """
    with open(file, 'w') as csvfile:
      fieldnames = ['param_x', 'param_y', 'param_space', 'param_comm_range', 'param_disruption_range', 'param_R', 'param_nb_tag_loc', 'param_sink_position', 'param_n_ch', 'param_agregation', 'directory']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerow({'param_x': str(param_x), 'param_y': str(param_y), 'param_space': str(param_space), 'param_comm_range': str(param_comm_range), 'param_disruption_range': str(param_disruption_range), 'param_R': str(param_R), 'param_nb_tag_loc': str(param_nb_tag_loc), 'param_sink_position': str(param_sink_position), 'param_n_ch': str(param_n_ch), 'param_agregation': str(param_agregation), 'directory': str(directory)})

def gen_topology_from_file(file):
  """Recommanded file name is "toplogy_param.csv" """
    with open(file) as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        return gen_topology(param_from_str(row['param_x']), param_from_str(row['param_y']), param_from_str(row['param_space']), param_from_str(row['param_comm_range']), param_from_str(row['param_disruption_range']), param_from_str(row['param_R']), param_from_str(row['param_nb_tag_loc']), param_from_str(row['param_sink_position']), param_from_str(row['param_n_ch']),  param_from_str(row['param_agregation']), str(row['directory']) )
      


def param_from_str(param):
    param = pos.replace('(', '').replace(')', '').split(', ')

    """Filter parameter to have a correct generation of topology"""
    if len(param) != 3:
      raise Exception("Parameters need to be a tuple of 3 values, start, end, step")
    start = param[0]
    end = param[1]
    step = param[2]
    if start == end:
      step = 1 #set a default value for step to allow range function to work correctly
    if step == 0 and star != end:
      raise Exception("Incorect incrementing step given: (0) will cause infinite loop")
    return (start, end, step)
