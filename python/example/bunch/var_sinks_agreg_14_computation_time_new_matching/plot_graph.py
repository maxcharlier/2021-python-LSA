from abc import ABC
import sys 
import os
sys.path.append('../../../')
from export_bunch import gen_topology
from gen_graph_bunch import schedule_duration_graph
from gen_graph_bunch import schedule_duration_bars
from gen_graph_bunch import slotframe_length_bars
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

REPEAT = 5
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

# plot_max_queue_size(input_params, curves_names, dir_path+"/maximum_queue_size_agreg.pdf", title="")
# slot_frame_length_graph(input_params, curves_names, dir_path+"/slot_frame_length_graph_agreg.pdf", title="", yticks=range(0, 1201, 100), curves_markers=curves_markers, alpha=0.8, legendcol=3)

schedule_duration_graph(input_params, curves_names, output_file=dir_path+"/schedule_duration_graph_agreg_means.pdf", title="", curves_markers=curves_markers, alpha=0.5, legendcol=3, repeat=REPEAT)
schedule_duration_bars(dir_path + "/topology_param_var_sinks_agreg1.csv", output_file="schedule_duration_bars_sinks_agreg1.pdf", title="", savefig=True,max_duration=14, repeat=REPEAT)
schedule_duration_bars(dir_path + "/topology_param_var_sinks_agreg14.csv", output_file="schedule_duration_bars_sinks_agreg14.pdf", title="", savefig=True,max_duration=14, repeat=REPEAT)
