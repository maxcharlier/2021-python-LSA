import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from nodes.anchor import Anchor
from nodes.tag import Tag
from nodes.point import Point
import os

def plot_neighbours(all_nodes, filepath):
    """
    Create a graph representing the current network
    :param all_nodes: All network nodes
    :param filepath: The path to save the figure
    """
    for node in all_nodes:
        for neighbour in node.neighbours:
            plt.plot([node.position.x, neighbour.position.x], [node.position.y, neighbour.position.y], color='black',
                     linewidth=0.5)

        if node.type == 'tag':
            plt.plot(node.position.x, node.position.y, color='red', marker='o')
        else:
            if node.sink:
                plt.plot(node.position.x, node.position.y, color='royalblue', marker='s')
            else:
                plt.plot(node.position.x, node.position.y, color='green', marker='s')
        plt.annotate(str(node.name), (node.position.x, node.position.y), xytext=(0, -8),
                     textcoords='offset points')

    legend_elements = [Line2D([0], [0], color='red', marker='o', label='mobile'),
                       Line2D([0], [0], color='royalblue', marker='s', label='anchor (root)'),
                       Line2D([0], [0], color='green', marker='s', label='anchor'),
                       Line2D([0], [0], color='black', linewidth=1, label='physical link')]
    plt.legend(handles=legend_elements)
    # plt.show()
    plt.savefig(filepath)
    plt.close()

def plot_C(all_nodes, filepath):
    """
    Create a graph representing the current network
    :param all_nodes: All network nodes
    :param filepath: The path to save the figure
    """
    for node in all_nodes:
        for neighbour in node.disrupted_nodes:
            plt.plot([node.position.x, neighbour.position.x], [node.position.y, neighbour.position.y], color='black',
                     linewidth=0.5)

        if node.type == 'tag':
            plt.plot(node.position.x, node.position.y, color='red', marker='o')
        else:
            if node.sink:
                plt.plot(node.position.x, node.position.y, color='royalblue', marker='s')
            else:
                plt.plot(node.position.x, node.position.y, color='green', marker='s')
        # plt.annotate(str(node.Q), (node.position.x, node.position.y), xytext=(0, 4),
        #              textcoords='offset points')
        plt.annotate(str(node.name), (node.position.x, node.position.y), xytext=(0, -8),
                     textcoords='offset points')

    legend_elements = [Line2D([0], [0], color='red', marker='o', label='mobile'),
                       Line2D([0], [0], color='royalblue', marker='s', label='anchor (root)'),
                       Line2D([0], [0], color='green', marker='s', label='anchor'),
                       Line2D([0], [0], color='black', linewidth=1, label='physical link')]
    plt.legend(handles=legend_elements)
    plt.savefig(filepath)
    plt.close()

def plot_Q(all_nodes, filepath):
    """
    Create a graph representing the current network
    :param all_nodes: All network nodes
    :param filepath: The path to save the figure
    """
    for node in all_nodes:

        if node.type == 'tag':
            plt.plot(node.position.x, node.position.y, color='red', marker='o')
        else:
            if node.sink:
                plt.plot(node.position.x, node.position.y, color='royalblue', marker='s')
            else:
                plt.plot(node.position.x, node.position.y, color='green', marker='s')
        # plt.annotate(str(node.Q), (node.position.x, node.position.y), xytext=(0, 4),
        #              textcoords='offset points')
        plt.annotate(str(node.get_Q()), (node.position.x, node.position.y), xytext=(0, -8),
                     textcoords='offset points')

    legend_elements = [Line2D([0], [0], color='red', marker='o', label='mobile'),
                       Line2D([0], [0], color='royalblue', marker='s', label='anchor (root)'),
                       Line2D([0], [0], color='green', marker='s', label='anchor'),
                       Line2D([0], [0], color='black', linewidth=1, label='physical link')]
    plt.legend(handles=legend_elements)
    plt.savefig(filepath)
    plt.close()

def plot_network_routing(all_nodes, filepath):
    """
    Create a graph representing the current network
    :param all_nodes: All network nodes
    :param filepath: The path to save the figure
    """
    for node in all_nodes:
        if node.type == 'tag':
            for parent in node.parents:
                plt.plot([node.position.x, parent.position.x], [node.position.y, parent.position.y], color='black',
                         linewidth=0.5)
        elif node.parent != None:
            # plt.plot([node.position.x, node.parent.position.x], [node.position.y, node.parent.position.y], color='black',
            #              linewidth=0.5)
            plt.arrow(node.position.x, node.position.y, node.parent.position.x-node.position.x, node.parent.position.y-node.position.y, head_width=0.05, head_length=0.1, fc='k', ec='k')

        if node.type == 'tag':
            plt.plot(node.position.x, node.position.y, color='red', marker='o')
        else:
            if node.sink:
                plt.plot(node.position.x, node.position.y, color='royalblue', marker='s')
            else:
                plt.plot(node.position.x, node.position.y, color='green', marker='s')
        # plt.annotate(str(node.Q), (node.position.x, node.position.y), xytext=(0, 4),
        #              textcoords='offset points')
        plt.annotate(str(node.name), (node.position.x, node.position.y), xytext=(0, -8),
                     textcoords='offset points')

    legend_elements = [Line2D([0], [0], color='red', marker='o', label='mobile'),
                       Line2D([0], [0], color='royalblue', marker='s', label='anchor (root)'),
                       Line2D([0], [0], color='green', marker='s', label='anchor'),
                       Line2D([0], [0], color='black', linewidth=1, label='physical link')]
    plt.legend(handles=legend_elements)
    plt.savefig(filepath)
    plt.close()

def plot_network_routing(all_nodes, filepath):
    """
    Create a graph representing the current network
    :param all_nodes: All network nodes
    :param filepath: The path to save the figure
    """
    for node in all_nodes:
        if node.type == 'tag':
            for parent in node.parents:
                plt.plot([node.position.x, parent.position.x], [node.position.y, parent.position.y], color='black',
                         linewidth=0.5)
        elif node.parent != None:
            # plt.plot([node.position.x, node.parent.position.x], [node.position.y, node.parent.position.y], color='black',
            #              linewidth=0.5)
            plt.arrow(node.position.x, node.position.y, node.parent.position.x-node.position.x, node.parent.position.y-node.position.y, head_width=0.05, head_length=0.1, fc='k', ec='k')

        if node.type == 'tag':
            plt.plot(node.position.x, node.position.y, color='red', marker='o')
        else:
            if node.sink:
                plt.plot(node.position.x, node.position.y, color='royalblue', marker='s')
            else:
                plt.plot(node.position.x, node.position.y, color='green', marker='s')
        # plt.annotate(str(node.Q), (node.position.x, node.position.y), xytext=(0, 4),
        #              textcoords='offset points')
        plt.annotate(str(node.name), (node.position.x, node.position.y), xytext=(0, -8),
                     textcoords='offset points')

    legend_elements = [Line2D([0], [0], color='red', marker='o', label='mobile'),
                       Line2D([0], [0], color='royalblue', marker='s', label='anchor (root)'),
                       Line2D([0], [0], color='green', marker='s', label='anchor'),
                       Line2D([0], [0], color='black', linewidth=1, label='physical link')]
    plt.legend(handles=legend_elements)
    plt.savefig(filepath)
    plt.close()


def dot_network_routing(all_nodes, filepath):
    """ function to call dot 
    dot -Kfdp -n -Tpdf -Gdpi=300 -o dot_network_routing.pdf dot_network_routing.dot
    """
    f = open(filepath, "w")
    f.write("digraph D { \n")
    f.write("  overlap=true; \n")

    for node in all_nodes:
        if node.type == 'tag':
            f.write(str(node.name) + " [label=\""+node.name+"\\n"+str(node.get_Q())+"\", shape=circle, pos = \""+str(node.position.x)+",-"+str(node.position.y)+"!\"] \n")
        else:
            if node.sink :
                color = "red"
            else:
                color = "black"
            f.write(str(node.name) + " [label=\""+node.name+"\\n"+str(node.get_Q())+"\", shape=square, pos = \""+str(node.position.x)+",-"+str(node.position.y)+"!\", color = "+color+"] \n")

    for node in all_nodes:


        if node.type == 'tag':
            for i in range(len(node.parents)):
                f.write(str(node.name) + " -> " + str(node.parents[i].name) + " [ label = \"" + str(node.parents_w[i])+"\" fontcolor=\"blue\"]\n")
        elif node.parent != None:
            # plt.plot([node.position.x, node.parent.position.x], [node.position.y, node.parent.position.y], color='black',
            #              linewidth=0.5)

            f.write(str(node.name) + " -> " + str(node.parent.name) + " [ label = \"" + str(node.get_Q())+"\"fontcolor=\"red\"]\n")

    f.write("}")

    f.close()
    command = "dot -Kfdp -n -Tpdf -Gdpi=300 -o "+filepath[0:-4]+".pdf "+filepath
    os.system(command)  
