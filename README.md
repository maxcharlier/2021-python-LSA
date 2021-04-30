# 2021-python-LSA
Localisation Scheduling Algorithm


##csv-generator.py
Take as input:
- the grid size x (in meter)
- the grid size y (in meter)
- the space between node (in meter)
- the communication range (in meter)
- the disruption range (in meter, >= communication range) 
- R the number of tag per cells (int, default 1)
- the number of localisation per tag (default 1)
- the duration of a time slot
------
Show the grid and ask for a list of sink.

Return:
- A csv containing previews parameters, a set of nodes (name, x, y, anchors or tags), a list of edge tag to anchors, a connectivity graph C based on the position of nodes and the disuption range, a routing graph G based on the communication range, the set of sink and dijkstra algorithm. Edges of W have an attribute : W the number of message to transmit between nodes.

##tasa-algorithm.py
Take as input a CSV file generate by csv-generator.py and return a csv file containing :
- The list of node with position
- The number of message transmit and received per node
- the slotframe ordered by timeslot and channel offset

##fig-slotframe.py
Take as input a VSC file and return figures such as 
- For each nodes, order by distance with the sink, the number of message to transmit and receive
- For each nodes, order by distance with the sink, the duty cycle

