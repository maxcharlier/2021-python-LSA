from abc import ABC
from nodes.point import Point
import sys 
sys.path.append('..')

from scheduling import Link

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
        self.last_slot = -1
        self.last_link = None


    def update_Q(self, offset):
        """Update the value of Q for the node and his parents"""
        self.Q = self.Q + offset
    def get_Q(self):
        return self.Q
    def get_weight(self):
        return self.current_weight


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

    def remove_children(self, children):
        self.childrens.remove(children)
        
    def distance(self, node):
        return self.position.distance(node.position)

    def get_last_slot_number(self):
        """Return the last timeslot when the node has been selected in the shedule"""
        return self.last_slot

    def set_slot_number(self, slot):
        """Update the last timeslot when the node was selected for the scedule"""
        self.last_slot = slot

    def set_link(self, link):
        """Set the last transmition link selected in the scheduling"""
        self.link = link
    def get_link(self):
        """Return the last transmition link selected in the scheduling"""
        return self.link

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
