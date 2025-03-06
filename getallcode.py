"""
get fund data from https://fund.eastmoney.com/
"""
import requests
import time
import timeit
import execjs
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import datetime
import calendar
import json
import shutil


t0 = timeit.time.time()
now = datetime.datetime.now()
datetoday = now.date()
#print(now, datetoday)
reftime1 = 1654099200000.
refdate1 = datetime.date(2022, 6, 2)
deltadays = datetoday - refdate1 
timetoday = deltadays.days*86400000. + reftime1 
#print(timetoday)



def inducdatem(givendate, days):
   return givendate - datetime.timedelta( days )  
   
def inducdatep(givendate, days):
   return givendate + datetime.timedelta( days )    
   
 
def inducdaym(givendate, days):
   date2 = givendate - datetime.timedelta( days )
   born = date2.weekday()
   return (calendar.day_name[born])
    
def inducdayp(givendate, days):
   date2 = givendate + datetime.timedelta( days )
   born = date2.weekday()
   return (calendar.day_name[born])
   
   

   
def getUrl(fscode):
   head = 'http://fund.eastmoney.com/pingzhongdata/'
   tail = '.js?v=' + time.strftime("%Y%m%d%H%M%S", time.localtime())
   return head+fscode+tail


def downdata(fscode):
   content = requests.get(getUrl(fscode))
   
   jsContent = execjs.compile(content.text)
   name = jsContent.eval('fS_name')
   code = jsContent.eval('fS_code')
   
   netWorthTrend = jsContent.eval('Data_netWorthTrend') # worth in Alipay
   ACWorthTrend = jsContent.eval('Data_ACWorthTrend')
   time1=netWorthTrend[::-1][0]['x']
   time2 = netWorthTrend[::-1][-1]['x']        
   netWorth = []
   xtimenetWorth = []
   ACWorth = []
   xtimeACWorth = []

   f = open("data/"+code+"worth.txt", "w+")   
   for i in range(len(netWorthTrend[::-1])):
      dayWorth = netWorthTrend[::-1][i]   
      dayACWorth = ACWorthTrend[::-1][i]
      if dayACWorth[1]!=None and dayWorth['y']!=None:      
         f.write(  ('%.1f %f %f' % (dayWorth['x'], dayWorth['y'], dayACWorth[1] ) ) + '\n' )   
   f.close()
   #f = open(code+"ac.txt", "w+")          
   #for dayACWorth in ACWorthTrend[::-1]:
   #   xtimeACWorth.append(dayACWorth[0])
   #   ACWorth.append(dayACWorth[1])
   #   f.write(  ('%.1f %f' % (dayACWorth[0], dayACWorth[1] ) ) + '\n' )   
   #f.close()   
   
   daysint1 = (time1-reftime1)/86400000.
   date1 = inducdatep(refdate1, daysint1)
   return {'name': name, 'code': code, 'days': (time1-time2)/86400000, 'currenttime': date1}

  
def getworth(fscode):
   content = requests.get(getUrl(fscode))
   
   jsContent = execjs.compile(content.text)
   name = jsContent.eval('fS_name')
   code = jsContent.eval('fS_code')
   
   netWorthTrend = jsContent.eval('Data_netWorthTrend') # time in 1/1000 second
   ACWorthTrend = jsContent.eval('Data_ACWorthTrend')
   time1, networth=netWorthTrend[::-1][0]['x'], netWorthTrend[::-1][0]['y']   
   acworth=ACWorthTrend[::-1][0][1]
   time2 = netWorthTrend[::-1][-1]['x'] 
   
   return {'name': name, 'code': code, 'networth': networth, 'acworth': acworth, 'days': (time1-time2)/86400000 }
   
      
def getAllCode(): # get all the funds' code
   url = 'http://fund.eastmoney.com/js/fundcode_search.js'
   content = requests.get(url)
   jsContent = execjs.compile(content.text)
   rawData = jsContent.eval('r')
   allCode = []
   allNamezh = []
   allNameen = []
   f = open('data/list_all_'+time.strftime("%Y%m%d", time.localtime())+'.txt', 'w+') 
   for code in rawData:
      allCode.append(code[0])
      allNamezh.append(code[2])
      allNameen.append(code[4])
      if '后端' not in code[2]:      
         f.write( code[0] + ' ' + code[2] + ' ' + code[4] + '\n' )
   f.close()
   
   #shutil.copyfile('data/list_all_'+time.strftime("%Y%m%d", time.localtime())+'.txt', 'data/list_all.txt')
   
   return allCode


def getestimate(fscode): #净值日期、单位净值、估算值、估算增长率、估算时间
   content = requests.get("http://fundgz.1234567.com.cn/js/{}.js".format(fscode))
   data = content.text.replace("jsonpgz(", "").replace(");", "")
   if len(data) !=0 :
      body = json.loads(data)
      return body
   else:
      return {}   

def downdata1(fscode): # download data with the estimated current-day worth
   f = open("data/"+fscode+"worth.txt", "w+") 
   date1 = inducdatem(datetoday, 1)
   time1, time2 = 0, 0
      
   try:
      content = requests.get("http://fundgz.1234567.com.cn/js/{}.js".format(fscode))
      data = content.text.replace("jsonpgz(", "").replace(");", "")
      if len(data)!=0:
         body = json.loads(data)
         f.write(  '%.1f ' % timetoday + body['gsz'] + ' ' + body['gsz'] + '\n' )   
         date1 = body['gztime']
      
      content = requests.get(getUrl(fscode))   
      jsContent = execjs.compile(content.text)
      name = jsContent.eval('fS_name')
      code = jsContent.eval('fS_code')
   
      netWorthTrend = jsContent.eval('Data_netWorthTrend') # worth in Alipay
      ACWorthTrend = jsContent.eval('Data_ACWorthTrend')
      #print(netWorthTrend)
      if len(netWorthTrend)>=3*30:
         time1=netWorthTrend[::-1][0]['x']
         time2 = netWorthTrend[::-1][-1]['x']        
  
         for i in range(len(netWorthTrend[::-1])):
            dayWorth = netWorthTrend[::-1][i]   
            dayACWorth = ACWorthTrend[::-1][i]
            if dayACWorth[1]!=None and dayWorth['y']!=None:      
               f.write(  ('%.1f %f %f' % (dayWorth['x'], dayWorth['y'], dayACWorth[1] ) ) + '\n' ) 
      else:
         print("data too short! ")
         f.write(  ('%.1f %f %f' % (1, 1, 1 ) ) + '\n' )
         f.write(  ('%.1f %f %f' % (1, 1, 1 ) ) + '\n' )
              
      f.close()
      
   except:
      name, code ='', ''

      
   return {'name': name, 'code': code, 'days': (time1-time2)/86400000, 'currenttime': date1}
   
   

#print( getUrl('012809') )

#content = requests.get("http://fundgz.1234567.com.cn/js/{}.js".format('001984'))
#data = content.text.replace("jsonpgz(", "").replace(");", "")
#print(data)
#print(getestimate('519002'))


#codeset = getAllCode()
#print( downdata1('001479') )



#print( '\n *** runtime: %.2f seconds ***\n' % (timeit.time.time() - t0))
#plt.show()



