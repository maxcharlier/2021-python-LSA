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
import seaborn
import pandas
from statistics import mean

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

def plot_timeslots_usage(input_params, curves_names, output_file="plot_timeslots_usage.pdf", savefig=True, index_param=0):
  """Generate the number of timeslot accoridng to the network size"""

  nb_tags = []
  nb_twr = []
  nb_data = []
  parameters = Bunch_Parameters.get_parameters_from_file(input_params[index_param])
  print("plot_timeslots_usage() curve name : " + str(curves_names[index_param]))
  for param in parameters:
    stat = scheduling.import_schedule_stat(param.directory + "schedule_stat.csv")
    nb_twr.append(int(stat["nb_twr"]))
    nb_data.append(int(stat["nb_data"]))
    nb_tags.append(int(stat["nb_tags"]))
  plt.plot(nb_tags, nb_twr, label="TWR timeslot", marker=".")
  plt.plot(nb_tags, nb_data, label="Data timeslot", marker="+")
  plt.xlabel('Number of cells of the network')
  plt.ylabel('Number of timeslots')
  plt.legend()
  if savefig:
    plt.savefig(output_file)
    plt.close()
  else:
    plt.show()

def plot_transmissions_repartion(param_best, param_worst, output_file="plot_transmissions_repartition.pdf", savefig=True):
  """Generate the number of transmissions according to the network size
  Best use case when the sink is in the center of the grid
  Worst when the sink is in a corner"""

  nb_tags_best = []
  nb_tags_worst = []
  nb_twr_best = []
  nb_data_best = []
  nb_twr_worst = []
  nb_data_worst = []
  all_best = []
  all_worst = []
  parameters_best = Bunch_Parameters.get_parameters_from_file(param_best)
  for param in parameters_best:
    stat = scheduling.import_schedule_stat(param.directory + "schedule_stat.csv")
    nb_twr_best.append(int(stat["nb_twr"]))
    nb_data_best.append(int(stat["nb_data"]))
    all_best.append(int(stat["nb_data"])+int(stat["nb_twr"]))

    nb_tags_best.append(int(stat["nb_tags"]))

  parameters_worst = Bunch_Parameters.get_parameters_from_file(param_worst)
  for param in parameters_worst:
    stat = scheduling.import_schedule_stat(param.directory + "schedule_stat.csv")
    nb_twr_worst.append(int(stat["nb_twr"]))
    nb_data_worst.append(int(stat["nb_data"]))
    all_worst.append(int(stat["nb_data"])+ int(stat["nb_twr"]))
    nb_tags_worst.append(int(stat["nb_tags"]))

  plt.plot(nb_tags_best, nb_twr_best, label="TWR - center", marker=".", linestyle='solid', color='tab:blue')
  plt.plot(nb_tags_best, nb_data_best, label="Data - center", marker="+", linestyle='solid', color='tab:blue')  
  plt.plot(nb_tags_best, all_best, label="All - center", marker="d", linestyle='solid', color='tab:blue')

  plt.plot(nb_tags_worst, nb_twr_worst, label="TWR - corner", marker=".", linestyle='dashed', color='tab:orange')
  plt.plot(nb_tags_worst, nb_data_worst, label="Data - corner", marker="+", linestyle='dashed', color='tab:orange')
  plt.plot(nb_tags_worst, all_worst, label="All - corner", marker="d", linestyle='dashed', color='tab:orange')

  plt.xlabel('Number of cells of the network')
  plt.ylabel('Number of transmissions')
  plt.legend()
  if savefig:
    plt.savefig(output_file)
    plt.close()
  else:
    plt.show()

def plot_hop_count0(param_best, param_worst, output_file="plot_hop_count.pdf", savefig=True):
  """Generate the number of hop according to the network size
  Best use case when the sink is in the center of the grid
  Worst when the sink is in a corner"""

  nb_hop_best = []
  nb_tags_best = []
  nb_hop_worst = []
  nb_tags_worst = []

  parameters_best = Bunch_Parameters.get_parameters_from_file(param_best)
  for param in parameters_best:
    nb_hop = []
    # topology_ = topology.Topology(20, 20, 1, 2, 3, 1, 1)
    topology_ = topology.Topology.import_param(param.directory + "topology_param.csv")
    topology_.import_nodes(param.directory + "nodes.csv")
    topology_.import_connectivity(param.directory + "connectivity.csv")
    topology_.import_routing(param.directory + "routing.csv")
    # print(topology_.sinks)
    #set the rank value of each node
    # topology_.generate_routing()
    for node in topology_.nodes:
      nb_hop.append(node.get_rank())

    stat = scheduling.import_schedule_stat(param.directory + "schedule_stat.csv")
    nb_hop_best.append(nb_hop)
    # print(nb_hop_best)
    nb_tags_best.append(int(stat["nb_tags"]))

  # parameters_worst = Bunch_Parameters.get_parameters_from_file(param_worst)
  # for param in parameters_worst:
  #   nb_hop = []
  #   topology_ = topology.Topology(20, 20, 1, 2, 3, 1, 1)
  #   topology_ = import_param(param.directory + "topology_param.csv")
  #   topology_.import_nodes(param.directory + "nodes.csv")
  #   topology_.import_connectivity(param.directory + "connectivity.csv")
  #   topology_.import_routing(param.directory + "routing.csv")
  #   #set the rank value of each node
  #   topology_.generate_routing()
  #   for node in topology_.nodes:
  #     nb_hop.append(node.get_rank())

  #   stat = scheduling.import_schedule_stat(param.directory + "schedule_stat.csv")
  #   nb_hop_worst.append(nb_hop)
  #   nb_tags_worst.append(int(stat["nb_tags"]))

  print(nb_tags_best[5])
  plt.boxplot(nb_hop_best[5], labels=nb_tags_best[5])

  # plt.plot(nb_tags_worst, all_worst, label="All - corner", marker="d", linestyle='dashed', color='tab:orange')

  plt.xlabel('Number of cells of the network')
  plt.ylabel('Number of transmissions')
  plt.legend()
  if savefig:
    plt.savefig(output_file)
    plt.close()
  else:
    plt.show()


def plot_hop_count(param_best, param_worst, output_file="plot_hop_count.pdf", savefig=True):
  """Generate the number of hop according to the network size
  Best use case when the sink is in the center of the grid
  Worst when the sink is in a corner"""

  fig, axs = plt.subplots(2)
  def boxplot(parameter_file, axis, title):
    nb_hops = []
    nb_cells = []
    directory_param = []
    parameters = Bunch_Parameters.get_parameters_from_file(parameter_file)
    for param in parameters:
      nb_hop = []
      # topology_ = topology.Topology(20, 20, 1, 2, 3, 1, 1)
      topology_ = topology.Topology.import_param(param.directory + "topology_param.csv")
      topology_.import_nodes(param.directory + "nodes.csv")
      topology_.import_connectivity(param.directory + "connectivity.csv")
      topology_.import_routing(param.directory + "routing.csv")
      # print(topology_.sinks)
      #set the rank value of each node
      # topology_.generate_routing()
      selected_node = []
      for node in topology_.nodes:
        if node.type == 'anchor' :
          for children in node.childrens:
            if children.type == 'tag': 
              nb_hop.append(node.get_rank())
        elif node.type == 'tag' :
          nb_hop.append(node.get_rank())

      stat = scheduling.import_schedule_stat(param.directory + "schedule_stat.csv")
      nb_hops.append(nb_hop)
      # print(nb_hops)
      nb_cells.append(int(stat["nb_tags"]))
      directory_param.append(param.directory)

    #remove duplicate
    i = 0
    while i < len(nb_cells)-1:
      if nb_cells[i] == nb_cells[i+1]:
        del nb_cells[i]
        del nb_hops[i]
        del directory_param[i]
      if nb_hops[i] == []:
        del nb_cells[i]
        del nb_hops[i]
        del directory_param[i]
      i+=1
    means = []
    for x in nb_hops:
      means.append(mean(x))
    print("len hops" + str(len(nb_hops)))
    print("len nb_cells" + str(len(nb_cells)))
    print("len directory" + str(len(directory_param)))
    data =  {'hops': nb_hops,
          'cells': nb_cells,
          'directory' : directory_param}

    dataframe  = pandas.DataFrame( data )
    print(dataframe)

    axis.plot(nb_cells, means, color='tab:grey', linestyle='--') 
    #whis avoid outliers, defautl value is 1.5
    axis.boxplot(nb_hops, positions=nb_cells, labels= ['' for x in range(len(nb_cells))], widths=1.5, whis=3.0)
    axis.set_title(title)
    # axis.set_yticks(np.arange(0, 22, 2.5), [int(x) if int(x)%5==0 else '' for x in np.arange(0, 22, 2.5)])
    axis.set_yticks(np.arange(0, 22, 2.5))
    # axis.set_xticks(range(0, 401, 50), ['' for x in range(0, 401, 50)]) 
    axis.set_xticks([]) 
    # axis.tick_params(labelrotation=90) 
    axis.set_xlim(-10, 410)
    axis.set_ylim(0, 22)
    axis.set_ylabel('Path length')
  boxplot(param_best, axs[0], "Sink in the center")
  boxplot(param_worst, axs[1], "Sink in a corner")
  plt.xticks(range(0, 401, 50), range(0, 401, 50), rotation=0)
  plt.xlabel('Number of cells of the network')
  # plt.xlim(-10, 410)
  fig.tight_layout()
  # plt.plot(nb_tags_worst, all_worst, label="All - corner", marker="d", linestyle='dashed', color='tab:orange')

  # plt.xlabel('Number of cells of the network')
  # plt.ylabel('Number of transmissions')
  # plt.legend()
  if savefig:
    plt.savefig(output_file)
    plt.close()
  else:
    plt.show()

def slot_frame_length_graph(input_params, curves_names, output_file="slot_frame_lenght_graph.pdf", title="Benefit of concurrent communications", yticks=None):
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
  plt.xlabel('Number of cells in the network')
  plt.ylabel('Lenght of the resulting slotframe')
  plt.title(title)
  plt.legend()
  plt.grid(color='tab:grey', linestyle='--', linewidth=1, alpha=0.3)
  if yticks !=None:
    plt.yticks(yticks)

  # plt.show()
  plt.savefig(output_file)
  plt.close()

def positionning_frequency_graph(input_params, curves_names, output_file="positionning_frequency_graph.pdf", title="Frequency of positioning", timeslot_duration=5, savefig=True, legendcol = 1):
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
  plt.xlabel('Number of cells in the network')
  plt.ylabel('Localisation update (Hz)')
  plt.grid(color='tab:grey', linestyle='--', linewidth=1, alpha=0.3)
  plt.title(title)
  plt.legend(ncol=legendcol)
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
    nb_comm = range(0, 2000)
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

def positionning_frequency_bars(input_csv_file, output_file="positionning_frequency_bars.pdf", title="Frequency of positioning", timeslot_duration=5, savefig=True):
  """Generate plot graph based on the schedule stat
  param timeslot_duration is in ms
  """
  fig, ax = plt.subplots()

  bar_x = []
  bar_height = []
  bar_tick_label = []
  bar_label = []
  i = 1
  parameters = Bunch_Parameters.get_parameters_from_file(input_csv_file)
  for param in parameters:
    stat = scheduling.import_schedule_stat(param.directory + "schedule_stat.csv")

    bar_x.append(i)
    frequency = 1000.0/(int(stat["len_schedule"])*timeslot_duration)
    bar_height.append(round(1000.0/(int(stat["len_schedule"])*timeslot_duration),2))
    bar_tick_label.append(str(param.name))
    i+=1
  bar_label = bar_height

  bar_plot = plt.bar(bar_x,bar_height,tick_label=bar_tick_label)

  def autolabel(rects):
    """ add text to describe the height of the bar plot """
    max_height = max(bar_height)
    for idx,rect in enumerate(bar_plot):
      height = rect.get_height()
      if height > (max(bar_height) / 4):
        ax.text(rect.get_x() + rect.get_width()/2., .3*height,
                bar_label[idx],
                ha='center', va='top', rotation=90)
      else:
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                bar_label[idx],
                ha='center', va='bottom', rotation=90)

  autolabel(bar_plot)

  def autolabel_text(rects):
    max_height = max(bar_height)
    for idx,rect in enumerate(bar_plot):
      height = rect.get_height()
      if height > (max(bar_height) / (2./3)):
        ax.text(rect.get_x() + rect.get_width()/2., 0.5,
              "\\textbf{" + bar_tick_label[idx] + "}",
              ha='center', va='bottom', rotation=90)
      else:
        ax.text(rect.get_x() + rect.get_width()/2., .95*max_height,
              "\\textbf{" + bar_tick_label[idx] + "}",
              ha='center', va='top', rotation=90)

  autolabel_text(bar_plot)
  plt.ylim(0,max(bar_height))

  plt.ylabel('Localisation update (Hz)')
  plt.title(title)
  plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off') # labels along the bottom edge are off
  # plt.legend()
  if savefig:
    plt.savefig(output_file)
    plt.close()
  else:
    plt.show()

if __name__ == '__main__':
  gen_graphs_from_file("./example/bunch/var_agreg/")
  gen_graphs_from_file("./example/bunch/var_channels/")
