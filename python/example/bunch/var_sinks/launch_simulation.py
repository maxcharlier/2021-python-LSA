from abc import ABC
import sys 
import os
sys.path.append('../../../')
from export_bunch import gen_topology
from gen_graph_bunch import slot_frame_lenght_graph
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

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
input_params = []
output_file=dir_path + "/slot_frame_lenght_graph.pdf"

input_params.append(dir_path + "/topology_param.csv")

# for file in input_params:
#   gen_topology(Bunch_Parameters.get_parameters_from_file(file), plot_graph=False)

# slot_frame_lenght_graph(input_params, curves_names, output_file, title="")
# plot_timeslots_usage(input_params, curves_names, savefig=True)
# positionning_frequency_graph(input_params, curves_names, title="", savefig=False)
positionning_frequency_bars(input_params[0], title="", savefig=True)

# plot_slotframe_distrib(dir_path + "/plot_slotframe_distrib.csv", file="plot_slotframe_distrib_0.pdf", type_of_curve_index=0, cumulative=False)
# plot_slotframe_distrib(dir_path + "/plot_slotframe_distrib.csv", file="plot_slotframe_distrib_1.pdf", type_of_curve_index=1, cumulative=False)
# plot_slotframe_distrib(dir_path + "/plot_slotframe_distrib.csv", file="plot_slotframe_distrib_2.pdf", type_of_curve_index=2, cumulative=False)
# plot_slotframe_distrib(dir_path + "/plot_slotframe_distrib.csv", file="plot_slotframe_distrib_3.pdf", type_of_curve_index=3, cumulative=False)
# plot_slotframe_distrib(dir_path + "/plot_slotframe_distrib.csv", file="plot_slotframe_distrib_cumulative_0.pdf", type_of_curve_index=0, cumulative=True)
# plot_slotframe_distrib(dir_path + "/plot_slotframe_distrib.csv", file="plot_slotframe_distrib_cumulative_1.pdf", type_of_curve_index=1, cumulative=True)
# plot_slotframe_distrib(dir_path + "/plot_slotframe_distrib.csv", file="plot_slotframe_distrib_cumulative_2.pdf", type_of_curve_index=2, cumulative=True)
# plot_slotframe_distrib(dir_path + "/plot_slotframe_distrib.csv", file="plot_slotframe_distrib_cumulative_3.pdf", type_of_curve_index=3, cumulative=True)
# plot_slotframe_channels_usage(dir_path + "/plot_slotframe_distrib.csv", file="plot_slotframe_channels_usage.pdf", nb_channel_max=8, cumulative=True)

