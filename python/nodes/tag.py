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