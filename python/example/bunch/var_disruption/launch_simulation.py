from abc import ABC
import sys 
import os
sys.path.append('../../../')
from export_bunch import gen_topology
from gen_graph_bunch import positionning_frequency_bars
from gen_graph_bunch import plot_slotframe_distrib
from gen_graph_bunch import plot_timeslot_distrib
from export_bunch import Bunch_Parameters
import scheduling
import topology
import graphics
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import csv
import math


def bar_graph(input_csv_file, disruption_distances, output_file="channel_reuse.pdf", title="Channel reuse", savefig=True, max_ch=8,  timeslot_duration=0, plt_ax=None, plot_legend=True):
  """Generate plot graph based on the schedule stat
  param timeslot_duration is in ms
  """
  if(plt_ax == None):
    fig, ax = plt.subplots()
  else:
    ax = plt_ax

  bar_x = []
  bar_height = []
  bar_tick_label = []
  bar_color = []
  bar_label = []
  i = 1
  with open(input_csv_file) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      stat = scheduling.import_schedule_stat(str(row['directory']) + "schedule_stat.csv")

      bar_x.append(i)
      if(timeslot_duration > 0):
        # frequency = 1000.0/(int(stat["len_schedule"])*timeslot_duration)
        # bar_height.append(round(1000.0/(int(stat["len_schedule"])*timeslot_duration),2))
        bar_height.append(int(stat["len_schedule"]))
      else:
        frequency = (1.0*int(stat["nb_ch"]))/int(stat["len_schedule"])
        bar_height.append(round(frequency,3))
      bar_tick_label.append(str(row['name']))
      bar_color.append(str(row['color']))
      i+=1
  bar_label = bar_height
  nb_bar = i-1
  bar_plot = ax.bar(bar_x,bar_height,tick_label=bar_tick_label, color=bar_color)

  def autolabel(rects):
    """ add text to describe the height of the bar plot """
    max_height = max(bar_height)
    for idx,rect in enumerate(bar_plot):
      height = rect.get_height()
      ax.text(rect.get_x() + rect.get_width()/2.,max_height/20,
                bar_label[idx],
                ha='center', va='bottom', rotation=90)

  autolabel(bar_plot)


  if timeslot_duration == 0:
    ax.set_ylim(0,max_ch)
    ax.set_ylabel('Mean concurrent \n Channels usage')
  else:
    ax.set_ylabel('Schedule length (Hz)')


  #set a fixed legends
  if plot_legend:
    legends_colors= ['tab:blue', 'tab:orange', 'tab:green']
    legends_label = ["208 cells", "400 cells", "625 cells"]
    legends_patches= []
    for i in range(len(legends_label)):
      legends_patches.append(mpatches.Patch(color=legends_colors[i], label=legends_label[i]))
    ax.legend(handles=legends_patches)

  plt.title(title)

  #ticks parameter
  nb_group = len(disruption_distances)
  offset_group = nb_bar/nb_group
  x = [(offset_group/2)+0.5+ i*offset_group  for i in range(0, nb_group)]
  ax.set_xticks(x)
  ax.set_xticklabels(disruption_distances)
  # plt.tick_params(
  #   axis='x',          # changes apply to the x-axis
  #   which='both',      # both major and minor ticks are affected
  #   bottom='on',      # ticks along the bottom edge are off
  #   top='off',         # ticks along the top edge are off
  #   labelbottom='on') # labels along the bottom edge are off

  plt.xlabel("Disruption range")

  #add diverder between group of bar
  y_max=ax.get_ylim()[1]
  for i in range(nb_group):
    x=math.ceil((i+1) * offset_group)+0.5
    ax.plot([x, x], [0, y_max], linestyle='dotted', color="grey")

  if plt_ax == None:
    if savefig:
      plt.savefig(output_file)
      plt.close()
    else:
      plt.show()


def sub_lot_bar(input_params, disruption_distances, output_file, timeslot_duration, max_ch):
  fig, axs = plt.subplots(2)
  bar_graph(input_params, disruption_distances, title="", timeslot_duration=timeslot_duration, plt_ax=axs[0])
  bar_graph(input_params, disruption_distances, title="", plt_ax=axs[1], max_ch=max_ch, plot_legend=False)

  plt.savefig(output_file)
  plt.close()
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
input_params = []
output_file=dir_path + "/slot_frame_length_graph.pdf"

input_params.append(dir_path + "/topology_param_ch8.csv")

# for file in input_params:
#   gen_topology(Bunch_Parameters.get_parameters_from_file(file), plot_graph=False)




# bar_graph(input_params[0], [2, 3, 4, 10, 30], output_file="channel_reuse_ch8.pdf", title="", savefig=True)
# bar_graph(input_params[0], [2, 3, 4, 10, 30], output_file="positionning_frequency_bars_ch8.pdf", title="", savefig=True, timeslot_duration=5)
# sub_lot_bar(input_params[0], [2, 3, 4, 10, 30], output_file="bar_graph_ch8.pdf", timeslot_duration=5, max_ch=8)


input_params = [dir_path + "/topology_param_4ch.csv"]


# for file in input_params:
#   gen_topology(Bunch_Parameters.get_parameters_from_file(file), plot_graph=False)

# bar_graph(input_params[0], [2, 3, 4, 10, 30], output_file="channel_reuse_ch4.pdf", title="", savefig=True, max_ch=4)
# bar_graph(input_params[0], [2, 3, 4, 10, 30], output_file="positionning_frequency_bars_ch4.pdf", title="", savefig=True, max_ch=4, timeslot_duration=5)
# sub_lot_bar(input_params[0], [2, 3, 4, 10, 30], output_file="bar_graph_ch4.pdf", timeslot_duration=5, max_ch=4)

input_params = [dir_path + "/topology_param_ch8_400.csv"]
# plot_slotframe_distrib(input_params[0], file="plot_slotframe_ch8-400_cells-coms_per_channel.pdf", type_of_curve_index=0, cumulative=True)
# plot_slotframe_distrib(input_params[0], file="plot_slotframe_ch8-400_cells-aggreg_per_channel.pdf", type_of_curve_index=1, cumulative=True)
# plot_slotframe_distrib(input_params[0], file="plot_slotframe_ch8-400_cells-coms_per_timeslot.pdf", type_of_curve_index=2, cumulative=True)
# plot_slotframe_distrib(input_params[0], file="plot_slotframe_ch8-400_cells-aggreg_per_timeslot.pdf", type_of_curve_index=3, cumulative=True)
# plot_timeslot_distrib(dir_path + "/topology_param_ch8_400.csv", file="plot_timeslot_ch8-400_cells.pdf", title="400 cells sheduled on 8 channels",max_ch=8)
# plot_timeslot_distrib(dir_path + "/topology_param_ch4_400.csv", file="plot_timeslot_ch4-400_cells.pdf", title="400 cells sheduled on 4 channels",max_ch=4)
plot_timeslot_distrib(dir_path + "/topology_param_ch8_400.csv", file="plot_timeslot_ch8-400_cells.pdf", max_ch=8, uniform_X_axis=False)
plot_timeslot_distrib(dir_path + "/topology_param_ch4_400.csv", file="plot_timeslot_ch4-400_cells.pdf", max_ch=4, uniform_X_axis=False)
