from abc import ABC
import matplotlib
import matplotlib.pyplot as plt
import sys 
import os
sys.path.append('../../../')
import numpy as np
from export_bunch import gen_topology
from export_bunch import Bunch_Parameters
import scheduling
import topology
import graphics

dir_path = os.path.dirname(os.path.realpath(__file__))

def slotframe_length_bars_aggreg(input_csv_file_ag1,input_csv_file_ag14, \
  output_file="slotframe_length_bars.pdf", title="Slotframe length", \
  savefig=True, timeslot_duration=0):
  """Generate graph bar of the schedule length base on the schedule stat
  param timeslot_duration is in ms for a bit-rate of 6.8 mbps
  """
  fig, ax = plt.subplots()



  parameters_ag1 = Bunch_Parameters.get_parameters_from_file(input_csv_file_ag1)
  parameters_ag14 = Bunch_Parameters.get_parameters_from_file(input_csv_file_ag14)

  if len(parameters_ag1) != len(parameters_ag14):
    raise Exception("The two csv file need to defind the same number of configuration")

  bars_x = np.arange(1, len(parameters_ag1)+1) #center position of each bar ticks
  schedule_length_ag1 = [] #schedule length of each configuration
  schedule_length_ag14 = []
  nb_sinks = [] #number of sink disply as x label

  bar_width = 0.35

  for param in parameters_ag1:
    stat = scheduling.import_schedule_stat(param.directory + "schedule_stat.csv")
    schedule_length_ag1.append(int(stat["len_schedule"]))
    nb_sinks.append(int(param.nb_sink))

  bar_plot_ag1 = plt.bar(bars_x - bar_width/2, schedule_length_ag1, bar_width, label="Aggreg 1")

  for param in parameters_ag14:
    stat = scheduling.import_schedule_stat(param.directory + "schedule_stat.csv")
    schedule_length_ag14.append(int(stat["len_schedule"]))

  bar_plot_ag14 = plt.bar(bars_x + bar_width/2, schedule_length_ag14, bar_width, label="Aggreg 14")

  def add_label_inside_bar(bar_plot, label, max_y_value):
    """ add text to describe the height of the bar plot """
    for idx,rect in enumerate(bar_plot):
      height = rect.get_height()
      if height > (max_y_value / 4):
        ax.text(rect.get_x() + rect.get_width()/2., .3*height,
                label[idx],
                ha='center', va='top', rotation=90)
      else:
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                label[idx],
                ha='center', va='bottom', rotation=90)

  def add_factor_inside_bar(bar_plot, label, max_y_value):
    """ add text to describe the height of the bar plot """
    for idx,rect in enumerate(bar_plot):
        ax.text(rect.get_x() + rect.get_width()/2., 0.8*max_y_value,
                label[idx],
                ha='center', va='top', rotation=90)


  max_y_value = max(max(schedule_length_ag1), max(schedule_length_ag14))
  add_label_inside_bar(bar_plot_ag1, schedule_length_ag1, max_y_value)
  add_label_inside_bar(bar_plot_ag14, schedule_length_ag14, max_y_value)
  # add_factor_inside_bar(bar_plot_ag1, schedule_length_ag1-schedule_length_ag14, max_y_value)
  add_factor_inside_bar(bar_plot_ag14, ["Reduction factor : " +str(round(schedule_length_ag1[i]/schedule_length_ag14[i],2)) for i in range(len(schedule_length_ag14))], max_y_value)


  plt.legend(["Aggreg 1", "Aggreg 14"], loc=1)

  for x in bars_x:
    plt.plot([x+0.5,x+0.5], [0, max_y_value], color='tab:grey', linestyle='--', linewidth=1, alpha=0.3)

  plt.xlabel('Number of sinks')
  plt.xticks(bars_x, nb_sinks)

  plt.ylim(0,max_y_value)

  plt.ylabel('Slotframe length')
  if title != '':
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

  if savefig:
    plt.savefig(output_file)
    plt.close()
  else:
    plt.show()

gen_topology(Bunch_Parameters.get_parameters_from_file(dir_path + "/topology_param_var_sinks_agreg1.csv"), plot_graph=False)
gen_topology(Bunch_Parameters.get_parameters_from_file(dir_path + "/topology_param_var_sinks_agreg14.csv"), plot_graph=False)
slotframe_length_bars_aggreg(dir_path + "/topology_param_var_sinks_agreg1.csv", dir_path + "/topology_param_var_sinks_agreg14.csv", \
          output_file="schedule_length_bars_sinks_agreg.pdf", title="", savefig=True, timeslot_duration=5)
