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
from export_bunch import Bunch_Parameters
import scheduling
import topology
import graphics

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
input_params = []
curves_names = []
output_file=dir_path + "/slot_frame_length_graph.pdf"

# input_params.append(dir_path + "/ch1-agr1-TDMA.csv")
# curves_names.append("Global TDMA")


input_params.append(dir_path + "/ch1-agr1.csv")
curves_names.append("1 Ch. - agreg 1")
input_params.append(dir_path + "/ch2-agr1.csv")
curves_names.append("2 to 8 Ch. - agreg 1")
# input_params.append(dir_path + "/ch8-agr1.csv")
# curves_names.append("8 Ch. - agreg 1")
input_params.append(dir_path + "/ch8-agr2.csv")
curves_names.append("8 Ch. - agreg 2")
input_params.append(dir_path + "/ch8-agr4.csv")
curves_names.append("8 Ch. - agreg 4")
input_params.append(dir_path + "/ch8-agr7.csv")
curves_names.append("8 Ch. - agreg 7")
input_params.append(dir_path + "/ch1-agr14.csv")
curves_names.append("1 Ch. - agreg 14")
input_params.append(dir_path + "/ch2-agr14.csv")
curves_names.append("2 Ch. - agreg 14")
input_params.append(dir_path + "/ch8-agr14.csv")
curves_names.append("8 Ch. - agreg 14")

# for file in input_params:
#   gen_topology(Bunch_Parameters.get_parameters_from_file(file), plot_graph=False)

slot_frame_length_graph(input_params, curves_names, output_file, title="", yticks=range(0, 1401, 100), timeslot_duration = 5)
# plot_timeslots_usage(input_params, curves_names, savefig=True)
positionning_frequency_graph(input_params, curves_names, title="", savefig=True)

