"""
click on the plot to record min and max points
"""
import os
import datetime
import time
import timeit
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import getallcode
from matplotlib.backend_bases import MouseButton



t0 = timeit.time.time()
reftime1 = 1654099200000.
refdate1 = datetime.date(2022, 6, 2)
linewidth1 = 0.5
linewidth2 = 1.5



# define a function to handle the on_click event
def on_click(event):
    if event.button == MouseButton.RIGHT:   
        x, y = event.xdata, event.ydata
        with open("findextreme4.txt", "a") as f:
            f.write(f"{x} {y}\n")
        print(f"clicked on ({x}, {y})")




def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num-1] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()




code1 = input("fund code: ")
if 1:
   print(getallcode.downdata(code1))
   
   
replace_line('plot.py', 56, 'code2 = [\''+code1+'\'] \n')

   

data = np.genfromtxt('data/'+code1+'worth.txt')
timesec = data[:, 0] 
worth = data[:,1]
reftime2 = timesec[0]


# record min
if(os.path.isfile('findextreme4.txt')):
   os.remove('findextreme4.txt')
print("record minima (right click at least two points)")
fig, ax = plt.subplots()
# right click
fig.canvas.mpl_connect('button_press_event', on_click)
ax.plot(timesec, worth)
plt.show()


extrdata = np.genfromtxt('findextreme4.txt')
if(os.path.isfile('datares/findextreme4_1_min_'+code1+'.txt')):
   extrdata1 = np.genfromtxt('datares/findextreme4_1_min_'+code1+'.txt')
   extrdata2 = np.concatenate((extrdata, extrdata1))
   #print(extrdata2)
   extrdata = extrdata2
      
extrxdata1 = [extrdata[0,0]]
extrydata1 = [extrdata[0,1]]

for i in range(len(extrdata)):
   indicator = 1
   for j in range(len(extrxdata1)):
      #print(i, extrdata[i, 0], extrxdata1[j])
      if abs(extrdata[i, 0]-extrxdata1[j])<5*86400000.:
         indicator = 0
         break
   #print(indicator, extrxdata1)
   if indicator:
      extrxdata1.append(extrdata[i,0])  
      extrydata1.append(extrdata[i,1])
   #print(extrxdata1)

extrxdata1, extrydata1 = np.array(extrxdata1), np.array(extrydata1)
indset_sort = np.flip(np.argsort(extrxdata1))
extrxdata1_sort, extrydata1_sort = extrxdata1[indset_sort], extrydata1[indset_sort]
f = open('datares/findextreme4_1_min_'+code1+'.txt', 'w+') 
for i in range(len(extrxdata1_sort)):
   f.write(('%.1f %.6f ' % (extrxdata1_sort[i], extrydata1_sort[i]) ) + '\n')
f.close()


plt.plot(timesec, worth)
for jj in range(len(extrxdata1_sort)):
   plt.axvline( extrxdata1_sort[jj], linestyle='--', linewidth=linewidth1, color='black')
plt.xlim(0.98*min(extrxdata1_sort), 1.02*max(extrxdata1_sort))
plt.show()



# record max
if(os.path.isfile('findextreme4.txt')):
   os.remove('findextreme4.txt')
print("record maxima (right click at least two points)")
fig, ax = plt.subplots()
# right click
fig.canvas.mpl_connect('button_press_event', on_click)
ax.plot(timesec, worth)
plt.show()


extrdata = np.genfromtxt('findextreme4.txt')
if(os.path.isfile('datares/findextreme4_1_max_'+code1+'.txt')):
   extrdata1 = np.genfromtxt('datares/findextreme4_1_max_'+code1+'.txt')
   extrdata2 = np.concatenate((extrdata, extrdata1))
   #print(extrdata2)
   extrdata = extrdata2
      
extrxdata1 = [extrdata[0,0]]
extrydata1 = [extrdata[0,1]]

for i in range(len(extrdata)):
   indicator = 1
   for j in range(len(extrxdata1)):
      #print(i, extrdata[i, 0], extrxdata1[j])
      if abs(extrdata[i, 0]-extrxdata1[j])<5*86400000.:
         indicator = 0
         break
   #print(indicator, extrxdata1)
   if indicator:
      extrxdata1.append(extrdata[i,0])  
      extrydata1.append(extrdata[i,1])
   #print(extrxdata1)

extrxdata1, extrydata1 = np.array(extrxdata1), np.array(extrydata1)
indset_sort = np.flip(np.argsort(extrxdata1))
extrxdata1_sort, extrydata1_sort = extrxdata1[indset_sort], extrydata1[indset_sort]
f = open('datares/findextreme4_1_max_'+code1+'.txt', 'w+') 
for i in range(len(extrxdata1_sort)):
   f.write(('%.1f %.6f ' % (extrxdata1_sort[i], extrydata1_sort[i]) ) + '\n')
f.close()


plt.plot(timesec, worth)
for jj in range(len(extrxdata1_sort)):
   plt.axvline( extrxdata1_sort[jj], linestyle='--', linewidth=linewidth1, color='black')
plt.xlim(0.98*min(extrxdata1_sort), 1.02*max(extrxdata1_sort))
plt.show()




