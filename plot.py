"""
ema and macd; phase diagram
"""
import sys
import os
import shutil
import datetime
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
import timeit
from PyPDF2 import PdfReader, PdfMerger
import pandas as pd
import getallcode
from scipy import stats


t0 = timeit.time.time()
reftime1 = 1654099200000.
refdate1 = datetime.date(2022, 6, 2)
today = datetime.date.today()
today1 = today-refdate1
today1sec = reftime1+86400000.*today1.days 
     
        
fontsize1 = 7
linewidth1 = 1.5
linewidth2 = 2.5



smoothing = 8.        
avenpt1max, avenpt2max = 160, 410   
avenptset1 = [80]      # adjustable parameter  
#avenptset1 = np.arange(30, avenpt1max, 20, dtype=int)    
avenptset2 = [200]          
sparset = [0.1, 0.2]       # fitting cannot be too particular
#sparset = np.arange(0.01, 0.21, 0.01) 
spar = 0.1            # adjustable parameter 
spar2 = 0.0

rsinptset = [20]


                 
colorset = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown']
rows, colnums = 1, 2
fig, axs = plt.subplots(rows, colnums, figsize=(colnums*6, rows*4))
fig.tight_layout(pad=5.0)   
   
         
code2 = ['000051'] 
update = 0
if update:
   for i in range(len(code2)):
      print(getallcode.downdata1(code2[i]))
      

for iiii in range(len(code2)):   
   code1 = code2[iiii]   
   #code1 = '001156' 
   print(code1)
   data = np.genfromtxt('data/'+code1+'worth.txt')
   timesec = data[:, 0] 
   worth = data[:,1] 
   timeday = np.zeros_like(timesec)
   for i in range(len(timesec)):
      timeday[i] = (timesec[i]-timesec[0])/86400000.
 
   timesec0, worth0, timeday0 = timesec, worth, timeday 
   curnpt = 0       # adjustable parameter
   timesec, worth, timeday = timesec0[curnpt:], worth0[curnpt:], timeday0[curnpt:]
   #print(timeday0[curnpt], timeday[0])
        
               
   ntrim1plot, ntrim2plot = 0, 300                                                          
   axs[0].plot(timeday[ntrim1plot:ntrim2plot], worth[ntrim1plot:ntrim2plot], linewidth = linewidth1, color='black')
    
   data1 = np.genfromtxt('datares/findextreme4_1_max_'+code1+'.txt')  
   timeday1 = np.zeros(len(data1)) 
   indmax = []
   for i in range(len(data1)):
      timeday1[i] = (data1[i,0]-timesec[0])/86400000. 
      if timeday[ntrim2plot]<=timeday1[i]<=timeday[ntrim1plot]:
         indmax.append( np.argmin(abs(data1[i,0]-timesec)) )    
   axs[0].scatter(timeday[indmax], worth[indmax], s=10, color='orange')
   
   data1 = np.genfromtxt('datares/findextreme4_1_min_'+code1+'.txt')  
   timeday1 = np.zeros(len(data1)) 
   indmin = []
   for i in range(len(data1)):
      timeday1[i] = (data1[i,0]-timesec[0])/86400000.
      if timeday[ntrim2plot]<=timeday1[i]<=timeday[ntrim1plot]: 
         indmin.append( np.argmin(abs(data1[i,0]-timesec)) )        
   axs[0].scatter(timeday[indmin], worth[indmin], s=10, color='green')   
           
   
   # ma
   for jjjj in range(len(avenptset1)):
      tempavenpt = avenptset1[jjjj]
      tempnptema = len(worth) - tempavenpt + 1 
      xdata1, ydata1 = np.zeros(tempnptema), np.zeros(tempnptema)
      xdata1[0] = timeday[tempnptema-1]   
      ydata1[0] = np.average(worth[len(worth)-tempavenpt:])      
      for jj in range(1, tempnptema):  
         xdata1[jj] = timeday[tempnptema - 1 - jj]
         ydata1[jj] = worth[tempnptema - 1 - jj]*smoothing/(1.+tempavenpt) + ydata1[jj-1]*(1.-smoothing/(1.+tempavenpt))
      emaxset1, ema1 = np.flip(xdata1), np.flip(ydata1)                     
                     
      axs[0].plot(emaxset1[ntrim1plot:ntrim2plot], ema1[ntrim1plot:ntrim2plot], linewidth = linewidth1)
                  
               
      for kkkk in range(len(avenptset2)):
         tempavenpt = avenptset2[kkkk]
         tempnptema = len(worth) - tempavenpt + 1 
         xdata1, ydata1 = np.zeros(tempnptema), np.zeros(tempnptema)
         xdata1[0] = timeday[tempnptema-1]   
         ydata1[0] = np.average(worth[len(worth)-tempavenpt:])      
         for jj in range(1, tempnptema):  
            xdata1[jj] = timeday[tempnptema - 1 - jj]
            ydata1[jj] = worth[tempnptema - 1 - jj]*smoothing/(1.+tempavenpt) + ydata1[jj-1]*(1.-smoothing/(1.+tempavenpt))
         emaxset2, ema2 = np.flip(xdata1), np.flip(ydata1)        

         axs[0].plot(emaxset2[ntrim1plot:ntrim2plot], ema2[ntrim1plot:ntrim2plot], linewidth = linewidth1)                      
         
         ema12 = ema1[:len(ema2)]-ema2
            
                
         #plot macd vs ma                                 
         plotxdata, plotydata = (ema2+ema1[:len(ema2)])/2, ema12
         axs[1].plot(plotxdata[ntrim1plot:ntrim2plot], plotydata[ntrim1plot:ntrim2plot], linewidth=linewidth1, color=colorset[0])        
         axs[1].scatter(plotxdata[ntrim1plot], plotydata[ntrim1plot], s=30, marker='+', color='red') 
         axs[1].scatter(plotxdata[ntrim2plot-1], plotydata[ntrim2plot-1], s=30, marker='o', color='red')    
 
         axs[1].scatter(plotxdata[indmin], plotydata[indmin], s=30, marker='o', color='green') 
         axs[1].scatter(plotxdata[indmax], plotydata[indmax], s=30, marker='o', color='orange')
         
                                
axs.title()
                                  
         
         

print( '\n *** uses %.2f seconds\n' % (timeit.time.time() - t0))
plt.show()

