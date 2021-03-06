import time
import csv
import math

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
        if self.src.type == 'tag':
            #invert src and dest because anchor initialise the localisation
            return '[{}->{} w={}]'.format(self.dest.name, self.src.name,self.weight)
        else:
            return '[{}->{} w={}]'.format(self.src.name, self.dest.name,self.weight)

    def str_short(self):
        """
        String representation
        :return: String representation
        """
        if self.src.type == 'tag':
            #invert src and dest because anchor initialise the localisation
            return '{}$\\rightarrow${} {}'.format(self.dest.name, self.src.name,self.weight)
        else:
            return '{}$\\rightarrow${} {}'.format(self.src.name, self.dest.name,self.weight)

    def is_data(self):
        return self.src.type == 'anchor' and self.dest.type == 'anchor'

    def is_twr(self):
        return not self.is_data()
    def __repr__(self) -> str:
        """
        Node representation
        :return: Node representation as string
        """
        return self.__str__()

    def get_src_str(self):
        if self.src.type == 'tag':
            #invert src and dest because anchor initialise the localisation
            return '{}'.format(self.dest.name)
        else:
            return '{}'.format(self.src.name)
    def get_dest_str(self):
        if self.src.type == 'tag':
            #invert src and dest because anchor initialise the localisation
            return '{}'.format(self.src.name)
        else:
            return '{}'.format(self.dest.name)


def scheduling(topology, n_ch=8, aggregation=1, max_queue_size=0):
    """
    Returns the complete scheduling of the ranging measurements and their routing to the sinknode.
    :param topology: A topology object with connectivity and routing graph complete
    :param n_ch: The maximum number of channels in the scheduling. By default there is no limit.
    :param aggregation: The number of ranging information than a anchor can agregate
    :param max_queue_size: The maximum of messages than a node (other than a sink) can have in it's queue, A value of 0 or less disable the check
    :return: The scheduling matrix and the execution time in seconds
    """
    if n_ch < 0:
        raise Exception("The number of channels cannot be negative")
    elif n_ch == 0:
        return []

    if max_queue_size > 0 and aggregation >= max_queue_size:
        raise Exception("The aggreagtion value is too big compare to the maximum queue size")

    if aggregation < 1 :
        raise Exception("Anchor need to be able to send at least one message (aggregation >=1)")

    start = time.perf_counter()
    schedule = []
    sinks = [sink for sink in topology.sinks]
    current_slot = 0 #current timeslot/step of the algorithm

    def continue_schedule(sinks):
        """ Check if all sinks have receives mesages of the network"""
        for sink in sinks:
            if sink.get_Q() > sink.get_weight(None):
                return True

        if (len(sinks) > 0):
            return False
        return False
    # print(sinks)
    # While sinks have not received all the ranging measurements from the network
    while continue_schedule(sinks):
        matching = matching_sinks(sinks, current_slot, aggregation, max_queue_size)
        # print("matching")
        # print(matching)
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



def matching_sinks(sinks, slot_number, aggregation, max_queue_size):
    """
    Performs the matching of the graph starting by selecting the sinks with the biggest priority
    :param sinks: roots of the network
    :return: A list of selected sending nodes
    """
    selected = []

    #first order sink by number of message to receive (bigger first)
    sinks_ = list(sinks)
    favorite_sinks = [s for s in sinks_ if s.get_weight(None) < s.get_Q()]
    # print(favorite_sinks)
    while favorite_sinks:
        #order sink by the number of messages they need to receives
        i = favorite_sinks.index(max(favorite_sinks, key=lambda s: s.get_Q()-s.get_weight(None)))
        selected += matching(favorite_sinks[i], slot_number, aggregation, max_queue_size)
        favorite_sinks.remove(favorite_sinks[i])
            

    return selected

def matching_old(anchor, slot_number, aggregation, max_queue_size):
    """
    Performs the matching of the tree graph
    :param anchor: The root of the sub-tree
    :return: A list of selected sending nodes
    """
    selected = []
    #check if the node have childrens
    if anchor.childrens:
        children = [c for c in anchor.childrens if(c.get_Q() > 0)]
        # Check if the queue of anchor is less than max queue size or if it is a sink.
        # In this case anchor can receive message from one of it's children.
        
        #children is listed if 
        # - they are anchor and they have a queue bigger or equals to the aggregation or the queue equals the global queue of the node  
        # or if they are a tag and have message to send to the anchor.
        favorite_children = [c for c in children if (\
            ((c.type == 'anchor' and c.get_weight(anchor) > 0 and (c.get_weight(anchor) >= aggregation or c.get_weight(anchor) == c.get_Q())) \
            or (c.type == 'tag' and c.get_weight(anchor) > 0) and c.get_last_slot_number() < slot_number)) \
            and (max_queue_size <= 0 or (anchor.current_weight+min(c.get_weight(anchor), aggregation) <= max_queue_size) or anchor.sink)]
        #if we have a favorite children we create the link with the best one and add this children to the childre list.
        if favorite_children:
            i = favorite_children.index(max(favorite_children, key=lambda c: c.get_Q()))
            selected += [favorite_children[i]]
            children.remove(favorite_children[i])
            favorite_children[i].set_slot_number(slot_number) #avoid selecting a node two times
            if(favorite_children[i].type == 'anchor'):
                children += list(favorite_children[i].childrens)
            favorite_children[i].set_link(Link(favorite_children[i], anchor, min(favorite_children[i].get_weight(anchor), aggregation)))
            
        for child in children:
            #we only perform the recursive call on anchors
            if child.type == 'anchor':
                selected += matching(child, slot_number, aggregation, max_queue_size)

    return selected

def matching(anchor, slot_number, aggregation, max_queue_size):
    """
    Performs the matching of the tree graph
    :param anchor: The root of the sub-tree
    :return: A list of selected sending nodes
    """
    def rec_call(children):
        """recursive call onf the matching on children sorted by global queue"""
        selected = []

        local_children = children.copy() #avoid edge effect
        while local_children: 
            i = local_children.index(max(local_children, key=lambda n: n.get_Q()))
            child = local_children.pop(i)
            if child.type == 'anchor' and child.get_Q() > 0:
                selected += matching(child, slot_number, aggregation, max_queue_size)
        return selected

    selected = []
    #check if the node have childrens
    if anchor.childrens:
        children = [c for c in anchor.childrens if(c.get_Q() > 0)]
        # Check if the queue of anchor is less than max queue size or if it is a sink.
        # In this case anchor can receive message from one of it's children.
        
        #children is listed if 
        # - they are anchor and they have a queue bigger or equals to the aggregation or the queue equals the global queue of the node  
        # or if they are a tag and have message to send to the anchor.
        favorite_children = [c for c in children if (\
            ((c.type == 'anchor' and c.get_weight(anchor) > 0 and (c.get_weight(anchor) >= aggregation or c.get_weight(anchor) == c.get_Q())) \
            or (c.type == 'tag' and c.get_weight(anchor) > 0) and c.get_last_slot_number() < slot_number)) \
            and (max_queue_size <= 0 or (anchor.current_weight+min(c.get_weight(anchor), aggregation) <= max_queue_size) or anchor.sink)]
        #if we have a favorite children we create the link with the best one and add this children to the childre list.
        if favorite_children:
            i = favorite_children.index(max(favorite_children, key=lambda c: c.get_Q()))
            selected += [favorite_children[i]]
            children.remove(favorite_children[i])
            favorite_children[i].set_slot_number(slot_number) #avoid selecting a node two times
            if(favorite_children[i].type == 'anchor'):
                selected+=rec_call(favorite_children[i].childrens)


            favorite_children[i].set_link(Link(favorite_children[i], anchor, min(favorite_children[i].get_weight(anchor), aggregation)))
        

        selected+=rec_call(children)




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

def export_schedule(schedule, file):
  """Recommanded file name is "schedule.csv" """
  with open(file, 'w') as csvfile:
    fieldnames = ['timeslot', 'channel', 'source', 'destination', 'weight']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    t = 0
    for timeslot in schedule:
      ch = 0
      for channel in timeslot:
        for link in channel:
          # print("t " + str(t) + " ch " + str(ch) + " " + str(link))
          writer.writerow({'timeslot': t, 'channel': ch, 'source': link.get_src_str(), 'destination':link.get_dest_str(), 'weight': link.weight})
        ch += 1
      t+=1

def export_schedule_stat(duration, schedule, topology, file):
  """Recommanded file name is "schedule_stat.csv" """
  with open(file, 'w') as csvfile:
    fieldnames = ['duration', 'len_schedule', 'nb_slot', 'nb_twr', 'nb_data', 'aggregation', 'nb_ch', 'nb_anchors', 'nb_tags']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    t = 0
    len_schedule = len(schedule)
    nb_slot = 0
    nb_twr = 0
    nb_data = 0
    aggregation = 0
    nb_ch = 0

    for timeslot in schedule:
      ch = 0
      for channel in timeslot:
        for link in channel:
          # print("t " + str(t) + " ch " + str(ch) + " " + str(link))
          if link.src.type == 'tag' or  link.dest.type == 'tag':
            nb_twr += 1
          else :
            nb_data += 1
            aggregation += link.weight
          nb_slot += 1
        ch += 1
        nb_ch += 1
      t+=1

    writer.writerow({'duration': str(duration), 'len_schedule': str(len_schedule), 'nb_slot': str(nb_slot), 'nb_twr': str(nb_twr), 'nb_data': str(nb_data), 'aggregation': str(aggregation), 'nb_ch': str(nb_ch), 'nb_anchors' : str(topology.nb_anchors), 'nb_tags' : str(topology.nb_tags)})  


def import_schedule_stat(file):
  """Recommanded file name is "schedule_stat.csv" """
  with open(file) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      return row

def import_schedule(file, nodes):
  """Recommanded file name is "schedule.csv" """
  #initialise list of node name to get node objet in the nodes list based on the name in the CSV file.
  nodes_name = []
  for node in nodes:
    nodes_name.append(node.name)

  schedule = []
  with open(file) as csvfile:
    reader = csv.DictReader(csvfile)
    t = 0
    timeslot = []      
    ch = 0
    channel = []
    for row in reader:
      if (int(row['timeslot'])) > t:
        t = int(row['timeslot'])
        if len(channel) > 0:
          timeslot.append(channel)
        schedule.append(timeslot)
        timeslot = []
        ch = 0
        channel = []

      if(int(row['channel']) > ch):
        timeslot.append(channel)
        channel = []
        ch = int(row['channel'])

      channel.append(Link(nodes[nodes_name.index(row['source'])], nodes[nodes_name.index(row['destination'])], int(row['weight'])))

    if len(channel) > 0:
      timeslot.append(channel)
    if(len(timeslot) > 0):
      schedule.append(timeslot)
  return schedule


def import_queue_sizes(schedule_file, nodes, aggregation=1):
  """ Return the maximum queue size by looking at each link, 
  Recommanded file name is "schedule.csv" """
  nodes_queue = dict([(node.name, [node.type == 'anchor' and node.sink, 0, 0]) for node in nodes])
  max_queue_size = 0
  # max_queue_row = ""
  with open(schedule_file) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      source = nodes_queue[row['source']]
      dest = nodes_queue[row['destination']]
      nodes_queue[row['source']] = [source[0], source[1], source[2]-int(row['weight'])]
      nodes_queue[row['destination']] = [dest[0], max(dest[1], dest[2]+int(row['weight'])), dest[2]+int(row['weight'])]
      # print(str(dest) + str(nodes_queue[row['destination']]))
      if nodes_queue[row['destination']][1] > max_queue_size and not dest[0]:
            max_queue_size = nodes_queue[row['destination']][1]
            # max_queue_row = row
  # print("Maximum queue size in this schedule " +str(max_queue_size))
  # print(str(max_queue_size) + " Max queue row "+ str(max_queue_row))
  # return math.ceil(max_queue_size/aggregation)
  return max_queue_size