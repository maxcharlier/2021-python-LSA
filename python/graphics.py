import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from nodes.anchor import Anchor
from nodes.tag import Tag
from nodes.point import Point
from scheduling import Link
import os
import matplotlib

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

BLUE_COLOR="#00ABCC"
BLUE_COLOR="#00ABCC"
RED_COLOR="#A80039"
GREY_COLOR="#cccccc"
WHITE_COLOR="#FFFFFF"
BLACK_COLOR="#000000"

def plot_slot_frame(schedule, file="plot_slot_frame.pdf", nb_ch = 6):
    """ Plot the slotframe
      """
    len_schedule = len(schedule)

    SLOT_NUMBER = int(len_schedule) + 1
    SLOT_HEIGHT = 0.5
    SLOT_WIDTH = 1.0

    X_START = 1.1 #offset from the left of the figure
    Y_START = 0.7
    X_END = X_START+(SLOT_NUMBER*SLOT_WIDTH)
    Y_END = Y_START+(SLOT_HEIGHT*nb_ch)
    LEGEND_OFFSET = 0.4


    # Latex style
    matplotlib.rc('text', usetex=True)
    matplotlib.rc('font', family='serif')
    matplotlib.rcParams.update({'font.size': 20})
    plt.clf()
    plot_width= (SLOT_NUMBER*SLOT_WIDTH) +1.35
    plot_height= (nb_ch * SLOT_HEIGHT) + 1.5

    print("Figure size : "+ str(plot_width) + ", " +str(plot_height))
    fig = plt.figure(frameon=False, figsize=(plot_width, plot_height))
    # ax = fig.add_subplot(111)
    ax = fig.add_axes([0, 0, 1, 1]) #don't display frame and axis


    x_lim = [0, plot_width]
    y_lim = [0, plot_height]

    def plot_slot(asn, channel_offset, _color=BLUE_COLOR, _text="A $\\rightarrow$ B",
      _shared=False, _text_color=WHITE_COLOR):
      """Draw a rectangle"""
      # if _shared:
      #   for i in range(0, self.channels):
      #     if i != channel_offset:
      #       plot_slot(asn, i, _color=GREY_COLOR, _text="Not allowable", _shared=False, _text_color=BLACK_COLOR)
      x1 = X_START+SLOT_WIDTH*asn
      x2 = x1 + SLOT_WIDTH
      x = [x1, x1, x2, x2]
      y1 = Y_START + SLOT_HEIGHT*channel_offset
      y2 = y1 + SLOT_HEIGHT
      y = [y1, y2, y2, y1]
      ax.fill(x, y, color=_color)
      if len(_text) > 0:
        ax.text(x1+SLOT_WIDTH/2, y1+SLOT_HEIGHT/2, r'\textbf{'+str(_text)+'}', verticalalignment='center', horizontalalignment='center', color=_text_color)

    # plot_slot(0, 3, _color=RED_COLOR, _text="Shared", _shared=True)
    # plot_slot(1, 0, _color=BLUE_COLOR, _text="A $\\rightarrow$ C")

    matplotlib.rcParams.update({'font.size': 12})
    t= 0
    for timeslot in schedule:
      ch = 0
      for channel in timeslot:
        slot_text = ""
        for link in channel:
          if link.is_data():
            color = GREY_COLOR
          else:
            color = BLUE_COLOR
          if len(slot_text) > 0:
            slot_text += "\\\\"

          slot_text += link.str_short()
        
        plot_slot(t, ch, _color=color, _text=slot_text, _shared=False)
          # print("t " + str(t) + " ch " + str(ch) + " " + str(link))

        ch += 1
      t+=1

    matplotlib.rcParams.update({'font.size': 20})

    #draw the tab
    for i in range(0, nb_ch+1):
      line_y = Y_START+(SLOT_HEIGHT*i)
      ax.plot([X_START, X_END], [line_y, line_y], color=BLACK_COLOR, zorder=1)
    for i in range(0, SLOT_NUMBER+1):
      line_x = X_START+(i*SLOT_WIDTH)
      if i % SLOT_NUMBER == 0:
        ax.plot([line_x, line_x], [Y_START, Y_END], color=BLACK_COLOR, zorder=1,linewidth=4.0)
      else:
        ax.plot([line_x, line_x], [Y_START, Y_END], color=BLACK_COLOR, zorder=1, linestyle='--')

    #plot legend channel offset
    x_channel_offset_legend = X_START
    ax.plot([x_channel_offset_legend, x_channel_offset_legend], [Y_START, Y_START+(SLOT_HEIGHT*nb_ch)], color=BLACK_COLOR, zorder=-1)
    legend_end_bar_width = 0.1
    for i in range(0, nb_ch+1):
      y_bar = Y_START + SLOT_HEIGHT*i
      ax.plot([x_channel_offset_legend-legend_end_bar_width/2, x_channel_offset_legend+legend_end_bar_width/2], [y_bar, y_bar], color=BLACK_COLOR, zorder=-1)

    for i in range(0, nb_ch):
      y_bar = Y_START + SLOT_HEIGHT*i + SLOT_HEIGHT/2
      ax.text(X_START-legend_end_bar_width, y_bar, r""+str(i)+"", verticalalignment='center', horizontalalignment='right')
    ax.text(X_START-LEGEND_OFFSET, Y_START+ (Y_END-Y_START)/2, r"\huge\begin{center}\textbf{Channel Offset\\(Freq. domain)}\end{center}", verticalalignment='center', rotation='vertical', horizontalalignment='right')

    #plot legend ASN
    y_asn_legend = Y_START
    ax.plot([X_START, X_END], [y_asn_legend, y_asn_legend], color=BLACK_COLOR, zorder=-1)
    arrow_lenght = (0.66)*LEGEND_OFFSET
    ax.arrow(X_START, y_asn_legend, X_END-X_START+2*legend_end_bar_width, 0,
        head_starts_at_zero=False, length_includes_head= True, fc='k', ec='k',
        head_width=legend_end_bar_width, head_length=legend_end_bar_width)
    for i in range(0, SLOT_NUMBER+1):
      x_bar = X_START + SLOT_WIDTH*i
      ax.plot([x_bar, x_bar], [y_asn_legend-legend_end_bar_width/2, y_asn_legend+legend_end_bar_width/2], color=BLACK_COLOR, zorder=-1)

    for i in range(0, SLOT_NUMBER):
      x_bar = X_START + SLOT_WIDTH*i + SLOT_WIDTH/2
      ax.text(x_bar, Y_START-legend_end_bar_width, r""+str(i)+"", verticalalignment='top', horizontalalignment='center')
    ax.text(X_START+(X_END-X_START)/2, Y_START-LEGEND_OFFSET, r"\huge\begin{center}\textbf{Absolute Slot Number (ASN) - (Time domain)}\end{center}", verticalalignment='top', horizontalalignment='center')


    #plot legend TSN
    y_asn_legend = Y_END
    ax.plot([X_START, X_END], [y_asn_legend, y_asn_legend], color=BLACK_COLOR, zorder=-1)
    arrow_lenght = (0.66)*LEGEND_OFFSET
    ax.arrow(X_START, y_asn_legend, X_END-X_START+2*legend_end_bar_width, 0,
        head_starts_at_zero=False, length_includes_head= True, fc='k', ec='k',
        head_width=legend_end_bar_width, head_length=legend_end_bar_width)
    for i in range(0, SLOT_NUMBER+1):
      x_bar = X_START + SLOT_WIDTH*i
      ax.plot([x_bar, x_bar], [y_asn_legend-legend_end_bar_width/2, y_asn_legend+legend_end_bar_width/2], color=BLACK_COLOR, zorder=-1)

    for i in range(0, SLOT_NUMBER):
      x_bar = X_START + SLOT_WIDTH*i + SLOT_WIDTH/2
      ax.text(x_bar, Y_END+legend_end_bar_width, r""+str((i)%len_schedule)+"", verticalalignment='bottom', horizontalalignment='center')
    ax.text(X_START+(X_END-X_START)/2, Y_END+LEGEND_OFFSET, r"\huge\begin{center}\textbf{TimeSlot Number (TSN)}\end{center}", verticalalignment='bottom', horizontalalignment='center')


    # plot_slot(3, 3, _color=BLUE_COLOR, _text="B $\\rightarrow$ D")
    plt.xlim(x_lim)
    plt.ylim(y_lim)


    plt.axis('off') #remove axis


    #plt.tight_layout() # Avoid matplotlib to hide the axis label
    # plt.show()
    plt.savefig(file, format='pdf', dpi=1000, bbox_inches='tight', pad_inches=0)

def plot_slotframe_distrib(schedule, file="plot_slotframe_distrib.pdf"):
  """ Plot the number of communication per cells"""
  #cells counter
  nb_comm = range(0, 100)
  c_comm_all = [0 for i in range(0, len(nb_comm))]
  c_weight_all = [0 for i in range(0, len(nb_comm))]
  #timeslot counter
  t_comm_all = [0 for i in range(0, len(nb_comm))]
  t_weight_all = [0 for i in range(0, len(nb_comm))]

  for timeslot in schedule:
    t_comm = 0
    t_weight = 0
    for channel in timeslot:
      c_comm_all[len(channel)] += 1
      c_weight = 0
      for link in channel:
        c_weight += link.weight
        nb_comm +=1
      c_weight_all[c_weight] += 1
      t_comm += len(channel)
      t_weight += c_weight
    t_comm_all[t_comm] += 1
    t_weight_all[t_weight] += 1

  # convert to %
  def convert_to_pourcent(_list):
    tot = sum(_list)
    for i in range(len(_list)):
      _list[i] = float(_list[i])/tot * 100.0

  plt.title("Slotframe Communications distribution")
  plt.plot(nb_comm, convert_to_pourcent(c_comm_all), label="Communication per cells")
  plt.plot(nb_comm, convert_to_pourcent(c_weight_all), label="Agreagation per cells")
  plt.plot(nb_comm, convert_to_pourcent(t_comm_all), label="Communication per timeslot")
  plt.plot(nb_comm, convert_to_pourcent(t_weight_all), label="Agreagation per timeslot")


  plt.legend()

  plt.savefig(file)
  plt.close()
        
      