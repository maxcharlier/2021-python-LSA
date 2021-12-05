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
import matplotlib.patches as mpatches

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

  plt.xlabel('Network size')
  plt.ylabel('Number of transmissions')
  plt.legend()
  if savefig:
    plt.savefig(output_file)
    plt.close()
  else:
    plt.show()

def plot_path_length(param_best, param_worst, output_file="path_length.pdf", savefig=True):
  """Generate the number of hop according to the network size
  Best use case when the sink is in the center of the grid
  Worst when the sink is in a corner"""

  fig, axs = plt.subplots(2)
  legend_handles = []

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
  
  # # Creating legend for the means curve
  # legend_handles = []
  # legend_handles.append(Line2D([0], [0], color='tab:grey', label="Means", linestyle='--'))
  # axs[0].legend(handles=legend_handles, loc="lower right", bbox_to_anchor=(1, 1.04))

  plt.xticks(range(0, 401, 50), range(0, 401, 50), rotation=0)
  plt.xlabel('Network size')
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

def slot_frame_length_graph(input_params, curves_names, output_file="slot_frame_length_graph.pdf", title="Benefit of concurrent communications", yticks=None, timeslot_duration = 5, curves_markers = None, alpha=1.0, legendcol=1, curves_colors=None):
  """Generate plot graph based on the schedule stat"""
  fig, ax1 = plt.subplots()
  for i in range(len(input_params)):
    len_schedule = []
    nb_tags = []
    parameters = Bunch_Parameters.get_parameters_from_file(input_params[i])
    for param in parameters:
      stat = scheduling.import_schedule_stat(param.directory + "schedule_stat.csv")
      len_schedule.append(int(stat["len_schedule"]))
      nb_tags.append(int(stat["nb_tags"]))
      if curves_colors != None:
        color = curves_colors[i]
      else:
        color= None
    if curves_markers != None : 
      ax1.plot(nb_tags, len_schedule, label=curves_names[i], alpha=alpha, marker=curves_markers[i], c=color)
    else:
      ax1.plot(nb_tags, len_schedule, label=curves_names[i], alpha=alpha, marker=".", c=color)
    if curves_colors != None:
      ax1.plot(nb_tags, len_schedule, alpha=0.3, marker=",", linestyle='dotted', color='black')

  plt.xlabel('Network size')
  ax1.set_ylabel('Slotframe length')

  plt.title(title)
  plt.legend(ncol=legendcol)
  ax1.grid(color='tab:grey', linestyle='--', linewidth=1, alpha=0.3)
  if yticks !=None:
    plt.yticks(yticks)

  if(timeslot_duration != 0):
    #generate second axis
    ax2 = ax1.twinx()
    factor = float(timeslot_duration)/1000
    print("slot_frame_length_graph factor : " + str(factor))
    mn, mx = ax1.get_ylim()
    print((mx, mx*factor))
    # ax1.set_ylim(0, mx)
    ax2.set_ylim(mn*factor, mx*factor)
    ax2.set_ylabel("Slotframe duration (s) at 6.8 Mb/s")


  # plt.show()
  plt.savefig(output_file)
  plt.close()

def schedule_duration_graph(input_params, curves_names, output_file="schedule_duration_graph.pdf", title="Computation duration of the Scheduling", yticks=None, curves_markers = None, alpha=1.0, legendcol=1, curves_colors=None, repeat=1):
  """Generate plot graph based on the schedule stat"""
  fig, ax1 = plt.subplots()
  for i in range(len(input_params)):
    durations = []
    nb_tags = []
    parameters = Bunch_Parameters.get_parameters_from_file(input_params[i])
    for param in parameters:
      duration =0
      nb_tag = 0
      for repeat_i in range(repeat):
        if repeat_i > 0 :
          current_directory = param.directory.replace("result", "result"+str(repeat_i))
        else:
          current_directory = param.directory
        stat = scheduling.import_schedule_stat(current_directory + "schedule_stat.csv")
        duration += float(stat["duration"])
        nb_tag = int(stat["nb_tags"])
        print("nb_tag "+str(nb_tag) + " duration " + str(duration))
      durations.append(duration/repeat)
      nb_tags.append(nb_tag)
    if curves_colors != None:
      color = curves_colors[i]
    else:
      color= None
    if curves_markers != None : 
      ax1.plot(nb_tags, durations, label=curves_names[i], alpha=alpha, marker=curves_markers[i], c=color)
    else:
      ax1.plot(nb_tags, durations, label=curves_names[i], alpha=alpha, marker=".", c=color)
    if curves_colors != None:
      ax1.plot(nb_tags, durations, alpha=0.3, marker=",", linestyle='dotted', color='black')
  plt.xlabel('Network size')
  if repeat ==1:
    ax1.set_ylabel('Computation time (s)')
  else:
    ax1.set_ylabel('Means computation time (s)')

  plt.title(title)
  plt.legend(ncol=legendcol)
  ax1.grid(color='tab:grey', linestyle='--', linewidth=1, alpha=0.3)
  if yticks !=None:
    plt.yticks(yticks)

  # plt.show()
  plt.savefig(output_file)
  plt.close()

def positionning_frequency_graph(input_params, curves_names, output_file="positionning_frequency.pdf", title="Frequency of positioning", timeslot_duration=5, savefig=True, legendcol = 1, curves_markers = None, alpha= 1.0, curves_colors=None):
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
    if curves_colors != None:
      color = curves_colors[i]
    else:
      color= None
    if curves_markers != None : 
      plt.plot(nb_tags, len_schedule, label=curves_names[i], alpha=alpha, marker=curves_markers[i], color=color)
    else:
      plt.plot(nb_tags, len_schedule, label=curves_names[i], alpha=alpha, marker=".", color=color)
    if curves_colors != None:
      plt.plot(nb_tags, len_schedule, alpha=0.3, marker=",", linestyle='dotted', color='black')
  plt.xlabel('Network size')
  plt.ylabel('Localization update (Hz)')
  plt.grid(color='tab:grey', linestyle='--', linewidth=1, alpha=0.3)
  plt.title(title)
  plt.legend(ncol=legendcol)
  if savefig:
    plt.savefig(output_file)
    plt.close()
  else:
    plt.show()

type_of_curve = ["Communication per channels", "Aggregation per channels", "Communication per timeslot", "Aggregation per timeslot"]

def plot_slotframe_distrib(input_csv_file, file="plot_slotframe_stepdistrib.pdf", type_of_curve_index=0, cumulative=True):
  """ Plot the number of communications per cells"""

  plt.title("Slotframe Communications distribution - " + type_of_curve[type_of_curve_index])
  # plt.gca().set_xscale('log')
  parameters = Bunch_Parameters.get_parameters_from_file(input_csv_file)
  for param in parameters:
    _topology = topology.Topology.import_param(param.directory + "/topology_param.csv")
    _topology.import_nodes(param.directory + "/nodes.csv")
    schedule = scheduling.import_schedule(param.directory + "schedule.csv", _topology.nodes)

    #channel counter
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
      # plt.plot(nb_comm, convert_to_pourcent(t_comm_all)[0:len(nb_comm)], drawstyle='steps-post', label=param.name)
      plt.step(nb_comm, convert_to_pourcent(t_comm_all)[0:len(nb_comm)], where='post', label=param.name)
    else:
      nb_comm = range(0, get_max_comm(t_weight_all))
      plt.plot(nb_comm, convert_to_pourcent(t_weight_all)[0:len(nb_comm)], drawstyle='steps-post', label=param.name)


  plt.legend()

  plt.savefig(file)
  plt.close()

def plot_timeslot_distrib(input_csv_file, file="plot_timeslot_distrib.pdf", cumulative=True, title="", max_ch=8, uniform_X_axis = True, legend="Disruption"):
  """ Plot the number of communications per timeslot"""

  fig, axs = plt.subplots(3)
  parameters = Bunch_Parameters.get_parameters_from_file(input_csv_file)
  legend_handles = []
  x =  []
  overall_tot_comm = 0
  overall_max_comm = 0
  for param in parameters:
    _topology = topology.Topology.import_param(param.directory + "/topology_param.csv")
    _topology.import_nodes(param.directory + "/nodes.csv")
    schedule = scheduling.import_schedule(param.directory + "schedule.csv", _topology.nodes)
    #travel the slotframe and for each timeslot number count:
    #the total number of communication
    #the number of channel used

    #generate the x axis and table according to the slotframe length:
    stat = scheduling.import_schedule_stat(param.directory + "schedule_stat.csv")
    length = int(stat["len_schedule"])
    if uniform_X_axis : 
      x = [float(i)/length for i in range(0, length)]
    else:
      x = range(0, length)
    nb_comm = [0 for i in range(0, length)]
    nb_weight = [0 for i in range(0, length)]
    max_comm = [0 for i in range(0, length)]
    nb_channel = [0 for i in range(0, length)]
    t = 0
    for timeslot in schedule:
      t_comm = 0
      t_weight = 0
      for channel in timeslot:
        for link in channel:
          t_weight += link.weight
        t_comm += len(channel)
        if len(channel) > max_comm[t]:
          max_comm[t] = len(channel)
      nb_comm[t] = t_comm
      nb_weight[t] = t_weight
      nb_channel[t] = len(timeslot)
      t+=1
    if max(nb_comm) > overall_tot_comm:
      overall_tot_comm = max(nb_comm)
    linewidth = 0.3
    if max(max_comm) > overall_max_comm:
      overall_max_comm = max(max_comm)
    linewidth = 0.3
    marker=''
    curve = axs[0].plot(x, nb_comm, linestyle='solid', marker=marker, markersize=0.5, alpha=0.7, linewidth=linewidth)

    color = curve[0].get_color()
    axs[1].plot(x, max_comm, linestyle='solid', marker=marker, markersize=0.5, alpha=0.7, linewidth=linewidth, color=color)
    axs[2].plot(x, nb_channel, linestyle='solid', marker=marker, markersize=0.5, alpha=0.7, color=color, linewidth=linewidth)

    if legend == "Disruption":
      # Creating legend with color box
      legend_handles.append(mpatches.Patch(color=color, label=param.disruption_range, alpha=0.7))
    elif legend == "Channel":
      # Creating legend with color box
      legend_handles.append(mpatches.Patch(color=color, label=param.nb_ch, alpha=0.7))

  axs[0].set_ylabel("Total \# of \nTransmissions")
  axs[1].set_ylabel("Max \# of \nTransmissions\nOn one channel")
  axs[2].set_ylabel("\# of channels \nused")
  axs[2].set_yticks(range(1, max_ch+1))

  axs[0].set_xticklabels(['' for i in range(0, len(x)+1, 200)])
  axs[0].set_xticks(range(0, len(x)+1, 200))
  axs[0].set_yticks(range(0, overall_tot_comm+1, 50))
  axs[1].set_xticklabels(['' for i in range(0, len(x)+1, 200)])
  axs[1].set_yticks(range(0, overall_max_comm+1, 10))
  axs[1].set_xticks(range(0, len(x)+1, 200))
  axs[2].set_xticks(range(0, len(x)+1, 200))


  plt.xlabel("Timeslot index")

  if len(title) >0:
    axs[0].set_title(title)
  if legend == "Disruption":
    axs[0].legend(title="Interference range :", ncol=3, handles=legend_handles)
  elif legend == "Channel":
    axs[0].legend(title="Number of channels :", ncol=3, handles=legend_handles)

  # plt.tight_layout()
  # plt.savefig(file)
  # plt.savefig(file, format='jpeg')
  plt.show()
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

def slotframe_length_bars(input_csv_file, output_file="slotframe_length_bars.pdf", title="Slotframe length", savefig=True, display_xlabels=True, timeslot_duration=0):
  """Generate plot graph based on the schedule stat
  param timeslot_duration is in ms for a bit-rate of 6.8 mbps
  """
  fig, ax = plt.subplots()

  bar_x = []
  bar_height = []
  bar_tick_label = []
  bar_in_label = []
  bar_x_labels = []
  i = 1
  parameters = Bunch_Parameters.get_parameters_from_file(input_csv_file)
  for param in parameters:
    stat = scheduling.import_schedule_stat(param.directory + "schedule_stat.csv")

    bar_x.append(i)
    bar_height.append(int(stat["len_schedule"]))
    bar_x_labels.append(int(param.nb_sink))
    bar_tick_label.append(str(param.name))
    i+=1
  bar_in_label = bar_height

  bar_plot = plt.bar(bar_x,bar_height,tick_label=bar_tick_label)

  def add_label_inside_bar(rects):
    """ add text to describe the height of the bar plot """
    max_height = max(bar_height)
    for idx,rect in enumerate(bar_plot):
      height = rect.get_height()
      if height > (max(bar_height) / 4):
        ax.text(rect.get_x() + rect.get_width()/2., .3*height,
                bar_in_label[idx],
                ha='center', va='top', rotation=90)
      else:
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                bar_in_label[idx],
                ha='center', va='bottom', rotation=90)

  add_label_inside_bar(bar_plot)

  def text_on_top(rects):
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


  def set_x_ticks_value(rects, x_labels):
    plt.xlabel('Number of sinks')
    x_ticks_value = []
    for idx,rect in enumerate(bar_plot):
      x_ticks_value.append(rect.get_x() + rect.get_width()/2.)
    plt.xticks(x_ticks_value, x_labels)

  if display_xlabels:
    set_x_ticks_value(bar_plot, bar_x_labels)
  else:
    #disable x label
    text_on_top(bar_plot)
    plt.tick_params(
      axis='x',          # changes apply to the x-axis
      which='both',      # both major and minor ticks are affected
      bottom='off',      # ticks along the bottom edge are off
      top='off',         # ticks along the top edge are off
      labelbottom='off') # labels along the bottom edge are off

  plt.ylim(0,max(bar_height))

  plt.ylabel('Slotframe length')
  plt.title(title)
  
  if(timeslot_duration != 0):
    #generate second axis
    ax2 = ax.twinx()
    factor = float(timeslot_duration)/1000
    print("slot_frame_length_graph factor : " + str(factor))
    mn, mx = ax.get_ylim()
    print((mx, mx*factor))
    # ax1.set_ylim(0, mx)
    ax2.set_ylim(mn*factor, mx*factor)
    ax2.set_ylabel("Slotframe duration (s) at 6.8 Mb/s")

  plt.grid(color='tab:grey', linestyle='--', linewidth=1, alpha=0.3)

  # plt.legend()
  if savefig:
    plt.savefig(output_file)
    plt.close()
  else:
    plt.show()

def plot_max_queue_size(input_params, curves_names, output_file="plot_max_queue_size.pdf", title="Maximum queue size", savefig=True, yticks=None, curves_markers = None, alpha=1.0, legendcol=2, curves_colors=None):
  """Plot the maximum queue size according to the size of the network"""
  """Generate plot graph based on the schedule stat"""

  matplotlib.rcParams.update({'font.size': 35})

  fig, ax1 = plt.subplots(figsize=(10,8))
  # fig, ax1 = plt.subplots()
  for i in range(len(input_params)):
    queue_sizes = []
    nb_tags = []
    parameters = Bunch_Parameters.get_parameters_from_file(input_params[i])
    for param in parameters:
      stat = scheduling.import_schedule_stat(param.directory + "schedule_stat.csv")
      topology_ = topology.Topology.import_param(param.directory + "topology_param.csv")
      topology_.import_nodes(param.directory + "nodes.csv")
      queue_size = scheduling.import_queue_sizes(param.directory + "schedule.csv", topology_.nodes, param.aggregation)

      queue_sizes.append(queue_size)
      nb_tags.append(int(stat["nb_tags"]))
      if curves_colors != None:
        color = curves_colors[i]
      else:
        color= None
    if curves_markers != None : 
      ax1.plot(nb_tags, queue_sizes, label=curves_names[i], alpha=alpha, marker=curves_markers[i], c=color)
    else:
      ax1.plot(nb_tags, queue_sizes, label=curves_names[i], alpha=alpha, marker=".", c=color, markersize=15)
    if curves_colors != None:
      ax1.plot(nb_tags, queue_sizes, alpha=0.3, marker=",", linestyle='dotted', color='black')

  plt.xlabel('Network size')
  ax1.set_ylabel('Maximum queue depth \\\\during the slotframe')

  plt.title(title)
  # plt.legend(ncol=legendcol)
  # plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.04), shadow=True, ncol=4)

  plt.xticks(range(0, 401, 50))
  ax1.grid(color='tab:grey', linestyle='--', linewidth=1, alpha=0.3)

  if yticks !=None:
    print(yticks)
    plt.yticks(yticks, yticks)


  # plt.show()
  plt.tight_layout()
  plt.savefig(output_file)
  plt.close()
      

def schedule_duration_bars(input_csv_file, output_file="schedule_duration_bars.pdf", title="Computation duration of the Scheduling",  savefig=True, display_xlabels=True, repeat=1,max_duration=0):
  """Generate plot graph based on the schedule stat"""
  fig, ax = plt.subplots()

  bar_x = []
  bar_height = []
  bar_tick_label = []
  bar_in_label = []
  bar_x_labels = []
  i = 1
  parameters = Bunch_Parameters.get_parameters_from_file(input_csv_file)

  for param in parameters:
    stat = scheduling.import_schedule_stat(param.directory + "schedule_stat.csv")
    duration =0
    for repeat_i in range(repeat):
      if repeat_i > 0 :
        current_directory = param.directory.replace("result", "result"+str(repeat_i))
      else:
        current_directory = param.directory
      stat = scheduling.import_schedule_stat(current_directory + "schedule_stat.csv")
      duration += float(stat["duration"])
    bar_x.append(i)
    bar_height.append(round(duration/repeat,2))
    bar_x_labels.append(int(param.nb_sink))
    bar_tick_label.append(str(param.name))
    i+=1
  bar_in_label = bar_height

  bar_plot = plt.bar(bar_x,bar_height,tick_label=bar_tick_label)

  def add_label_inside_bar(rects):
    """ add text to describe the height of the bar plot """
    max_height = max(bar_height)
    for idx,rect in enumerate(bar_plot):
      height = rect.get_height()
      if height > (max(bar_height) / 4):
        ax.text(rect.get_x() + rect.get_width()/2., .3*height,
                bar_in_label[idx],
                ha='center', va='top', rotation=90)
      else:
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                bar_in_label[idx],
                ha='center', va='bottom', rotation=90)

  add_label_inside_bar(bar_plot)

  def text_on_top(rects):
    max_height = max(max(bar_height), max_duration)
    for idx,rect in enumerate(bar_plot):
      height = rect.get_height()
      # if height > (max(bar_height) / (2./3)):
      #   ax.text(rect.get_x() + rect.get_width()/2., 0.5,
      #         "\\textbf{" + bar_tick_label[idx] + "}",
      #         ha='center', va='bottom', rotation=90)
      # else:
      ax.text(rect.get_x() + rect.get_width()/2., .95*max_height,
              "\\textbf{" + bar_tick_label[idx] + "}",
              ha='center', va='top', rotation=90)


  

  def set_x_ticks_value(rects, x_labels):
    plt.xlabel('Number of sinks')
    x_ticks_value = []
    for idx,rect in enumerate(bar_plot):
      x_ticks_value.append(rect.get_x() + rect.get_width()/2.)
    plt.xticks(x_ticks_value, x_labels)

  if display_xlabels:
    set_x_ticks_value(bar_plot, bar_x_labels)
  else:
    #disable x label
    text_on_top(bar_plot)
    plt.tick_params(
      axis='x',          # changes apply to the x-axis
      which='both',      # both major and minor ticks are affected
      bottom='off',      # ticks along the bottom edge are off
      top='off',         # ticks along the top edge are off
      labelbottom='off') # labels along the bottom edge are off

  if max_duration == 0:
    plt.ylim(0,max(bar_height))
  else:
    plt.ylim(0,max_duration)


  if repeat ==1:
    plt.ylabel('Computation duration of the Scheduling (s)')
  else:
    plt.ylabel('Means computation duration of the Scheduling (s)')

  plt.title(title)

  # plt.legend()
  if savefig:
    plt.savefig(output_file)
    plt.close()
  else:
    plt.show()

if __name__ == '__main__':
  gen_graphs_from_file("./example/bunch/var_agreg/")
  gen_graphs_from_file("./example/bunch/var_channels/")

