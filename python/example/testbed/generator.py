from abc import ABC
import sys 
sys.path.append('../..')
import graphics
import scheduling
from topology import Topology
channels = 6

# topology_ = Topology(40, 20, 20, 30, 30, 2, 1)
topology_ = Topology.import_param("./topology_param.csv")
topology_.import_nodes("./nodes.csv")
topology_.import_connectivity("./connectivity.csv")
topology_.import_routing("./routing.csv")

graphics.plot_C(topology_.nodes, "./graph-C.pdf")
graphics.plot_neighbours(topology_.nodes, "./plot_neighbours.pdf")
graphics.plot_network_routing(topology_.nodes, "./plot_network_routing.pdf")
graphics.plot_Q(topology_.nodes, "./plot_Q.pdf")
graphics.dot_network_routing(topology_.nodes, "./dot_network_routing.dot")
(schedule, duration) = scheduling.scheduling(topology_, n_ch=1, agregation=1)
print("duration : " + str(duration))
scheduling.print_schedule(schedule)
print("len schedule " + str(len(schedule)))

scheduling.export_schedule(schedule, "./schedule.csv")
print("-----")
# scheduling.print_schedule(scheduling.import_schedule("./schedule.csv", topology_.nodes))

graphics.plot_slot_frame(schedule, "./plot_slot_frame.pdf", nb_ch = channels)
