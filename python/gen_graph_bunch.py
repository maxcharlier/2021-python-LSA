import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from nodes.anchor import Anchor
from nodes.tag import Tag
from nodes.point import Point
import os
import scheduling

from export_bunch import Bunch_Parameters

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

def slot_frame_lenght_graph(input_params, curves_names, output_file="stat_graph.pdf"):
  """Generate plot graph based on the schedule stat"""
  for i in range(len(input_params)):
    len_schedule = []
    nb_tags = []
    parameters = Bunch_Parameters.get_parameters_from_file(input_params[i])
    for param in parameters:
      stat = scheduling.import_schedule_stat(param.directory + "schedule_stat.csv")
      len_schedule.append(int(stat["len_schedule"]))
      nb_tags.append(int(stat["nb_tags"]))
    plt.plot(nb_tags, len_schedule, label=curves_names[i])

  title="Benefit of concurrent communications and agregation"
  plt.title(title)
  plt.legend()

  plt.savefig(output_file)
  plt.close()



if __name__ == '__main__':
  gen_graphs_from_file("./example/bunch/var_agreg/")
  gen_graphs_from_file("./example/bunch/var_channels/")
