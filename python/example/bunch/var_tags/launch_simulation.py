from abc import ABC
import sys 
import os
sys.path.append('../../../')
from export_bunch import gen_topology
from gen_graph_bunch import slot_frame_lenght_graph
from export_bunch import Bunch_Parameters

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
input_params = []
curves_names = []
output_file=dir_path + "/stat_graph2.pdf"

# input_params.append(dir_path + "/ch1-agr1-TDMA.csv")
# curves_names.append("No concurrent cummunication")


input_params.append(dir_path + "/ch1-agr1.csv")
curves_names.append("1 Ch. - 1 Agreg.")
input_params.append(dir_path + "/ch2-agr1.csv")
curves_names.append("2 Ch. - 1 Agreg.")
input_params.append(dir_path + "/ch8-agr1.csv")
curves_names.append("8 Ch. - 1 Agreg.")

input_params.append(dir_path + "/ch1-agr4.csv")
curves_names.append("1 Ch. - 4 Agreg.")
input_params.append(dir_path + "/ch2-agr4.csv")
curves_names.append("2 Ch. - 4 Agreg.")
input_params.append(dir_path + "/ch8-agr4.csv")
curves_names.append("8 Ch. - 4 Agreg.")

# for file in input_params:
#   gen_topology(Bunch_Parameters.get_parameters_from_file(file), plot_graph=False)

slot_frame_lenght_graph(input_params, curves_names, output_file)
