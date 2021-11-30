from abc import ABC
import sys 
import os
sys.path.append('../../../')
from export_bunch import gen_topology
from gen_graph_bunch import slot_frame_length_graph
from gen_graph_bunch import positionning_frequency_graph
from gen_graph_bunch import plot_timeslots_usage
from gen_graph_bunch import plot_transmissions_repartion
from gen_graph_bunch import gen_graphs_from_file
from gen_graph_bunch import plot_slotframe_distrib
from gen_graph_bunch import plot_slotframe_channels_usage
from gen_graph_bunch import schedule_duration_graph
from gen_graph_bunch import plot_max_queue_size
from export_bunch import Bunch_Parameters
import scheduling
import topology
import graphics

def display_table_parameters(input_params):
  """Display parameter of the simulation with a latex table format"""
  print(" Radius & Cells & Anchors & Mobile Nodes\\\\")
  for i in range(len(input_params)):
    parameters = Bunch_Parameters.get_parameters_from_file(input_params[i])
    for param in parameters:
      stat = scheduling.import_schedule_stat(param.directory + "schedule_stat.csv")

      print(param.dist_sink, end='')
      print(" & ", end='')
      print(stat["nb_tags"], end='')
      print(" & ", end='')
      print(stat["nb_anchors"], end='')
      print(" & ", end='')
      print(stat["nb_tags"], end='')
      print("\\\\")

dir_path = os.path.dirname(os.path.realpath(__file__))

display_table_parameters([dir_path + "/ch1-agr1.csv"])
display_table_parameters([dir_path + "/ch1-agr1-worst.csv"])
