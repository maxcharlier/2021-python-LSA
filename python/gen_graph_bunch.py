import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from nodes.anchor import Anchor
from nodes.tag import Tag
from nodes.point import Point
import os
import scheduling

from export_bunch import Bunch_Parameters

def gen_graphs_from_file(result_directory, input_param="toplogy_param.csv", output_file="stat_graph.pdf"):
  """Generate plot graph based on the schedule stat"""
  param = Bunch_Parameters.get_param_from_file(result_directory+input_param)
  title=param.get_str_variable_parameter()
  variable = param.get_variable_parameter()
  print(variable)
  duration = []
  len_schedule= []
  nb_slot = []
  nb_twr = []
  nb_data = []
  agregation_ = []
  nb_ch_ = []

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
                        stat = scheduling.import_schedule_stat(param.directory + current_directory + "schedule_stat.csv")
                        duration.append(float(stat["duration"]))
                        len_schedule.append(int(stat["len_schedule"]))
                        nb_slot.append(int(stat["nb_slot"]))
                        nb_twr.append(int(stat["nb_twr"]))
                        nb_data.append(int(stat["nb_data"]))
                        agregation_.append(int(stat["agregation"]))
                        nb_ch_.append(int(stat["nb_ch"]))
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



if __name__ == '__main__':
  gen_graphs_from_file("./example/bunch/var_agreg/")
  gen_graphs_from_file("./example/bunch/var_channels/")
