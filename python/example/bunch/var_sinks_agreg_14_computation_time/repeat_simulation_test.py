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

input_params.append(dir_path + "/test-ch8-agr1-sink1.csv")
curves_names.append("1 a, 1 s")
curves_markers.append("s")
REPEAT = 5
# for file in input_params:
#   gen_topology(Bunch_Parameters.get_parameters_from_file(file), plot_graph=False, repeat=REPEAT)

schedule_duration_graph(input_params, curves_names, output_file=dir_path+"/schedule_duration_graph_filtered.pdf", title="", curves_markers=curves_markers, alpha=0.5, legendcol=3, repeat=REPEAT)