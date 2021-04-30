from nodes.node import Node

class Anchor(Node):

    def __init__(self, name, position, comm_range, disruption_range):
        """
        Class representing a mobile node
        :param id: The unique identifier of the node
        :param position: The position of the node
        :param tx_range: The transmission range of the node
        :param all_nodes: All the nodes in the network
        :param n_loc: The number of mobile locations per slotframe
        """
        super().__init__(name, position, comm_range, disruption_range, 'anchor')

        self.childrens = []
        # Define node in the routing tree
        self.parent = None
        self.parent_w = 0
        self.set_as_sink(False)

    def set_as_sink(self, sink):

        self.sink = sink
        if sink:
            self.rank = 0
            self.sink_distance = 0
            self.path = [self]
        else:
            self.rank = None
            self.sink_distance = None
            self.path = []

    def set_parent(self, parent, weight):
        """
        :param parent: a node 
        :param wieght: the number of message to transmit to this parent
        For anchors, always add the links to the sink first.
        """
        #first remove this node from childrens list of his current parent

        if self.parent != None:
            self.parent.remove_children(self)

        #set the parents
        self.parent = parent
        self.parent_w = weight

        parent.add_children(self)

        self.rank = self.parent.rank + 1

        self.path = [self] + self.parent.path
        self.sink_distance = self.parent.sink_distance + self.distance(self.parent)
    def remove_children(self, children):
        index = self.childrens.index(children)
        self.childrens.pop(index)

    def broadcast_rank(self):
        """
        Broadcast rank to all neighbors
        """
        for neighbour in self.neighbours:
            if neighbour.type == 'anchor' and not neighbour.sink:
                neighbour.receive_rank(self)

    def receive_rank(self, node):
        """
        Process the reception of a rank by a neighboring node.
        :param node: The node sending its rank
        """
        if self.rank is None or self.rank > node.rank + 1 or (
                self.rank == node.rank + 1 and self._path_through_node_shorter(node)):
            self.set_parent(node, 0)
            self.broadcast_rank()

    def initialise_and_get_w(self):
        """Tag start with the number of packet to send to anchors, anchors need to sum packet from children after the routing step."""
        w =0 
        for children in self.childrens:
            if children.type == 'tag':
                w += children.get_weight(self)
            elif not children.sink:
                w += children.initialise_and_get_w()

        self.parent_w = w
        return w

    def _path_through_node_shorter(self, node):
        """
        Method to know if follow path through a neighbour is the shortest path to the root
        :param id: The identifier of the neighboring node
        :return: True if the path passing through the neighboring node is shorter than the current path
        """
        return self.sink_distance > node.sink_distance + self.distance(node)