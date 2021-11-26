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
from gen_graph_bunch import positionning_frequency_bars
from gen_graph_bunch import schedule_duration_graph
from gen_graph_bunch import plot_max_queue_size
from export_bunch import Bunch_Parameters
import scheduling
import topology
import graphics

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
input_params = []
curves_names = []
curves_markers = []
curves_colors = []
output_file=dir_path + "/slot_frame_length_graph.pdf"

input_params.append(dir_path + "/ch8-agr1-sink1.csv")
curves_names.append("1 a, 1 s")
curves_markers.append("s")
curves_colors.append('0.15')
input_params.append(dir_path + "/ch8-agr1-sink2.csv")
curves_names.append("1 a, 2 s")
curves_markers.append("s")
curves_colors.append('0.25')
input_params.append(dir_path + "/ch8-agr1-sink3.csv")
curves_names.append("1 a, 3 s")
curves_markers.append("s")
curves_colors.append('0.35')
input_params.append(dir_path + "/ch8-agr1-sink4.csv")
curves_names.append("1 a, 4 s")
curves_markers.append("s")
curves_colors.append('0.45')
input_params.append(dir_path + "/ch8-agr1-sink5.csv")
curves_names.append("1 a, 5 s")
curves_markers.append("s")
curves_colors.append('0.55')
input_params.append(dir_path + "/ch8-agr1-sink9.csv")
curves_names.append("1 a, 9 s")
curves_markers.append("s")
curves_colors.append('0.65')
input_params.append(dir_path + "/ch8-agr1-sink18.csv")
curves_names.append("1 a, 18 s")
curves_markers.append("s")
curves_colors.append('0.75')
input_params.append(dir_path + "/ch8-agr1-sink440.csv")
curves_names.append("1 a, 440 s")
curves_markers.append("s")
curves_colors.append('0.85')

input_params.append(dir_path + "/ch8-agr2-sink1.csv")
curves_names.append("2 a, 1 s")
curves_markers.append("X")
curves_colors.append('0.25')
input_params.append(dir_path + "/ch8-agr3-sink1.csv")
curves_names.append("3 a, 1 s")
curves_markers.append("X")
curves_colors.append('0.55')
input_params.append(dir_path + "/ch8-agr4-sink1.csv")
curves_names.append("4 a, 1 s")
curves_markers.append("X")
curves_colors.append('0.75')
input_params.append(dir_path + "/ch8-agr7-sink1.csv")
curves_names.append("7 a, 1 s")
curves_markers.append("X")
curves_colors.append('0.85')

input_params.append(dir_path + "/ch8-agr14-sink1.csv")
curves_names.append("14 a, 1 s")
curves_markers.append("*")
curves_colors.append('0.15')
input_params.append(dir_path + "/ch8-agr14-sink2.csv")
curves_names.append("14 a, 2 s")
curves_markers.append("*")
curves_colors.append('0.25')
input_params.append(dir_path + "/ch8-agr14-sink3.csv")
curves_names.append("14 a, 3 s")
curves_markers.append("*")
curves_colors.append('0.35')
input_params.append(dir_path + "/ch8-agr14-sink4.csv")
curves_names.append("14 a, 4 s")
curves_markers.append("*")
curves_colors.append('0.45')
input_params.append(dir_path + "/ch8-agr14-sink5.csv")
curves_names.append("14 a, 5 s")
curves_markers.append("*")
curves_colors.append('0.55')
input_params.append(dir_path + "/ch8-agr14-sink9.csv")
curves_names.append("14 a, 9 s")
curves_markers.append("*")
curves_colors.append('0.65')
input_params.append(dir_path + "/ch8-agr14-sink18.csv")
curves_names.append("14 a, 18 s")
curves_markers.append("*")
curves_colors.append('0.75')
input_params.append(dir_path + "/ch8-agr14-sink440.csv")
curves_names.append("14 a, 440 s")
curves_markers.append("*")
curves_colors.append('0.85')

# for file in input_params:
#   gen_topology(Bunch_Parameters.get_parameters_from_file(file), plot_graph=False)

slot_frame_length_graph(input_params, curves_names, output_file, title="", yticks=range(0, 1201, 100), curves_markers=curves_markers, alpha=0.8, legendcol=3)
# plot_timeslots_usage(input_params, curves_names, savefig=True, index_param=6)
positionning_frequency_graph(input_params, curves_names, title="", savefig=True, legendcol=3, curves_markers=curves_markers, alpha=0.5)
# positionning_frequency_bars(dir_path + "/topology_param.csv", output_file="positionning_frequency_bars.pdf", title="", savefig=True)
schedule_duration_graph(input_params, curves_names, dir_path+"/schedule_duration_graph.pdf", title="", curves_markers=curves_markers, alpha=0.5, legendcol=3)

input_params = []
curves_names = []
curves_markers = []
curves_colors = []
output_file=dir_path + "/slot_frame_length_graph.pdf"

input_params.append(dir_path + "/ch8-agr1-sink1.csv")
curves_names.append("1 a, 1 s")
curves_markers.append("s")
curves_colors.append('0.15')
input_params.append(dir_path + "/ch8-agr1-sink18.csv")
curves_names.append("1 a, 18 s")
curves_markers.append("s")
curves_colors.append('0.75')

# input_params.append(dir_path + "/ch8-agr2-sink1.csv")
# curves_names.append("2 a, 1 s")
# curves_markers.append("X")
# curves_colors.append('0.25')
# input_params.append(dir_path + "/ch8-agr3-sink1.csv")
# curves_names.append("3 a, 1 s")
# curves_markers.append("X")
# curves_colors.append('0.55')
# input_params.append(dir_path + "/ch8-agr4-sink1.csv")
# curves_names.append("4 a, 1 s")
# curves_markers.append("X")
# curves_colors.append('0.75')
# input_params.append(dir_path + "/ch8-agr7-sink1.csv")
# curves_names.append("7 a, 1 s")
# curves_markers.append("X")
# curves_colors.append('0.85')

input_params.append(dir_path + "/ch8-agr14-sink1.csv")
curves_names.append("14 a, 1 s")
curves_markers.append("*")
curves_colors.append('0.15')
input_params.append(dir_path + "/ch8-agr14-sink2.csv")
curves_names.append("14 a, 2 s")
curves_markers.append("*")
curves_colors.append('0.25')
input_params.append(dir_path + "/ch8-agr14-sink3.csv")
curves_names.append("14 a, 3 s")
curves_markers.append("*")
curves_colors.append('0.35')
input_params.append(dir_path + "/ch8-agr14-sink4.csv")
curves_names.append("14 a, 4 s")
curves_markers.append("*")
curves_colors.append('0.45')
input_params.append(dir_path + "/ch8-agr14-sink5.csv")
curves_names.append("14 a, 5 s")
curves_markers.append("*")
curves_colors.append('0.55')
input_params.append(dir_path + "/ch8-agr14-sink9.csv")
curves_names.append("14 a, 9 s")
curves_markers.append("*")
curves_colors.append('0.65')
input_params.append(dir_path + "/ch8-agr14-sink18.csv")
curves_names.append("14 a, 18 s")
curves_markers.append("*")
curves_colors.append('0.75')


input_params.append(dir_path + "/ch8-agr1-sink440.csv")
curves_names.append("1 to 14 a, 440 s")
curves_markers.append("s")
curves_colors.append('0.85')

# for file in input_params:
#   gen_topology(Bunch_Parameters.get_parameters_from_file(file), plot_graph=False)

# slot_frame_length_graph(input_params, curves_names, output_file=dir_path+"/slot_frame_length_graph_filtered.pdf", title="", yticks=range(0, 1201, 100), curves_markers=curves_markers, alpha=0.8, legendcol=3)
# plot_timeslots_usage(input_params, curves_names, savefig=True, index_param=6)
# positionning_frequency_graph(input_params, curves_names, output_file=dir_path+"/positionning_frequency_filtered.pdf", title="", savefig=True, legendcol=3, curves_markers=curves_markers, alpha=0.5)
# positionning_frequency_bars(dir_path + "/topology_param.csv", output_file="positionning_frequency_bars.pdf", title="", savefig=True)
# schedule_duration_graph(input_params, curves_names, output_file=dir_path+"/schedule_duration_graph_filtered.pdf", title="", curves_markers=curves_markers, alpha=0.5, legendcol=3)

plot_max_queue_size(input_params, curves_names, dir_path+"/maximum_queue_size.pdf", title="")
