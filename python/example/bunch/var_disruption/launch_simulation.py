from abc import ABC
import sys 
import os
sys.path.append('../../../')
from export_bunch import gen_topology
from gen_graph_bunch import slot_frame_length_graph
from gen_graph_bunch import positionning_frequency_graph
from gen_graph_bunch import positionning_frequency_bars
from gen_graph_bunch import plot_timeslots_usage
from gen_graph_bunch import gen_graphs_from_file
from gen_graph_bunch import plot_slotframe_distrib
from gen_graph_bunch import plot_slotframe_channels_usage
from export_bunch import Bunch_Parameters
import scheduling
import topology
import graphics
import matplotlib
import matplotlib.pyplot as plt

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
input_params = []
output_file=dir_path + "/slot_frame_length_graph.pdf"

input_params.append(dir_path + "/topology_param.csv")

# for file in input_params:
#   gen_topology(Bunch_Parameters.get_parameters_from_file(file), plot_graph=False)

# slot_frame_length_graph(input_params, curves_names, output_file, title="")
# plot_timeslots_usage(input_params, curves_names, savefig=True)
# positionning_frequency_graph(input_params, curves_names, title="", savefig=False)
positionning_frequency_bars(input_params[0], title="", savefig=True)
def channel_reuse(input_csv_file, output_file="channel_reuse.pdf", title="Channel reuse", savefig=True):
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
    frequency = (1.0*int(stat["nb_ch"]))/int(stat["len_schedule"])
    bar_height.append(round(frequency,2))
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
  plt.ylim(0,8)

  plt.ylabel('Mean concurrent channels usage')
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
channel_reuse(input_params[0], title="", savefig=True)

# plot_slotframe_distrib(dir_path + "/plot_slotframe_distrib.csv", file="plot_slotframe_distrib_0.pdf", type_of_curve_index=0, cumulative=False)
# plot_slotframe_distrib(dir_path + "/plot_slotframe_distrib.csv", file="plot_slotframe_distrib_1.pdf", type_of_curve_index=1, cumulative=False)
# plot_slotframe_distrib(dir_path + "/plot_slotframe_distrib.csv", file="plot_slotframe_distrib_2.pdf", type_of_curve_index=2, cumulative=False)
# plot_slotframe_distrib(dir_path + "/plot_slotframe_distrib.csv", file="plot_slotframe_distrib_3.pdf", type_of_curve_index=3, cumulative=False)
# plot_slotframe_distrib(dir_path + "/plot_slotframe_distrib.csv", file="plot_slotframe_distrib_cumulative_0.pdf", type_of_curve_index=0, cumulative=True)
# plot_slotframe_distrib(dir_path + "/plot_slotframe_distrib.csv", file="plot_slotframe_distrib_cumulative_1.pdf", type_of_curve_index=1, cumulative=True)
# plot_slotframe_distrib(dir_path + "/plot_slotframe_distrib.csv", file="plot_slotframe_distrib_cumulative_2.pdf", type_of_curve_index=2, cumulative=True)
# plot_slotframe_distrib(dir_path + "/plot_slotframe_distrib.csv", file="plot_slotframe_distrib_cumulative_3.pdf", type_of_curve_index=3, cumulative=True)
# plot_slotframe_channels_usage(dir_path + "/plot_slotframe_distrib.csv", file="plot_slotframe_channels_usage.pdf", nb_channel_max=8, cumulative=True)

