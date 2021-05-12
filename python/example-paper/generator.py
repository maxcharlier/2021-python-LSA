from abc import ABC
import sys 
sys.path.append('..')
import graphics
import scheduling
import topology

topology_ = topology.Topology(40, 20, 20, 30, 30, 2, 1)
topology_.import_param("./topology_param.csv")
topology_.import_nodes("./nodes.csv")
topology_.import_connectivity("./connectivity.csv")
topology_.import_routing("./routing.csv")
# anchors = []
# tags = []
# for node in topology_.nodes:
#   if node.type == 'anchor':
#     anchors.append(node)
#   else:
#     tags.append(node)
# for i in range(2):
#   for j in range(3):
#     tags[(2*i)].add_parent(anchors[j+i], 1)
#     tags[(2*i)+1].add_parent(anchors[j+i], 1)

# topology_.generate_neighbourhood(anchors, tags)
# topology_.set_nodes(anchors, tags)
# topology_.generate_routing()

# topology_.export_connectivity("./export_connectivity.csv")
# topology_.export_routing("./export_routing.csv")

graphics.plot_C(topology_.nodes, "./graph-C.pdf")
graphics.plot_neighbours(topology_.nodes, "./plot_neighbours.pdf")
graphics.plot_network_routing(topology_.nodes, "./plot_network_routing.pdf")
graphics.plot_Q(topology_.nodes, "./plot_Q.pdf")
graphics.dot_network_routing(topology_.nodes, "./dot_network_routing.dot")
(schedule, duration) = scheduling.scheduling(topology_, n_ch=6, agregation=1)
print("duration : " + str(duration))
scheduling.print_schedule(schedule)
print("len schedule " + str(len(schedule)))

# scheduling.export_schedule(schedule, "./schedule.csv")
print("-----")
scheduling.print_schedule(scheduling.import_schedule("./schedule.csv", topology_.nodes))
