from abc import ABC
import sys 
import os
sys.path.append('../../../')
from export_bunch import gen_topology
from gen_graph_bunch import slot_frame_length_graph
from gen_graph_bunch import positionning_frequency_graph
from gen_graph_bunch import plot_timeslots_usage
from gen_graph_bunch import gen_graphs_from_file
from gen_graph_bunch import plot_slotframe_distrib
from gen_graph_bunch import plot_slotframe_channels_usage
from gen_graph_bunch import schedule_duration_graph
from gen_graph_bunch import slotframe_length_bars
from export_bunch import Bunch_Parameters
import scheduling
import topology
import graphics
import matplotlib
import matplotlib.pyplot as plt
import csv
import math
from scipy.stats import truncnorm
import matplotlib.patches as mpatches
import numpy as np




def distribution_graph(input_csv_file, output_file="tag_per_cells.pdf", title="Tag per cells", savefig=True,timeslot_duration=5.0, update_rate_s=True):
  """Generate plot graph based on the schedule stat
  param timeslot_duration is in ms
  """

  bar_values = []
  labels = []
  refresh = []
  update_rate = []
  R = []
  legend_handles = []
  with open(input_csv_file) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      stat = scheduling.import_schedule_stat(str(row['directory']) + "schedule_stat.csv")
      topology_ = topology.Topology.import_param(str(row['directory']) + "topology_param.csv")
      topology_.import_nodes(str(row['directory']) + "nodes.csv")
      refresh.append(1000.0/(int(stat["len_schedule"])*timeslot_duration))
      update_rate.append((int(stat["len_schedule"])*timeslot_duration)/1000.0)
      # print("Shedule length " +str(int(stat["len_schedule"])))
      R.append(topology_.R)
      max_cells_x = math.ceil(topology_.x/topology_.space)
      max_cells_y = math.ceil(topology_.y/topology_.space)
      nb_tags_per_cells = [[0 for i in range(0, max_cells_y)] for j in range(0, max_cells_x)]
      for tag in topology_.nodes:
        if tag.type == "tag":  
          i = math.floor(tag.position.x/topology_.space)
          j = math.floor(tag.position.y/topology_.space)
          nb_tags_per_cells[i][j] += 1

      count_distrib = [0 for i in range(0, max([max(x) for x in nb_tags_per_cells])+1)]
      for i in range(len(nb_tags_per_cells)):
        for j in range(len(nb_tags_per_cells[i])):
          count_distrib[nb_tags_per_cells[i][j]]+=1
      bar_values.append(count_distrib)
      i+=1
  
  # print(bar_values)
  # print(refresh)

  #plot
  fig, ax = plt.subplots()
  max_x = max([len(x) for x in bar_values])

  #add 2 colors in the color cycle
  colors = list(plt.cm.tab10(np.arange(10))) + ["crimson", "indigo"]
  ax.set_prop_cycle('color', colors)

  # print(bar_values)
  for i in range(len(bar_values)):
      bar_plot = ax.bar([(x*2)+(i*(1.0/len(bar_values))) for x in range(0, len(bar_values[i]))],[(x/sum(bar_values[i]))*100 for x in bar_values[i]])
      # Creating legend with color box
      if i == 0:
        color = bar_plot.patches[-1].get_facecolor()
        # Creating legend with color box
        legend_handles.append(mpatches.Patch(color=color, label="Uniform distribution"))  
        legend_handles.append(mpatches.Patch(color='black', label="Mean values"))    
      if i == 1:
        color = bar_plot.patches[-1].get_facecolor()
        # Creating legend with color box
        legend_handles.append(mpatches.Patch(color=color, label="Run 1"))
        legend_handles.append(mpatches.Patch(color="white", label="   ..."))    
      if i == len(bar_values)-1:
        color = bar_plot.patches[-1].get_facecolor()
        # Creating legend with color box
        legend_handles.append(mpatches.Patch(color=color, label="Run "+str(len(bar_values)-1)))

  plt.xticks([(x*2)+0.5 for x in range(0, max_x)], range(0, max_x)) 
  plt.yticks([i*10 for i in range(0, 11)]) 
  plt.xlabel('Number of tags in a cell')
  plt.ylabel('Fraction of cells [\%]')
  plt.grid(color='tab:grey', linestyle='--', linewidth=1, alpha=0.3)
  plt.title(title)
  plt.legend(handles=legend_handles)
  if savefig:
    plt.savefig(output_file[:-4]+"-nb-tags-per-cells.pdf")
    plt.close()
  else:
    plt.show()
  plt.clf()

  #plot2
  fig, ax = plt.subplots()


  #add 2 colors in the color cycle
  colors = list(plt.cm.tab10(np.arange(10))) + ["crimson", "indigo"]
  ax.set_prop_cycle('color', colors)

  ax_secondary = ax.twiny()
  max_x = max([len(x) for x in bar_values])

  def i_to_x(i):
    return (i*2)

  # print([(refresh[0]*R[0])/i for i in range(1, max_x)])
  # print([(x*2)+0.5 for x in range(1, max_x)])
  distribution_tags = [[] for i in range(0, len(bar_values))] #percentage of tags for each number of tags in a cell.
  for i in range(0, len(bar_values)):
    nb_tags = sum([((bar_values[i][y]*y)) for y in range(1, len(bar_values[i]))])
    if i == 0:
      distribution_tags[i] = [((bar_values[i][y]*y)/nb_tags*100) for y in range(1, len(bar_values[i]))]
      bar_plot = ax.bar([i_to_x(x) for x in range(1, len(bar_values[i]))],distribution_tags[i])
    else:
      distribution_tags[i] = [((bar_values[i][y]*y)/nb_tags*100) for y in range(1, len(bar_values[i]))]
      bar_plot = ax.bar([i_to_x(x)-0.5+(i*(1.0/len(bar_values))) for x in range(1, len(bar_values[i]))],distribution_tags[i])
  
  # print(distributison_tags)

  bar_mean= [0 for x in range(1, max([len(bar_values[i]) for i in range(1, len(bar_values))]))]
  # print("bar mean " + str(bar_mean))
  for i in range(1, len(bar_values)):
    j=0
    nb_tags = sum([((bar_values[i][y]*y)) for y in range(1, len(bar_values[i]))])
    # print(bar_values[i][1:])
    for y in range(1, len(bar_values[i])):
      bar_mean[j]+= ((bar_values[i][y]*y)/nb_tags)*100 
      j+=1

  for i in range(0, len(bar_mean)):
    bar_mean[i] = bar_mean[i]/(len(bar_values)-1)
  print("sum mean " + str(sum(bar_mean)))

  plt.plot([i_to_x(i) for i in range(1, max_x)], bar_mean, color='black')

  # print("sum mean " +str(sum(bar_mean)))

  def convert_tag_per_cell_to_refresh(tab):
    refresh_means = []
    for distrib in tab:
      refresh_means_current = 0
      for i in range(len(distrib)):
        tag_per_cell_to_refresh = (refresh[0]/(i+1))*R[0] #(refresh of uniform distribution / nb_tag_in_a_cell) * nb_tag_in_a_cell_uniform_distribution
        refresh_means_current += distrib[i]*tag_per_cell_to_refresh
      refresh_means.append(refresh_means_current/100.0)
    return refresh_means

  print("Means refresh for uniform run " + str(convert_tag_per_cell_to_refresh([distribution_tags[0]])))
  print("Means refresh for uniform run " + str(1/sum(convert_tag_per_cell_to_refresh([distribution_tags[0]]))))
  print("Means refresh for all run " + str(convert_tag_per_cell_to_refresh(distribution_tags)))
  print("Means refresh for all random run " + str(convert_tag_per_cell_to_refresh(distribution_tags[1:])))
  print("--------------------")
  print("Means refresh for all random run " + str(sum(convert_tag_per_cell_to_refresh(distribution_tags[1:]))/len(distribution_tags[1:])) +" Hz")
  print("Means refresh for all random run " + str(1/(sum(convert_tag_per_cell_to_refresh(distribution_tags[1:]))/len(distribution_tags[1:])))+" s")
  print("--------------------")

  #axis ticks and label
  #bottom x axis
  ax.set_xticks([i_to_x(i) for i in range(1, max_x)]) 
  ax.set_xticklabels([str(i) for i in range(1, max_x)]) 
  ax.set_xlabel('Number of tags in a cell')

  #top x axis
  ax_secondary.set_xlim(ax.get_xlim())
  # print(ax.get_xlim())
  ax_secondary.set_xticks([i_to_x(i) for i in range(1, max_x)])
  # print(ax.get_xticks())
  ax_secondary.set_xticklabels([(str(round((refresh[0]/(x/2)*R[0]),3)) if x > 0 else '') for x in ax_secondary.get_xticks()])
  ax_secondary.set_xlabel('Localisation rate for each tag [Hz]')
  #yaxis
  plt.yticks([i*10 for i in range(0, 11)]) 
  ax.set_ylabel('Fraction of tags [\%]')
  plt.ylim((0,100))

  ax.grid(color='tab:grey', linestyle='--', linewidth=1, alpha=0.3)
  # plt.title(title)
  plt.legend(handles=legend_handles)
  plt.tight_layout()
  if savefig:
    plt.savefig(output_file[:-4]+"-refresh-pos.pdf")
    plt.close()
  else:
    plt.show()

dir_path = os.path.dirname(os.path.realpath(__file__))

# gen_topology(Bunch_Parameters.get_parameters_from_file(dir_path + "/topology_param-distrib-1.csv"), plot_graph=False)
distribution_graph(dir_path + "/topology_param-distrib-1.csv", output_file="distribution-1-tag.pdf")

# gen_topology(Bunch_Parameters.get_parameters_from_file(dir_path + "/topology_param-distrib-2.csv"), plot_graph=False)
# distribution_graph(dir_path + "/topology_param-distrib-2.csv", output_file="distribution-2-tags.pdf")
# slotframe_length_bars(dir_path + "/topology_param-distrib-1.csv", output_file="slotframe_length_bars_distrib_1.pdf", title="", savefig=True)
# slotframe_length_bars(dir_path + "/topology_param-distrib-2.csv", output_file="slotframe_length_bars_distrib_2.pdf", title="", savefig=True)
