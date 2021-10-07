from abc import ABC
import sys 
import os
sys.path.append('../../../')
from export_bunch import gen_topology
from gen_graph_bunch import plot_hop_count
from gen_graph_bunch import gen_graphs_from_file
from export_bunch import Bunch_Parameters
import scheduling
import topology
import graphics

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
input_params = []
curves_names = []
output_file=dir_path + "/slot_frame_length_graph.pdf"



input_params.append(dir_path + "/ch1-agr1-worst.csv")
curves_names.append("1 Channel Worst")
input_params.append(dir_path + "/ch1-agr1.csv")
curves_names.append("1 Channel")

# for file in input_params:
#   gen_topology(Bunch_Parameters.get_parameters_from_file(file), plot_graph=False)

plot_hop_count(dir_path + "/ch1-agr1.csv", dir_path + "/ch1-agr1-worst.csv", savefig=True,  output_file="plot_hop_count_no_agreg.pdf")
