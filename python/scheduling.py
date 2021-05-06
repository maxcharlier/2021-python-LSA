import time

class Link():
    def __init__(self, src, dest, weight = 1):
        self.src = src
        self.dest = dest
        self.weight = weight

    def get_weight(self):
        return self.weight

    def __str__(self):
        """
        String representation
        :return: String representation
        """
        return '[{}->{} w={}]'.format(self.src.name, self.dest.name,self.weight)

    def __repr__(self) -> str:
        """
        Node representation
        :return: Node representation as string
        """
        return self.__str__()

def scheduling(topology, n_ch=8, agregation=1):
    """
    Returns the complete scheduling of the ranging measurements and their routing to the sinknode.
    :param topology: A topology object with connectivity and routing graph complete
    :param n_ch: The maximum number of channels in the scheduling. By default there is no limit.
    :param agregation: The number of ranging information than a anchor can agregate
    :return: The scheduling matrix and the execution time in seconds
    """
    if n_ch < 0:
        raise Exception("The number of channels cannot be negative")
    elif n_ch == 0:
        return []

    if agregation < 1 :
        raise Exception("Anchor need to be able to send at least one message (agregation >=1)")

    start = time.perf_counter()
    schedule = []
    sinks = [sink for sink in topology.sinks]
    current_slot = 0 #current timeslot/step of the algorithm

    def end_shedule(sinks):
        """ Check if all sinks have receives mesages of the network"""
        for sink in sinks:
            if sink.get_Q() > sink.get_weight(None):
                return True

        if (len(sinks) > 0):
            return False
        return False
    print(sinks)
    # While sinks have not received all the ranging measurements from the network
    while end_shedule(sinks):
        matching = matching_sinks(sinks, current_slot, agregation)
        print("matching")
        print(matching)
        colored = coloring(matching, n_ch)
        timeslot = []
        for color in colored:
            # cell = [n.send_packet_to_parent(loc_packet) for n in color if n.rang_measurements]
            cell = []
            for node in color:
                cell.append(node.get_link())
                node.send_packet(node.get_link().dest, node.get_link().weight)
            timeslot.append(cell)
        schedule.append(timeslot)
        current_slot += 1

    stop = time.perf_counter()
    return (schedule), stop - start



def matching_sinks(sinks, slot_number, agregation):
    """
    Performs the matching of the graph starting by selecting the sinks with the biggest priority
    :param sinks: roots of the network
    :return: A list of selected sending nodes
    """
    selected = []

    #first order sink by number of message to receive (bigger first)
    sinks_ = list(sinks)
    favorite_sinks = [s for s in sinks_ if s.get_weight(None) < s.get_Q()]
    print(favorite_sinks)
    while favorite_sinks:
        #order sink by the number of messages they need to receives
        i = favorite_sinks.index(max(favorite_sinks, key=lambda s: s.get_Q()-s.get_weight(None)))
        selected += matching(favorite_sinks[i], slot_number, agregation)
        favorite_sinks.remove(favorite_sinks[i])
            

    return selected

def matching(anchor, slot_number, agregation):
    """
    Performs the matching of the tree graph
    :param anchor: The root of the sub-tree
    :return: A list of selected sending nodes
    """
    selected = []
    #check if the node have childrens
    if anchor.childrens:
        children = list(anchor.childrens)
        #children is listed if 
        # - they are anchor and they have a queue bigger or equals to the agregation or the queue equals the global queue of the node  
        # or if they are a tag and have message to send to the anchor.
        favorite_children = [c for c in children if (c.type == 'anchor' and c.get_weight(anchor) > 0 and (c.get_weight(anchor) >= agregation or c.get_weight(anchor) == c.get_Q()) or c.get_weight(anchor) > 0) and c.get_last_slot_number() < slot_number]
        #if we have a favorite children we create the link with the best one and add this children to the childre list.
        if favorite_children:
            i = favorite_children.index(max(favorite_children, key=lambda c: c.get_Q()))
            selected += [favorite_children[i]]
            children.remove(favorite_children[i])
            favorite_children[i].set_slot_number(slot_number) #avoid selecting a node two times
            if(favorite_children[i].type == 'anchor'):
                children += list(favorite_children[i].childrens)
            favorite_children[i].set_link(Link(favorite_children[i], anchor, min(favorite_children[i].get_weight(anchor), agregation)))

        for child in children:
            #we only perform the recursive call on anchors
            if child.type == 'anchor':
                selected += matching(child, slot_number, agregation)

    return selected


def coloring(nodes, n_colors):
    """
    Performs the coloring of the interference graph whose nodes are passed as a parameter
    :param nodes: The nodes of the interference graph
    :param n_colors: Maximum number of colors
    :return: A list of lists. The i-th list contains the nodes of the color i.
    """
    colored = []
    remaining = list(nodes)
    c = 0
    while remaining:
        colored.append([])
        while remaining:
            i = remaining.index(max(remaining, key=lambda n: n.get_Q()))
            selected = remaining.pop(i)
            colored[c] += [selected]
            not_interf = []
            for n in remaining:
                if not interfering(n, selected):
                    not_interf += [n]
            remaining = not_interf

        c += 1
        if c == n_colors:
            break

        colored_nodes = [node for color_list in colored for node in color_list]

        remaining = []
        for n in nodes:
            if n not in colored_nodes:
                remaining += [n]

    return colored


def interfering(n1, n2):
    """
    Function allowing to check if there is interference between links (n1 -> dest1) and (n2 -> dest2).
    We use the last link store in each node and check in the interference graph if there is a link n1 -> dest2 or n2 -> dest1
    :param n1: The first node
    :param n2: The second node
    :return: True if there is interference between links (n1 -> dest1) and (n2 -> dest2)
    """
    return (n1 in n2.get_link().dest.disrupted_nodes) or (n2 in n1.get_link().dest.disrupted_nodes)

def print_schedule(schedule):
    t = 0
    for timeslot in schedule:
        ch = 0
        for channel in timeslot:
            for link in channel:
                print("t " + str(t) + " ch " + str(ch) + " " + str(link))
            ch += 1
        t+=1