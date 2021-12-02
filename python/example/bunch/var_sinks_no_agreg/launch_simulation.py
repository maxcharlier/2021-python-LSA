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
from gen_graph_bunch import slotframe_length_bars
from export_bunch import Bunch_Parameters
import scheduling
import topology
import graphics

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
input_params = []
curves_names = []
output_file=dir_path + "/slot_frame_length_graph.pdf"

input_params.append(dir_path + "/ch8-agr1-sink1.csv")
curves_names.append("1 sink")
input_params.append(dir_path + "/ch8-agr1-sink2.csv")
curves_names.append("2 sinks")
input_params.append(dir_path + "/ch8-agr1-sink3.csv")
curves_names.append("3 sinks")
input_params.append(dir_path + "/ch8-agr1-sink4.csv")
curves_names.append("4 sinks")
input_params.append(dir_path + "/ch8-agr1-sink5.csv")
curves_names.append("5 sinks")
input_params.append(dir_path + "/ch8-agr1-sink9.csv")
curves_names.append("9 sinks")
input_params.append(dir_path + "/ch8-agr1-sink18.csv")
curves_names.append("18 sinks")
input_params.append(dir_path + "/ch8-agr1-sink440.csv")
curves_names.append("440 sinks")

# for file in input_params:
#   gen_topology(Bunch_Parameters.get_parameters_from_file(file), plot_graph=False)

slot_frame_length_graph(input_params, curves_names, output_file, title="", yticks=range(0, 1201, 100))
plot_max_queue_size(input_params, curves_names, dir_path+"/plot_max_queue_size.pdf", title="")
# plot_timeslots_usage(input_params, curves_names, savefig=True, index_param=6)
# positionning_frequency_graph(input_params, curves_names, title="", savefig=True, legendcol=2)
# positionning_frequency_bars(dir_path + "/topology_param.csv", output_file="positionning_frequency_bars.pdf", title="", savefig=True)
slotframe_length_bars(dir_path + "/topology_param.csv", output_file="slotframe_length_bars_8ch.pdf", title="", savefig=True, display_xlabels=True)
# schedule_duration_graph(input_params, curves_names, dir_path+"/schedule_duration_graph.pdf", title="")
