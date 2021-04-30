from abc import ABC
from nodes.point import Point

class Node(ABC):
    def __init__(self, name, position, comm_range, disruption_range, type):
        """
        Abstract class of a node
        :param name: The unique name of the node
        :param position: The position of the node
        :param comm_range: The communciation range of the node
        :param disruption_range: The disruption range of the node
        :param type: The type of node
        """
        self.name = name
        self.position = position
        self.comm_range = comm_range
        self.disruption_range = disruption_range
        self.type = type

        # weight the number of packet to transmit.
        self.current_weight = 0
        self.initial_weight = 0

        """ neighbours are nodes that have a distance <= comm_range
        disrupted nodes are nodes that have distance <= disruption_range"""
        self.neighbours = []
        self.disrupted_nodes = []
        self.Q = 0


    def update_Q(self, offset):
        """Update the value of Q for the node and his parents"""
        self.Q = self.Q + offset

    def set_initial_weight(self, weight):
        if weight < 0 :
            raise Exeption("The weight (number of message in the buffer) cannot be negative")
        self.initial_weight = weight
        self.current_weight = weight

    def add_disrupted_node(self, node):
        if not self.is_disrupted_node(node):
            self.disrupted_nodes.append(node)

    def is_disrupted_node(self, node):
        return node in self.disrupted_nodes

    def add_comm_node(self, node):
        if not self.is_comm_node(node):
            self.neighbours.append(node)

    def is_comm_node(self, node):
        return node in self.neighbours

    def is_recheable(self, node, distance):
        return self.position.distance(node.position) <= distance

    def add_children(self, children):
        self.childrens.append(children)

    def send_packet(self, destination):
        """
        Send a packet to a neighboring node
        :param destination: The destination node
        """
        destination.receive_packet()
        self.current_weight -= 1
        self.parents_w[self.parent.index(destination)] += 1

        self.update_Q(-1)

        if self.curent_weight < 0 :
            raise Exeption("The weight (number of message in the buffer) cannot be negative")
    def distance(self, node):
        return self.position.distance(node.position)
    def __str__(self):
        """
        String representation
        :return: String representation
        """
        return '{}[name={} pos={}]'.format(self.type, self.name,self.position)

    def __repr__(self) -> str:
        """
        Node representation
        :return: Node representation as string
        """
        return self.__str__()

    def __eq__(self, other):
        """
        Comparator method
        :param other: The other object
        :return: True if the objects are equal, False otherwise
        """
        if isinstance(other, Node):
            return self.name == other.name and \
                   self.position == other.position and \
                   self.type == other.type
        return False

    def __hash__(self):
        """
        Hash method
        :return: The hash of the node
        """
        return hash(self.name)
