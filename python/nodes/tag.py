from nodes.node import Node

class Tag(Node):

    def __init__(self, name, position, comm_range, disruption_range):
        """
        Class representing a mobile node
        :param id: The unique identifier of the node
        :param position: The position of the node
        :param tx_range: The transmission range of the node
        :param all_nodes: All the nodes in the network
        :param n_loc: The number of mobile locations per slotframe
        """
        super().__init__(name, position, comm_range, disruption_range, 'tag')
        self.parents = []
        self.parents_w = []

    def is_parent(self, node):
        return node in self.parents

    def add_parent(self, parent, weight):
        """
        :param parent: a node 
        :param wieght: the number of message to transmit to this parent
        For anchors, always add the links to the sink first.
        """
        if not self.is_parent(parent):
            self.parents.append(parent)
            self.parents_w.append(weight)
            parent.add_children(self)
            self.neighbours.append(parent)

    def remove(self):
        for parent in self.parents:
            parent.remove_children(self)
            
    def get_weight(self, parent):
        if self.is_parent(parent):
            return self.parents_w[self.parents.index(parent)]
        else:
            raise Exception("This parent do not exist " + str(parent))
            return 0

    def gen_comm_parents(self):
        """Generate the connectivity of the tag based on the union of connectiviy of his parents """
        for parent in self.parents:
            for node in parent.neighbours:
                self.add_comm_node(node)
                #do other side because connectivity is be derectionnal
                node.add_comm_node(self)

    def gen_disrupted_nodes(self):
        """Generate the connectivity of the tag based on the union of connectiviy of his parents """
        for parent in self.parents:
            for node in parent.disrupted_nodes:
                self.add_disrupted_node(node)
                #do other side because connectivity is be derectionnal
                node.add_disrupted_node(self)

    def initialise_Q(self):
        """Tag start with the number of packet to send to anchors, anchors need to sum packet from children after the routing step."""
        Q =0 
        for weight in self.parents_w:
            Q += weight
        self.Q = Q
    def send_packet(self, destination, agregate=1):
        """
        Send a packet to a neighboring node
        :param destination: The destination node
        """
        destination.receive_packet(agregate)
        self.parents_w[self.parents.index(destination)] -= agregate

        self.update_Q(-agregate)

        if self.current_weight < 0 :
            raise Exception("The weight (number of message in the buffer) cannot be negative")

    def get_rank(self):
        """Return the number of hop between the node and the sink"""
        rank = self.parents[0].get_rank()
        for parent in self.parents[1:]:
            rank = max(rank, parent.get_rank())
        return rank + 1