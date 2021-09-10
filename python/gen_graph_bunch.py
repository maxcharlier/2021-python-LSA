import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from nodes.anchor import Anchor
from nodes.tag import Tag
from nodes.point import Point
import os
import scheduling
import topology
import graphics

from export_bunch import Bunch_Parameters

# Latex style
matplotlib.rc('text', usetex=True)
matplotlib.rc('font', family='serif')
matplotlib.rcParams.update({'font.size': 12})

def gen_graphs_from_file(result_directory, input_param="bunch_parameters.csv", output_file="stat_graph.pdf"):
  """Generate plot graph based on the schedule stat"""
  parameters = Bunch_Parameters.get_parameters_from_file(result_directory+input_param)
  title=Bunch_Parameters.get_str_variable_1_parameter(parameters)
  variable = Bunch_Parameters.get_variable_1_parameter(parameters)
  print(variable)
  duration = []
  len_schedule= []
  nb_slot = []
  nb_twr = []
  nb_data = []
  agregation_ = []
  nb_ch_ = []
  i = 0
  for param in parameters:
    stat = scheduling.import_schedule_stat(param.directory + "schedule_stat.csv")
    duration.append(float(stat["duration"]))
    len_schedule.append(int(stat["len_schedule"]))
    nb_slot.append(int(stat["nb_slot"]))
    nb_twr.append(int(stat["nb_twr"]))
    nb_data.append(int(stat["nb_data"]))
    agregation_.append(int(stat["agregation"]))
    nb_ch_.append(int(stat["nb_ch"]))
    i+=1
  plt.title(title)
  print(duration)
  print("len" + str(len_schedule))
  print("nb_slot" + str(nb_slot))
  print("nb_twr" + str(nb_twr))
  print("nb_data" + str(nb_data))
  print("agregation_" + str(agregation_))
  print("nb_ch_" + str(nb_ch_))
  # plt.plot(variable, duration, label="Duration")
  plt.plot(variable, len_schedule, label="Lenght")
  plt.plot(variable, nb_slot, label="Nb slots")
  plt.plot(variable, nb_twr, label="Nb TWR")
  plt.plot(variable, nb_data, label="Nb data")
  plt.plot(variable, agregation_, label="Agregation")
  plt.plot(variable, nb_ch_, label="Nb Ch")
  plt.legend()

  plt.savefig(result_directory + output_file)
  plt.close()

def plot_timeslots_usage(input_params, curves_names, output_file="plot_timeslots_usage.pdf", savefig=True):
  """Generate plot graph based on the schedule stat"""

  nb_tags = []
  nb_twr = []
  nb_data = []
  parameters = Bunch_Parameters.get_parameters_from_file(input_params[0])
  for param in parameters:
    stat = scheduling.import_schedule_stat(param.directory + "schedule_stat.csv")
    nb_twr.append(int(stat["nb_twr"]))
    nb_data.append(int(stat["nb_data"]))
    nb_tags.append(int(stat["nb_tags"]))
  plt.plot(nb_tags, nb_twr, label="TWR timeslot", marker=".")
  plt.plot(nb_tags, nb_data, label="Data timeslot", marker="+")
  plt.xlabel('Number of tags to localise in the network')
  plt.ylabel('Number of timeslots')
  plt.legend()
  if savefig:
    plt.savefig(output_file)
    plt.close()
  else:
    plt.show()

def slot_frame_lenght_graph(input_params, curves_names, output_file="slot_frame_lenght_graph.pdf", title="Benefit of concurrent communications"):
  """Generate plot graph based on the schedule stat"""
  for i in range(len(input_params)):
    len_schedule = []
    nb_tags = []
    parameters = Bunch_Parameters.get_parameters_from_file(input_params[i])
    for param in parameters:
      stat = scheduling.import_schedule_stat(param.directory + "schedule_stat.csv")
      len_schedule.append(int(stat["len_schedule"]))
      nb_tags.append(int(stat["nb_tags"]))
    plt.plot(nb_tags, len_schedule, label=curves_names[i], marker=".")
  plt.xlabel('Number of tags to localise in the network')
  plt.ylabel('Lenght of the resulting slotframe')
  plt.title(title)
  plt.legend()
  # plt.show()
  plt.savefig(output_file)
  plt.close()

def positionning_frequency_graph(input_params, curves_names, output_file="positionning_frequency_graph.pdf", title="Frequency of positioning", timeslot_duration=2.5, savefig=True):
  """Generate plot graph based on the schedule stat
  param timeslot_duration is in ms
  """
  for i in range(len(input_params)):
    len_schedule = []
    nb_tags = []
    parameters = Bunch_Parameters.get_parameters_from_file(input_params[i])
    for param in parameters:
      stat = scheduling.import_schedule_stat(param.directory + "schedule_stat.csv")
        
      if(int(stat["nb_tags"]) > 50):
        len_schedule.append(1000.0/(int(stat["len_schedule"])*timeslot_duration))
        nb_tags.append(int(stat["nb_tags"]))

      if(int(stat["nb_tags"]) == 400):
        print(curves_names[i])
        print((int(stat["len_schedule"])*timeslot_duration)/1000)
    plt.plot(nb_tags, len_schedule, label=curves_names[i], marker=".")
  plt.xlabel('Number of tags to localise in the network')
  plt.ylabel('Localisation update (Hz)')
  plt.title(title)
  plt.legend()
  if savefig:
    plt.savefig(output_file)
    plt.close()
  else:
    plt.show()

type_of_curve = ["Communication per cells", "Agreagation per cells", "Communication per timeslot", "Agreagation per timeslot"]

def plot_slotframe_distrib(input_csv_file, file="plot_slotframe_stepdistrib.pdf", type_of_curve_index=0, cumulative=True):
  """ Plot the number of communication per cells"""

  plt.title("Slotframe Communications distribution - " + type_of_curve[type_of_curve_index])
  plt.gca().set_xscale('log')
  parameters = Bunch_Parameters.get_parameters_from_file(input_csv_file)
  for param in parameters:
    _topology = topology.Topology.import_param(param.directory + "/topology_param.csv")
    _topology.import_nodes(param.directory + "/nodes.csv")
    schedule = scheduling.import_schedule(param.directory + "schedule.csv", _topology.nodes)

    #cells counter
    nb_comm = range(0, 500)
    c_comm_all = [0 for i in range(0, len(nb_comm))]
    c_weight_all = [0 for i in range(0, len(nb_comm))]
    #timeslot counter
    t_comm_all = [0 for i in range(0, len(nb_comm))]
    t_weight_all = [0 for i in range(0, len(nb_comm))]
    nb_channel = [0 for i in range(0, 8)]
    for timeslot in schedule:
      t_comm = 0
      t_weight = 0
      for channel in timeslot:
        c_comm_all[len(channel)] += 1
        c_weight = 0
        for link in channel:
          c_weight += link.weight
        c_weight_all[c_weight] += 1
        t_comm += len(channel)
        t_weight += c_weight
      t_comm_all[t_comm] += 1
      t_weight_all[t_weight] += 1

    # convert to %
    def convert_to_pourcent(_list):
      tot = sum(_list)
      cum = 0
      for i in range(len(_list)):
        _list[i] = float(_list[i])/tot * 100.0
        if cumulative:
          cum = cum + _list[i]
          _list[i] = cum
      return _list
    def get_max_comm(_list):
      max_comm = 0
      for i in range(len(_list)):
        if (_list[i] >0):
          max_comm = i
      return max_comm +1
    if type_of_curve_index == 0:
      nb_comm = range(0, get_max_comm(c_comm_all))
      plt.plot(nb_comm, convert_to_pourcent(c_comm_all)[0:len(nb_comm)], drawstyle='steps-post', label=param.name)
    elif type_of_curve_index == 1:
      nb_comm = range(0, get_max_comm(c_weight_all))
      plt.plot(nb_comm, convert_to_pourcent(c_weight_all)[0:len(nb_comm)], drawstyle='steps-post', label=param.name)
    elif type_of_curve_index == 2:
      nb_comm = range(0, get_max_comm(t_comm_all))
      plt.plot(nb_comm, convert_to_pourcent(t_comm_all)[0:len(nb_comm)], drawstyle='steps-post', label=param.name)
    else:
      nb_comm = range(0, get_max_comm(t_weight_all))
      plt.plot(nb_comm, convert_to_pourcent(t_weight_all)[0:len(nb_comm)], drawstyle='steps-post', label=param.name)


  plt.legend()

  plt.savefig(file)
  plt.close()


def plot_slotframe_channels_usage(input_csv_file, file="plot_slotframe_channels_usage.pdf", cumulative=True, nb_channel_max=8):
  """ Plot the number of communication per cells"""

  plt.title("Slotframe channels usages distribution")

  parameters = Bunch_Parameters.get_parameters_from_file(input_csv_file)
  for param in parameters:
    _topology = topology.Topology.import_param(param.directory + "/topology_param.csv")
    _topology.import_nodes(param.directory + "/nodes.csv")
    schedule = scheduling.import_schedule(param.directory + "schedule.csv", _topology.nodes)

    #cells counter
    channels = range(1, nb_channel_max+1)
    comm_channels = [0 for i in range(0, len(channels))]
    for timeslot in schedule:
      comm_channels[len(timeslot)-1] = comm_channels[len(timeslot)-1]  + 1

    # convert to %
    def convert_to_pourcent(_list):
      tot = sum(_list)
      cum = 0
      for i in range(len(_list)):
        _list[i] = float(_list[i])/tot * 100.0
        if cumulative:
          cum = cum + _list[i]
          _list[i] = cum
      return _list
    def get_max_comm(_list):
      max_comm = 0
      for i in range(len(_list)):
        if (_list[i] >0):
          max_comm = i
      return max_comm +1

    plt.plot(channels, convert_to_pourcent(comm_channels), drawstyle='steps-post', label=param.name)


  plt.legend()

  plt.savefig(file)
  plt.close()

if __name__ == '__main__':
  gen_graphs_from_file("./example/bunch/var_agreg/")
  gen_graphs_from_file("./example/bunch/var_channels/")
