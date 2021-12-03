from abc import ABC
import sys 
import os
sys.path.append('../../../')
from export_bunch import gen_topology
from gen_graph_bunch import plot_max_queue_size
from gen_graph_bunch import slot_frame_length_graph
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
curves_names.append("A1,S1")
curves_markers.append("s")
curves_colors.append('0.15')
input_params.append(dir_path + "/ch8-agr1-sink440.csv")
curves_names.append("A1,SAll")
curves_markers.append("s")
curves_colors.append('0.85')

input_params.append(dir_path + "/ch8-agr2-sink1.csv")
curves_names.append("A2,S1")
curves_markers.append("X")
curves_colors.append('0.25')
input_params.append(dir_path + "/ch8-agr3-sink1.csv")
curves_names.append("A3,S1")
curves_markers.append("X")
curves_colors.append('0.55')
input_params.append(dir_path + "/ch8-agr4-sink1.csv")
curves_names.append("A4,S1")
curves_markers.append("X")
curves_colors.append('0.75')
input_params.append(dir_path + "/ch8-agr7-sink1.csv")
curves_names.append("A7,S1")
curves_markers.append("X")
curves_colors.append('0.85')


input_params.append(dir_path + "/ch8-agr14-sink1.csv")
curves_names.append("A14,S1")
curves_markers.append("*")
curves_colors.append('0.85')

input_params.append(dir_path + "/ch8-agr14-sink440.csv")
curves_names.append("A14,SAll")
curves_markers.append("*")
curves_colors.append('0.85')

# for file in input_params:
#   gen_topology(Bunch_Parameters.get_parameters_from_file(file), plot_graph=False)

plot_max_queue_size(input_params, curves_names, dir_path+"/maximum_queue_size_agreg.pdf", title="",yticks=[i for i in range(0, 30, 5)]+[28])
slot_frame_length_graph(input_params, curves_names, dir_path+"/slot_frame_length_graph_agreg.pdf", title="", yticks=range(0, 1201, 100), curves_markers=curves_markers, alpha=0.8, legendcol=3)
