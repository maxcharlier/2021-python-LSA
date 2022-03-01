
step = [0.1, 0.71, 1.6, 2, 2.5, 3, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10., 11, 11.5, 12, 12.5, 13, 13.5]
print("x,y,space,comm_range,disruption_range,R,nb_tag_loc,sink_allocation,nb_sink,nb_ch,agregation,directory,dist_sink")
for dist_sink in step:
  print("20,20,1,1.5,2,1,1,best,1,1,14,./result/ch1-agr14-dist-"+str(dist_sink)+"/,"+str(dist_sink))