from abc import ABC
import sys 
import os
sys.path.append('../../../')
from export_bunch import gen_topology
from export_bunch import Bunch_Parameters

dir_path = os.path.dirname(os.path.realpath(__file__))

gen_topology(Bunch_Parameters.get_parameters_from_file(dir_path + "/topology_param-distrib-1.csv"), plot_graph=False)
gen_topology(Bunch_Parameters.get_parameters_from_file(dir_path + "/topology_param-distrib-2.csv"), plot_graph=False)
